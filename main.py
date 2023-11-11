import pygame
from collections import defaultdict
import random
import math
from heapq import heapify, heappop, heappush

# TO-DO: Check for errors in set find distance and implement own heap for dijkstra's and check for scc's to use union find on set_edges


pygame.init()
pygame.display.set_caption("Dijkstra's Algorithm Visualization")

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen.fill((255, 255, 255))


class Button:

    def __init__(self, text, x, y, font_name, font_size, button_color, clickable):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font_name, font_size)
        self.normal_color = button_color
        self.clickable = clickable
        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x = self.x
        self.text_rect.y = self.y

    def draw(self, screen):
        text_surface = self.text_surface
        text_rect = self.text_rect
        screen.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        return self.text_rect.collidepoint(mouse_pos) if self.clickable else False
    
    def check_hover(self, mouse_pos):
        if self.text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 0, 0), self.text_rect, 1)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.text_rect, 1)

def dfs(node, G, visited, component):
    visited[node] = True
    component.append(node)
    for neighbor, _ in G[node]:
        if not visited[neighbor]:
            dfs(neighbor, G, visited, component)

def get_scc(G: dict) -> list:
    visited = {node: False for node in G}
    strongly_connected_components = []

    for node in G:
        if not visited[node]:
            component = []
            dfs(node, G, visited, component)
            strongly_connected_components.append(component)

    return strongly_connected_components

def min_dist_scc(scc1: list, scc2: list) -> list:
    min_distance = float('inf')
    min_edge = None
    if scc1 != scc2:
        for node1 in scc1:
            for node2 in scc2:
                dist = get_dist(node1, node2)
                if dist < min_distance:
                    min_distance = dist
                    min_edge = [node1, node2]
    return [min_edge, min_distance]

def dijkstra_path(G, s):
    E = {s}
    d = {s: 0}
    p = {s: [s]}
    heap = [[n[1], s, n[0]] for n in G[s]]
    heapify(heap)

    while len(E) < len(G):
        n = heappop(heap)
        if n[-1] in E:
            continue
        E.add(n[-1])
        d[n[-1]] = n[0]
        p[n[-1]] = p[n[1]] + [n[-1]]
        for tail, length in G[n[-1]]:
            if tail not in E:
                heappush(heap, [length + d[n[-1]], n[-1], tail])
    return d, p

def plot_nodes(num_rows: int, num_cols: int) -> list:
    nodes = []
    x_buffer = screen_width // 10
    y_buffer = screen_height // 10
    rows = num_rows
    cols = num_cols

    x_spacing = (screen_width - 2 * x_buffer) // cols
    y_spacing = (screen_height - 2 * y_buffer) // rows

    for i in range(rows):
        for j in range(cols):
            x = x_buffer + j * x_spacing + 150
            y = y_buffer + i * y_spacing
            nodes.append((x, y))

    return nodes

def plot_edges(nodes: list, num_rows: int, num_columns: int) -> list:
    edges = []

    for i in range(len(nodes)):
        if (i + 1) % num_columns != 0 and i + 1 < len(nodes):
            edges.append((nodes[i], nodes[i + 1]))
        if i + num_columns < len(nodes):
            edges.append((nodes[i], nodes[i + num_columns]))
    return edges

def get_dist(node1: list, node2: list):
    return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

def randomize_weights(dist: float) -> int:
    return math.floor(dist * (random.choices([i for i in range(1,6)], weights=(50, 25, 15, 7, 3))[0]) / 10 + 1)

def make_graph(edges: list, randomize: bool) -> dict:
    G = defaultdict(list)
    for edge in edges:
        dist = get_dist(edge[0], edge[1])
        if randomize:
            weight = randomize_weights(dist)
        else:
            weight = dist
        G[edge[0]].append([edge[1], weight])
        G[edge[1]].append([edge[0], weight])
    return G

def plot_shortest(p: list):
    for node in p:
        pygame.draw.circle(screen, (255, 0, 0), node, 10)
    for i in range(len(p) - 1):
        pygame.draw.line(screen, (0, 0, 255), p[i], p[i + 1], 3)

def plot_weights(G: dict, path: list, d: int):
    total_distance = 0
    nodes_list = []
    weights = []
    for i in range(len(path) - 1):
        node1, node2 = path[i], path[i + 1]
        nodes_list.append((node1, node2))
        for nodes in G[path[i]]:
            if node2 in nodes:
                weights.append(nodes[1])
    
    for i in range(len(nodes_list)):
        node1, node2 = nodes_list[i]
        dist = weights[i]
        if node1[0] == node2[0]:  
            x = node1[0] - 50
            y = (node1[1] + node2[1]) // 2
        elif node1[1] == node2[1]: 
            x = (node1[0] + node2[0]) // 2
            y = node1[1] - 50
        text_surface = font.render(str(dist), True, (0, 0, 0))
        screen.blit(text_surface, (x, y))
    
    text_surface = font.render(("Total Distance: " + str(sum(weights))), True, (0, 0, 0))
    screen.blit(text_surface, (screen_width // 2, screen_height // 10 * 9))

def get_closest_node(pos: tuple, nodes: list) -> list:
    closest_node = None
    closest_dist = float('inf')
    for node in nodes:
        dist = get_dist(pos, node)
        if dist < closest_dist:
            closest_dist = dist
            closest_node = node
    return closest_node

def get_edges(nodes: list) -> list:
    edges = []
    for node in nodes:
        for neighbor in nodes:
            if node != neighbor:
                edges.append((node, neighbor))

    return edges

def get_2_closest(G: dict) -> dict:
    temp = []
    closest = defaultdict()
    for node in G:
        closest[node] = []
    for node in closest:
        temp = G[node]
        temp.sort(key=lambda x: x[1])
        temp[0][1] = math.floor(temp[0][1])
        temp[2][1] = math.floor(temp[2][1])
        closest[node].append(temp[0])
        closest[node].append(temp[2])
        closest[temp[0][0]].append([node, temp[0][1]])
        closest[temp[2][0]].append([node, temp[2][1]])
    return closest

def draw_weight_set_edge(G: dict, edges: list):
    weights = []
    for i in range(len(edges) - 1):
        for neighbor in G[edges[i]]:
            if edges[i + 1] in neighbor:
                weights.append(math.floor(neighbor[1]))
                break

    for i in range(len(edges) - 1):
        start = edges[i]
        end = edges[i + 1]
        weight = weights[i]
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2

        angle = math.atan2(end[1] - start[1], end[0] - start[0])

        text_offset = 20
        x = mid_x + text_offset * math.cos(angle)
        y = mid_y + text_offset * math.sin(angle)

        text_surface = font.render(str(weight), True, (0, 0, 0))
        screen.blit(text_surface, (x, y))

    text_surface = font.render(("Total Distance: " + str(sum(weights))), True, (0, 0, 0))
    screen.blit(text_surface, (screen_width // 2, screen_height // 10 * 9))

buttons = []
nodes = []
edges = []

quit_button = Button("Quit", 10, 10, "freesansbold.ttf", 20, (255, 0, 0), True)
set_edges_button = Button("Set Edges", 10, screen_height // 3 + 10, "freesansbold.ttf", 20, (0, 255, 0), True)
auto_edges_button = Button("Auto Edges", 10, screen_height // 3 * 2 + 10, "freesansbold.ttf", 20, (0, 0, 255), True)
reset_button = Button("Reset", screen_width - 75, 10, "freesansbold.ttf", 20, (255, 0, 0), True)
buttons.extend([quit_button, set_edges_button, auto_edges_button, reset_button])
auto_edges = False
input_rect = pygame.Rect(10, screen_height // 3 * 2 + 120, 140, 32)
input_text = ''
active = False
delete = False
new_inp = False
changed = False
distances = {}
distance = None
set_edges = False
first = True
p_to_end = []
p = {}
closest = None
start_node = None
end_node = None
cleared = False
selecting = True
font = pygame.font.Font('freesansbold.ttf', 20)
entered_nodes = []
G = {}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.check_click(pygame.mouse.get_pos()):
                pygame.quit()
            if input_rect.collidepoint(event.pos): 
                active = True
            else: 
                active = False

            if reset_button.check_click(pygame.mouse.get_pos()):
                auto_edges = False
                input_text = ''
                active = False
                delete = False
                new_inp = False
                changed = False
                distances = {}
                distance = None
                set_edges = False
                first = True
                p_to_end = []
                p = {}
                closest = None
                start_node = None
                end_node = None
                cleared = False
                selecting = True
                entered_nodes = []
                G = {}
                pygame.surface.Surface.fill(screen, (255, 255, 255))


            if auto_edges and not start_node:
                start_node = get_closest_node(pygame.mouse.get_pos(), nodes)
            elif auto_edges:
                end_node = get_closest_node(pygame.mouse.get_pos(), nodes)
            
            if selecting == True and set_edges:
                entered_nodes.append(pygame.mouse.get_pos())
            
            if selecting == False and set_edges and not start_node:
                start_node = get_closest_node(pygame.mouse.get_pos(), entered_nodes)
            elif selecting == False and set_edges:
                end_node = get_closest_node(pygame.mouse.get_pos(), entered_nodes)

            if set_edges_button.check_click(pygame.mouse.get_pos()):
                auto_edges = False
                input_text = ''
                nodes = []
                set_edges = True
                edges = []
                pygame.surface.Surface.fill(screen, (255, 255, 255))

            if auto_edges_button.check_click(pygame.mouse.get_pos()):
                auto_edges = True
                set_edges = False
                input_text = ''
                nodes = []
                edges = []
                changed = True
                pygame.surface.Surface.fill(screen, (255, 255, 255))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            selecting = False

        if event.type == pygame.KEYDOWN and auto_edges: 
            if event.key == pygame.K_BACKSPACE: 
                input_text = input_text[:-1] 
                delete = True
            elif event.key == pygame.K_RETURN:
                active = False
            else: 
                input_text += event.unicode
                new_inp = True

            

    pygame.draw.rect(screen, (255, 255, 255), input_rect)
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 

    for button in buttons:
        button.draw(screen)
        button.check_hover(pygame.mouse.get_pos())

    if auto_edges:
        num_nodes_button = Button("Number of Rows/Columns: ", 10, screen_height // 3 * 2 + 100, "freesansbold.ttf", 20, (0, 0, 0), False)
        num_nodes_button.draw(screen)
        num_nodes = 0
       
        if len(input_text.split()) == 2:
            num_rows, num_columns = int(input_text.split()[0].strip()), int(input_text.split()[1].strip())
            nodes = plot_nodes(num_rows, num_columns)
            edges = plot_edges(nodes, num_rows, num_columns)

            if not start_node:
                text_surface = font.render(("Click Start Node"), True, (0, 0, 0))
                screen.blit(text_surface, (screen_width // 2, screen_height // 15))
            if start_node and not end_node:
                if cleared == False:
                    screen.fill((255, 255, 255))
                    cleared = True
                text_surface = font.render(("Click End Node"), True, (0, 0, 0))
                screen.blit(text_surface, (screen_width // 2, screen_height // 15))

            if changed and start_node and end_node:
                screen.fill((255, 255, 255))
                G = make_graph(edges, True)
                distances, p = dijkstra_path(G, start_node)
                distance = distances[end_node]
                p_to_end = p[end_node]
                changed = False
        
            plot_shortest(p_to_end)
            plot_weights(G, p_to_end, distance)


        if delete: 
            num_nodes = input_text[:-1] 
            nodes = []
            edges = []
            delete = False
            changed = True
            start_node = None
            end_node = None
            pygame.surface.Surface.fill(screen, (255, 255, 255))
        
        if new_inp:
            pygame.surface.Surface.fill(screen, (255, 255, 255))
            changed = True
            start_node = None
            end_node = None
            new_inp = False
        
        for node in nodes:
            pygame.draw.circle(screen, (0, 0, 0), node, 5)
        for edge in edges:
            pygame.draw.line(screen, (0, 0, 0), edge[0], edge[1], 1)

    elif set_edges:
        if selecting:
            text_surface = font.render(("Click To Add Node. Click Space to Stop."), True, (0, 0, 0))
            screen.blit(text_surface, (screen_width / 2, screen_height // 15))

        if selecting == False:
            if first:
                edges = get_edges(entered_nodes)
                G = make_graph(edges, randomize=False)
                closest = get_2_closest(G)
                sccs = get_scc(closest)
                if len(sccs) > 1:
                    max_connections = 1  

                    for i in range(len(sccs)):
                        connections_count = 0

                        closest_sccs = sorted(range(len(sccs)), key=lambda j: min_dist_scc(sccs[i], sccs[j])[1])

                        for j in closest_sccs:
                            if connections_count < max_connections and i != j:
                                min_edge, min_distance = min_dist_scc(sccs[i], sccs[j])
                                print(min_edge, min_distance)
                                edges.append(min_edge)
                                closest[min_edge[0]].append([min_edge[1], min_distance])
                                closest[min_edge[1]].append([min_edge[0], min_distance])
                                connections_count += 1

                screen.fill((255, 255, 255))
                first = False

        if not first:
            if not start_node:
                text_surface = font.render(("Click Start Node"), True, (0, 0, 0))
                screen.blit(text_surface, (screen_width // 2, screen_height // 15))
            if start_node and not end_node:
                if cleared == False:
                    screen.fill((255, 255, 255))
                    cleared = True
                text_surface = font.render(("Click End Node"), True, (0, 0, 0))
                screen.blit(text_surface, (screen_width // 2, screen_height // 15))
            
            if start_node and end_node:
                screen.fill((255, 255, 255))
                # shouldn't need this but for some reason buttons are not being drawn
                for button in buttons:
                    button.draw(screen)
                    button.check_hover(pygame.mouse.get_pos())
                distances, p = dijkstra_path(closest, start_node)
                distance = distances[end_node]
                p_to_end = p[end_node]
                changed = True
                plot_shortest(p_to_end)
                draw_weight_set_edge(G, p_to_end)

        for node in entered_nodes:
            pygame.draw.circle(screen, (0, 0, 0), node, 5)
        
        if closest:
            for node in closest:
                for neighbor in closest[node]:
                    pygame.draw.line(screen, (0, 0, 0), node, neighbor[0], 1)

    pygame.display.update()
    screen.fill((255, 255, 255))
    