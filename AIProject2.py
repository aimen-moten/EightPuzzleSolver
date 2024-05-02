from queue import Queue, PriorityQueue
from collections import deque
import heapq


class PuzzleState:
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        if self.state:
            self.blank_index = self.state.index(0)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(self.state))

    def __lt__(self, other):
        return False

    def goal_test(self):
        return self.state == self.goal_state

    @staticmethod
    def possible_moves(i):
        moves = {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4, 6],
            4: [1, 3, 5, 7],
            5: [2, 4, 8],
            6: [3, 7],
            7: [4, 6, 8],
            8: [5, 7]
        }
        return moves[i]

    def successors(self):
        successors = []
        blank_row = self.blank_index // 3
        blank_col = self.blank_index % 3
        for move in self.possible_moves(self.blank_index):
            new_state = self.state[:]
            new_state[self.blank_index], new_state[move] = new_state[move], new_state[self.blank_index]
            successors.append(PuzzleState(new_state, self, move))
        return successors

    def path(self):
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]


def bfs(start):
    frontier = Queue()
    frontier.put(start)
    visited = set()
    visited.add(tuple(start.state))
    nodes_expanded = 0

    while not frontier.empty():
        current_state = frontier.get()
        nodes_expanded += 1

        if current_state.goal_test():
            return current_state.path(), len(current_state.path()) - 1, nodes_expanded

        for successor in current_state.successors():
            if tuple(successor.state) not in visited:
                frontier.put(successor)
                visited.add(tuple(successor.state))

    return None


def manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue
        distance += abs(i // 3 - PuzzleState.goal_state.index(state[i]) // 3) + abs(
            i % 3 - PuzzleState.goal_state.index(state[i]) % 3)
    return distance


def astar(start):
    frontier = []
    heapq.heappush(frontier, (manhattan_distance(start.state), start))
    visited = set()
    nodes_expanded = 0

    while frontier:
        current_cost, current_state = heapq.heappop(frontier)
        nodes_expanded += 1

        if current_state.goal_test():
            return current_state.path(), len(current_state.path()) - 1, nodes_expanded

        visited.add(tuple(current_state.state))

        for successor in current_state.successors():
            if tuple(successor.state) not in visited:
                cost = len(successor.path()) + manhattan_distance(successor.state)
                heapq.heappush(frontier, (cost, successor))

    return None


def print_solution(path, length, nodes_expanded):
    print("Solution:")
    for state in path:
        print_state(state)
    print(f"Length of path: {length}")
    print(f"Nodes expanded: {nodes_expanded}")


def print_state(state):
    for i in range(9):
        if i % 3 == 0:
            print()
        print(state.state[i], end=" ")
    print()


def load_puzzle(filename):
    try:
        with open(filename, 'r') as file:
            puzzle = [int(x) for x in file.read().split()]
            return PuzzleState(puzzle)
    except FileNotFoundError:
        print("File not found.")
        return None


def main():
    print("Welcome to the 8-Puzzle Solver!")
    filename = input("Enter the filename containing the puzzle: ")
    puzzle = load_puzzle(filename)
    if not puzzle:
        return

    print("\nInitial State:")
    print_state(puzzle)

    algorithm = input("Select algorithm (BFS or A*): ").upper()

    if algorithm == "BFS":
        path, length, nodes_expanded = bfs(puzzle)
    elif algorithm == "A*":
        path, length, nodes_expanded = astar(puzzle)
    else:
        print("Invalid algorithm selected.")
        return

    if path:
        print_solution(path, length, nodes_expanded)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
