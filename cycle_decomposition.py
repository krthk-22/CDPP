# Using this code we want to determine the cycles present in final permutation

# This function applies the move on the permutation and gives us the new permutation after that move
# here we are using the fact that the move (a,b,c,d,e..) can be written as product of 2-cycles as (a b)(a c)(a d)(a e)..

def permute(move, permutation):
    n = len(move)
    for i in range(0, n):
        j = i
        permutation[move[j]-1], permutation[move[0]-1] = permutation[move[0]-1], permutation[move[j]-1]

    return permutation


# We are going to find the cycles in the permutation
def find_cycles(permutation):
    perm1 = permutation[:]
    n = len(perm1)
    cycles = []
    for i in range(0, n):
        if perm1[i] != 0:
            cycle = []
            current = i
            while perm1[current] != 0:
                cycle.insert(0, perm1[current])
                temp = current
                current = perm1[current]-1
                perm1[temp] = 0
            cycles.append(cycle)
    return cycles


# Getting the permutation
element = int(input('Enter the permutation element-wise: '))
permutation = []
while element != -1:
    permutation.append(element)
    element = int(input('Enter the next element: '))

# Collecting the moves
moves = []
m = input('Enter the move and after last move enter -1: ')
while m != '-1':
    move = []
    for k in m:
        move.append(int(k))
    moves.append(move)
    m = input('Enter the move: ')

for move in moves:
    permute(move, permutation)
cycles = find_cycles(permutation)
print('The final permutation is :', permutation)
print('The cycles in the final permutation are :', cycles)
