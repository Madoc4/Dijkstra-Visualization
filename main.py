import pygame
from collections import defaultdict
import random
import math
from heapq import heapify, heappop, heappush


pygame.init()

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

def get_dist(node1: list, node2: list) -> float:
    return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5

def randomize_weights(dist: float) -> int:
    return math.floor(dist * (random.choices([i for i in range(1,6)], weights=(50, 25, 15, 7, 3))[0]) / 100 + 1)

def make_graph(edges: list) -> dict:
    G = defaultdict(list)
    for edge in edges:
        dist = get_dist(edge[0], edge[1])
        weight = randomize_weights(dist)
        G[edge[0]].append([edge[1], weight])
        G[edge[1]].append([edge[0], weight])
    return G

def plot_shortest(p: list):
    for node in p:
        pygame.draw.circle(screen, (255, 0, 0), node, 5)
    for i in range(len(p) - 1):
        pygame.draw.line(screen, (0, 0, 255), p[i], p[i + 1], 3)


buttons = []
nodes = []
edges = []

quit_button = Button("Quit", 10, 10, "freesansbold.ttf", 20, (255, 0, 0), True)
set_edges_button = Button("Set Edges", 10, screen_height // 3 + 10, "freesansbold.ttf", 20, (0, 255, 0), True)
auto_edges_button = Button("Auto Edges", 10, screen_height // 3 * 2 + 10, "freesansbold.ttf", 20, (0, 0, 255), True)
buttons.extend([quit_button, set_edges_button, auto_edges_button])
auto_edges = False
input_rect = pygame.Rect(10, screen_height // 3 * 2 + 120, 140, 32)
input_text = ''
active = False
delete = False
new_inp = False
changed = False
distances = {}
distance = None
p_to_end = []
p = {}
font = pygame.font.Font('freesansbold.ttf', 20)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if auto_edges_button.check_click(pygame.mouse.get_pos()):
                    auto_edges = True
                    input_text = ''

    if auto_edges:
        num_nodes_button = Button("Number of Rows/Columns: ", 10, screen_height // 3 * 2 + 100, "freesansbold.ttf", 20, (0, 0, 0), False)
        num_nodes_button.draw(screen)
        num_nodes = 0
       
        if len(input_text.split()) == 2:
            num_rows, num_columns = int(input_text.split()[0]), int(input_text.split()[1])
            nodes = plot_nodes(num_rows, num_columns)
            edges = plot_edges(nodes, num_rows, num_columns)
            if changed:
                start_node = nodes[0]
                end_node = nodes[-1]
                G = make_graph(edges)
                distances, p = dijkstra_path(G, nodes[0])
                distance = distances[nodes[-1]]
                p_to_end = p[end_node]
                changed = False
            plot_shortest(p_to_end)

        if delete: 
            num_nodes = input_text[:-1] 
            nodes = []
            edges = []
            delete = False
            changed = True
            pygame.surface.Surface.fill(screen, (255, 255, 255))
        
        if new_inp:
            pygame.surface.Surface.fill(screen, (255, 255, 255))
            changed = True
            new_inp = False
        
        for node in nodes:
            pygame.draw.circle(screen, (0, 0, 0), node, 5)
        for edge in edges:
            pygame.draw.line(screen, (0, 0, 0), edge[0], edge[1], 1)

    pygame.display.update()
    