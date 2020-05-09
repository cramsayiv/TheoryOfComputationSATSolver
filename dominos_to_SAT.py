def make_dominoes(ls_blocked, WIDTH, HEIGHT):
    ls_dominoes = []
    for i in range(WIDTH-1):
        for j in range(HEIGHT):
            if (i, j) not in ls_blocked and (i+1, j) not in ls_blocked:
                ls_dominoes.append((i, j, 'horizontal'))
    for i in range(WIDTH):
        for j in range(HEIGHT-1):
            if (i, j) not in ls_blocked and (i, j+1) not in ls_blocked:
                ls_dominoes.append((i, j, 'vertical'))
    return ls_dominoes


def get_covered_squares(domino):
    ls_covered = []
    x, y, orientation = domino
    if orientation == 'horizontal':
        ls_covered = [(x, y), (x+1, y)]
    elif orientation == 'vertical':
        ls_covered = [(x, y), (x, y+1)]
    return ls_covered


def map_dominoes_and_squares(dominoes):
    dominoes_to_squares = {}
    squares_to_dominoes = {}
    for domino in dominoes:
        dominoes_to_squares[domino] = get_covered_squares(domino)
        for square in dominoes_to_squares[domino]:
            if square not in squares_to_dominoes:
                squares_to_dominoes[square] = [domino]
            else:
                squares_to_dominoes[square].append(domino)
    return dominoes_to_squares, squares_to_dominoes


def solve_sat(str_input):
    ls_input = eval(str_input)
    print(ls_input)
    WIDTH = ls_input[1]
    HEIGHT = ls_input[0]
    blocked = ls_input[2:]
    temp = []
    for element in blocked:
        temp.append((element[0]-1, element[1]-1))
    blocked = temp

    dominoes = make_dominoes(blocked, WIDTH, HEIGHT)
    dominoes_to_squares, squares_to_dominoes = map_dominoes_and_squares(dominoes)

    str_vars = {}
    for d in range(len(dominoes)):
        str_vars[dominoes[d]] = str(d+1)

    num_vars = 0
    vars_used = []

    IS_COVERED = "\n"
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (i, j) not in blocked and (i, j) != (WIDTH, HEIGHT):
                clause = ""
                for domino in squares_to_dominoes[(i, j)]:
                    clause += str_vars[domino]+" "
                    if str_vars[domino] not in vars_used:
                        num_vars += 1
                        vars_used.append(str_vars[domino])
                IS_COVERED += clause+'0\n'

    NO_OVERLAP = ""
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (i, j) not in blocked:
                covering_dominoes = squares_to_dominoes[(i, j)]
                for d1 in range(len(covering_dominoes)):
                    for d2 in range(d1+1, len(covering_dominoes)):
                        NO_OVERLAP += '-'+str_vars[covering_dominoes[d1]]+' -'+str_vars[covering_dominoes[d2]]+' 0\n'
                        if str_vars[covering_dominoes[d1]] not in vars_used:
                            num_vars += 1
                            vars_used.append(str_vars[covering_dominoes[d1]])
                        if str_vars[covering_dominoes[d2]] not in vars_used:
                            num_vars += 1
                            vars_used.append(str_vars[covering_dominoes[d2]])
    IS_COVERED_WITH_NO_OVERLAP = IS_COVERED + NO_OVERLAP
    return "p cnf " + str(num_vars) + " " + str(IS_COVERED_WITH_NO_OVERLAP.count('\n')-1) + IS_COVERED + NO_OVERLAP

print(solve_sat(str(input('Dominoes: '))))
