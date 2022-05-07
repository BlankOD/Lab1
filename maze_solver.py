#!/usr/bin/env python3
from fringe import Fringe
from state import State

oppositeDirection = {"NORTH": "SOUTH", "EAST": "WEST", "SOUTH": "NORTH", "WEST": "EAST", "UP": "DOWN", "DOWN": "UP"}

def solve_maze_general(maze, algorithm):
    """
    Finds a path in a given maze with the given algorithm
    :param maze: The maze to solve
    :param algorithm: The desired algorithm to use
    :return: True if solution is found, False otherwise
    """
    # select the right fringe for each algorithm
    if algorithm == "BFS":
        fr = Fringe("FIFO")
    elif algorithm == "DFS":
        fr = Fringe("STACK")
    elif algorithm == "UCS":
        fr = Fringe("PRIORITY")
    elif algorithm == "ASTAR":
        fr = Fringe("ASTAR_PRIORITY")
    elif algorithm == "GREEDY":
        fr = Fringe("HEURISTIC_PRIORITY")
    else:
        print("Algorithm not found/implemented, exit")
        return

    # get the start room, create state with start room and None as parent and put it in fringe
    room = maze.get_room(*maze.get_start())
    state = State(room, None)
    fr.push(0, state)
    while not fr.is_empty():

        # get item from fringe and get the room from that state
        state = fr.pop()
        room = state.get_room()
        if room.is_goal():
            # if room is the goal, print that with the statistics and the path and return
            print("solved")
            fr.print_stats()
            state.print_path()
            state.print_actions()
            print()  # print newline
            maze.print_maze_with_path(state)
            return True
        for d in room.get_connections():
            # loop through every possible move
            if not room.usedConnections[d]:
                new_room, cost = room.make_move(d, state.get_cost())    # Get new room after move and cost to get there
                new_state = State(new_room, state, cost)                # Create new state with new room and old roo
                fr.push(cost, new_state)
                room.usedConnections[d] = True
                new_room.usedConnections[oppositeDirection[d]] = True
            # push the new state

    print("not solved")     # fringe is empty and goal is not found, so maze is not solved
    fr.print_stats()        # print the statistics of the fringe
    return False
