
def evaluate(state):
    endstate_list =   ['D','E','M','N','J','K','L','H']
    endstate_values = [ 7,  9,  0,  7,  5,  7,  8,  4]
    for endstate,value in zip(endstate_list,endstate_values):
        if state == endstate:
            return value
    return None

def is_terminal(state):
    end_state_list = ['D','E','M','N','J','K','L','H']
    for end_state in end_state_list:
        if state == end_state:
            return True
    return False


def testeLR(state):
    if state == 'A':
        yield 'B'
        yield 'C'

    if state == 'B':
        yield 'D'
        yield 'E'

    if state == 'C':
        yield 'F'
        yield 'G'
        yield 'H'

    if state == 'F':
        yield 'I'
        yield 'J'

    if state == 'G':
        yield 'K'
        yield 'L'

    if state == 'I':
        yield 'M'
        yield 'N'

def testeRL(state):
    if state == 'A':
        yield 'C'
        yield 'B'

    if state == 'B':
        yield 'E'
        yield 'D'

    if state == 'C':
        yield 'G'
        yield 'F'
        yield 'H'

    if state == 'F':
        yield 'J'
        yield 'I'

    if state == 'G':
        yield 'L'
        yield 'K'

    if state == 'I':
        yield 'N'
        yield 'M'