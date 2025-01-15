import random as rd

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


### Agente modificado
class AgentT3(MazeGenerator):
    def __init__(self,color,*args) -> None:
        self.position = [0,0]
        self.visited = []
        self.visited_copy = []
        self.tour = []
        self.next_path = []
        self.color = color
        self.motion = True
    
    def get_available(self,maze,position_,visited_):
        self.pos_available = []
        positions = [[a[0]+b[0],a[1]+b[1]] for a, b in zip([position_ for _ in range(4)],[[0,1],[1,0],[0,-1],[-1,0]])]

        for position in positions:
            if self.available(position,maze):
                if not maze[position[0]][position[1]] == 0 and not position in visited_:
                    self.pos_available.append(position)

    def move(self,maze,goal,*args):
        if not self.next_path:
            self.get_available(maze,self.position,self.visited)

            if len(self.pos_available) == 1 :
                next_pos = rd.choice(self.pos_available)
                self.tour.append(self.position)
                self.visited.append(self.position)
                self.position = next_pos
            else:
                # [[0, 0], [0, 1], [1, 0], [1, 1]]
                # [[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]]
                self.next_path.extend([[pos_available] for pos_available in self.pos_available])
                self.visited.append(self.position)
                self.visited_copy = [self.visited.copy() for _ in range(len(self.pos_available))]
                self.position = self.visited.pop()
        elif len(self.next_path) > 1:
            path_to_delete = []            
            new_paths = []
            new_visited = []
            for path, visited in zip(self.next_path,self.visited_copy):
                position = path[-1]
                maze[position[0]][position[1]] = 3
                self.get_available(maze,position,visited)
                
                new_path = len(self.pos_available) - 1

                visited.append(position)

                if new_path == 0:
                    path.append(self.pos_available[0])
                elif new_path > 0:
                    for new_position in self.pos_available[1:]:
                        new_paths.append(path.copy())
                        new_paths[-1].append(new_position)
                        new_visited.append(visited)
                    path.append(self.pos_available[0])
                else:
                    path_to_delete.append((path,visited))

            for path, visited in path_to_delete:
                if not goal in path:
                    self.next_path.remove(path)
                    for position in path:
                        if not any([position in this_path for this_path in self.next_path]):
                            maze[position[0]][position[1]] = 1
                    self.visited_copy.remove(visited)
            
            self.next_path.extend(new_paths)
            self.visited_copy.extend(new_visited)
        else:
            self.tour.append(self.position)
            self.visited.append(self.position)
            self.position = self.next_path[0].pop(0)
            if not self.next_path[0]:
                self.next_path.remove([])
                self.visited_copy = []
            


            

        

        
        

        
        