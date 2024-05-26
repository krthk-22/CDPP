import copy

# declaring the solved state
solved_state = ('W0', 'W1', 'W2', 'W3', 'B0', 'B1', 'B2', 'B3', 'Y0', 'Y1', 'Y2', 'Y3', 'G0', 'G1', 'G2', 'G3',
                'O0', 'O1', 'O2', 'O3', 'R0', 'R1', 'R2', 'R3')


def get_state():
    state = []
    for i in range(0, 24):
        c = input()
        state.append(c)
    return tuple(state)


def permute(move, state):
    n = len(move)
    for i in range(0, n):
        j = i
        state[move[j]], state[move[0]] = state[move[0]], state[move[j]]

    return state


# moves that can be applied on the cube
moves = [[[0, 4, 11, 15], [3, 7, 8, 12], [20, 23, 22, 21]], [[1, 5, 10, 14], [2, 6, 9, 13], [16, 19, 18, 17]],
         [[0, 16, 9, 21], [1, 17, 8, 20], [12, 13, 14, 15]], [[3, 19, 10, 22], [2, 18, 11, 23], [4, 5, 6, 7]],
         [[4, 19, 13, 20], [5, 16, 12, 23], [0, 3, 2, 1]], [[7, 18, 14, 21], [6, 17, 15, 22], [11, 10, 8, 9]]]


def get_neighbours(state):
    neighbours = []
    for i in range(0, 6):
        state1 = list(copy.deepcopy(state))
        state2 = list(copy.deepcopy(state))
        for move in moves[i]:
            permute(move, state1)
            permute(move[::-1], state2)
        neighbours.append(tuple(state1))
        neighbours.append(tuple(state2))
    return neighbours


def bfs(current_state):
    queue = [current_state]
    visited = {current_state}
    no_of_moves = 0

    while queue:
        state = queue.pop(0)
        if state == solved_state:
            print(no_of_moves)
            return state
        else:
            no_of_moves += 1
            if state not in visited:
                visited.add(tuple(state))
            for i in range(0, 12):
                neighbour = get_neighbours(state)[i]
                if tuple(neighbour) not in visited:
                    queue.append(neighbour)


print(bfs(('Y3', 'W1', 'W2', 'Y0', 'G3', 'B1', 'B2', 'G0', 'W3', 'Y1', 'Y2', 'W0', 'B3', 'G1', 'G2', 'B0', 'O0', 'O1',
           'O2', 'O3', 'R2', 'R3', 'R0', 'R1')))
