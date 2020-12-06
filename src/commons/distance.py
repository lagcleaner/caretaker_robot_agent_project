

def distance(coord1, coord2, extended=False):
    '''
        extended: `False` Manhatan Distance, `True` Diagonal Distance     
    '''
    applier = max if extended else sum
    return applier(abs(x1 - x2) for x1, x2 in zip(coord1, coord2))
