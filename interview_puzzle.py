from itertools import product
from itertools import permutations

res = "y"
while res == "y":

    def swap(a, b):
        a, b = b, a
        return a, b


    def perm(cyc, l):
        n = len(cyc)
        for i in range(1, n):
            j = i
            l[cyc[j] - 1], l[cyc[0] - 1] = l[cyc[0] - 1], l[cyc[j] - 1]

        return l


    def MoveQ(m):
        print("m:", m)


    def ObjQ(obj):
        print("o:", obj)


    def run(obj, m, l):
        for i in range(5):
            print("Iter", i + 1)
            for j in range(5):
                # print(" Sub Iter", j+1)
                if obj[j] == "o":
                    obj = perm(m[i], obj)

                elif obj[j] == "l":
                    l = perm(m[i], l)

                elif obj[j] == "m":
                    m = perm(m[i], m)

            ObjQ(obj)
            MoveQ(m)
            print("l:", l)
            print("")


    def run2(sym):
        for i in range(5):
            print("Iter", i + 1)
            for j in range(5):
                # print(" Sub Iter", j+1)
                if (sym['o'][j] != 'b'):
                    temp = sym['o'][j]
                    sym[temp] = perm(sym['m'][i], sym[temp])

                    # print(obj[j])

            for t in sym:
                print(t, ":", sym[t])
            print()


    def fill(obj):
        while (len(obj) < 5):
            obj.append('b')


    def choose(l, k):
        n = len(l)
        ans = []

        if k == 0:
            return ans

        for j in choose(l, k - 1):
            temp = j
            for el in l:
                temp.append(el)
                ans.append(temp)
                temp = j
        return ans


    l = [1, 2, 3, 4, 5]
    lvl = 1
    obj = ["m", "b", "l", "b", "b"]

    m = []

    '''
    for i in range(5):
        s = input("Enter Cycle: ")
        cyc = []
        for k in s:
            cyc.append(int(k))

        m.append(cyc)
    '''

    print("---A Puzzle By Skandan S---")
    print("This is a game about restoring order")
    print("In each level you will have one or more target arrays (denoted by l) which you will need to unscramble")
    print("You must restore these arrays to the order [1, 2, 3, 4, 5]")
    print(
        "1. A move denotes a permutation action. Moves must always be cyclic permutations. To implement the cycle (3 1 5) you must enter 315 \n 12 34 is not a valid move as it is 2 different cycles whereas 12 and 34 are induvidually valid")
    print("")
    print(
        "2. Lists are objects which are affected by moves. Lists are a set of elements enclosed with '[]' \n For example, [1, 2, 4, 5, 3] is a list. If the move 15 is applied, it becomes [3, 2, 4, 5, 1] \n the target object(s) which we are unscrambling is by definition a list")
    print("")
    print(
        "3. There are 2 types of queues. The move queue (denoted by m) and the list queue (denoted by o) \n In the jth sub-iteration of the ith iteration the move m[i] will be applied on the list o[j]")
    print("")
    print(
        "4. Everything is indexed from 1 to 5. If the list queue has less than 5 elements remaining elements are filled by 'b' which stands for blank")
    print("")
    print(
        "5. The player may only enter swaps or 2 cycles as input moves, identity moves such as 44 are not considered as swaps")
    print("")
    print(
        "6. If you want the list queue to be initialized as ['x', 'y', 'z', 'b', 'b'] Enter xyz (here x, y, z are the names of the lists) \n Note lists must be distinct and only lists that have already been created may be pushed into the queue")
    print("")
    print("7. Move Queue must have 5 non empty elements")
    print("")
    lvl = int(input("Level Select (1-5):"))

    if (lvl == 1):
        print("Level 1: A Little Too Much Space")
        l = [2, 1, 3, 4, 5]
        m = []
        obj = []
        print("l:", l)
        MoveQ(m)

        # Collecting moves
        for i in range(5):
            s = input("Enter Move: ")
            cyc = []
            for k in s:
                cyc.append(int(k))

            m.append(cyc)

        print("")
        print("Since we are trying to permute 'l' you can try entering l")
        s = input("Enter Lists(no spaces):")

        for c in s:
            obj.append(c)

        fill(obj)
        run(obj, m, l)

    elif (lvl == 2):
        print("Level 2: A narrow valley")
        print("In this level you only have control over move 3")
        l = [2, 1, 3, 4, 5]
        m = [[1, 2, 4, 5], [1, 2, 4, 5], [], [1, 2, 4, 5], [1, 2, 4, 5]]
        obj = []
        print("l:", l)
        MoveQ(m)

        s = input("Enter Move: ")
        cyc = []
        for k in s:
            cyc.append(int(k))

        m[2] = cyc

        s = input("Enter Lists(no spaces):")

        for c in s:
            obj.append(c)

        fill(obj)
        run(obj, m, l)

    elif (lvl == 3):
        print("Level 3: A moving suspicion?")
        print("In this level you only have control over moves 1 and 4")
        l = [5, 4, 2, 3, 1]
        m = [[], [2, 3, 4], [2, 3, 4], [], [2, 3, 4]]
        obj = []
        print("l:", l)
        MoveQ(m)

        # Collecting moves
        for i in range(2):
            s = input("Enter Move: ")
            cyc = []
            for k in s:
                cyc.append(int(k))

            m[3 * i] = cyc

        s = input("Enter Lists(no spaces):")

        for c in s:
            obj.append(c)

        fill(obj)
        run(obj, m, l)

    elif (lvl == 4):
        print("Level 4: Who cares about parity?")
        l = [3, 4, 1, 2, 5]
        m = []
        obj = []
        print("l:", l)
        MoveQ(m)

        for i in range(5):
            s = input("Enter Move: ")
            cyc = []
            for k in s:
                cyc.append(int(k))

            m.append(cyc)

        print("")
        s = input("Enter Lists(no spaces):")

        for c in s:
            obj.append(c)

        fill(obj)
        run(obj, m, l)


    elif (lvl == 5):
        print("Level 5: Entangled")
        print("In this level both the lists x and y need to have their order restored")
        m = []
        obj = []
        x = [2, 3, 4, 5, 1]
        y = [3, 4, 5, 1, 2]

        print("x:", x)
        print("y:", y)
        print("b: []")
        MoveQ(m)

        for i in range(5):
            s = input("Enter Move: ")
            cyc = []
            for k in s:
                cyc.append(int(k))

            m.append(cyc)

        print("")
        s = input("Enter Lists(no spaces):")

        for c in s:
            obj.append(c)

        fill(obj)

        print("x:", x)
        print("y:", y)
        MoveQ(m)
        ObjQ(obj)

        sym = {'x': x, 'y': y, 'o': obj, 'm': m}

        run2(sym)

    res = input("Restart? (y/n)")