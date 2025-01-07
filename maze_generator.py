from entities import MazeGenerator
import random as rd

def maze_generator(size_of_maze: int, random: bool = True) -> list:
    cols = size_of_maze
    rows = size_of_maze

    new_maze = [[0 for _ in range(cols)] for _ in range(rows)]

    generator = MazeGenerator()

    building_maze = True
    while building_maze:

        available_pos = generator.get_available(new_maze)

        if available_pos:
            next_pos = rd.choice(available_pos)
            generator.visited.append(generator.position.copy())
        else:
            generator.set_goal()
            generator.change_to_visited(new_maze)
            next_pos = generator.visited.pop()
        
        generator.move(next_pos,new_maze)

        if not generator.visited:
            building_maze = False
    
    for col in range(cols):
        for row in range(rows):
            if not new_maze[col][row] == 0:
                new_maze[col][row] = 1
    
    return new_maze, generator.goal
