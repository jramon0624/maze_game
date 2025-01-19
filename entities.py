import random as rd
from typing import Optional, List, Tuple


class MazeGenerator():
    def __init__(self,color=(34,139,34)):
        self.position = [0,0]
        self.color = color
        self.visited = []
        self.goal = []
        self.len_to_goal = 0
    
    def get_available(self,matrix):

        pos_available = []
        positions = [[a[0]+b[0],a[1]+b[1]] for a, b in zip([self.position for _ in range(4)],[[0,2],[2,0],[0,-2],[-2,0]])]

        for position in positions:
            if self.available(position,matrix):
                if matrix[position[0]][position[1]] == 0:
                    pos_available.append(position)
        
        return pos_available

    def available(self, position: list, matrix: list):
        rows = len(matrix)
        cols = len(matrix[0])

        if not position[0] in range(rows):
            return False
        elif not position[1] in range(cols):
            return False

        return True

    def move(self,position, matrix):
        direction = [(position[0]-self.position[0])//2,(position[1]-self.position[1])//2]
        for _ in range(2):
            self.change_to_visited(matrix)
            self.position[0] += direction[0]
            self.position[1] += direction[1]

    def change_to_visited(self,matrix):
        value = matrix[self.position[0]][self.position[1]]
        if value == 0:
            matrix[self.position[0]][self.position[1]] = 1
        elif value == 1:
            matrix[self.position[0]][self.position[1]] = 2
    
    def set_goal(self):
        if self.len_to_goal < len(self.visited):
            self.goal = self.position.copy()
            self.len_to_goal = len(self.visited)
    
class AgentT1(MazeGenerator):
    def __init__(self,color,*args) -> None:
        self.position = [0,0]
        self.tour = []
        self.prev_pos = []
        self.color = color
        self.motion = True
    
    def get_available(self,maze):
        self.pos_available = []
        positions = [[a[0]+b[0],a[1]+b[1]] for a, b in zip([self.position for _ in range(4)],[[0,1],[1,0],[0,-1],[-1,0]])]

        for position in positions:
            if self.available(position,maze):
                if not maze[position[0]][position[1]] == 0:
                    self.pos_available.append(position)
    
    def move(self,maze,*args):          # Linea modificada
        self.get_available(maze)

        if self.pos_available:
            while True:
                next_pos = rd.choice(self.pos_available)
                if not next_pos == self.prev_pos:
                    self.prev_pos = self.position.copy()
                    break
                elif len(self.pos_available) == 1:
                    self.prev_pos = self.position.copy()
                    break
        else:
            next_pos = self.position
        
        if next_pos in self.tour:
            self.tour.append(next_pos)
        if not self.position in self.tour:
            self.tour.append(self.position.copy())
        else:
            self.tour.remove(self.position)
        
        self.position = next_pos
        

class AgentT2(MazeGenerator):
    def __init__(self,color,*args) -> None:
        self.position = [0,0]
        self.visited = []
        self.visited_copy = []
        self.tour = []
        self.color = color
        self.motion = True
    
    def get_available(self,maze):
        self.pos_available = []
        positions = [[a[0]+b[0],a[1]+b[1]] for a, b in zip([self.position for _ in range(4)],[[0,1],[1,0],[0,-1],[-1,0]])]

        for position in positions:
            if self.available(position,maze):
                if not maze[position[0]][position[1]] == 0 and not position in self.visited:
                    self.pos_available.append(position)
    
    def move(self,maze,*args):              # Linea modificada
        self.get_available(maze)

        if self.pos_available:
            next_pos = rd.choice(self.pos_available)
            self.tour.append(self.position)
            self.visited.append(self.position)
        else:
            next_pos = self.tour.pop()
            self.visited.append(self.position)
        
        self.position = next_pos


class AgentT3(AgentT2):
    def find_alternative_route(self, position: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Busca una ruta alternativa en caso de encontrarse con un obstáculo.
        Optimizado para reducir operaciones innecesarias.
        """
        stack = [(position, [position])]
        visited = set()
        
        while stack:
            current, path = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    if self.maze[neighbor[1]][neighbor[0]] == 'END':
                        return new_path
                    stack.append((neighbor, new_path))
        return None