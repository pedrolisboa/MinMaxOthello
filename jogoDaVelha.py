import numpy as np

def childIter(node, symbol,n):
    i = 0
    import copy
    while i <= node.size - 1:
        print("\t" * n, "Iter", n, i, node)
        if node[i] == 0:
            child = copy.copy(node)
            child[i] = symbol
            i += 1
            yield child
        i += 1


def av_fun(node):
    p1 = np.array([1 if (casa == 2) else 0 for casa in node])
    p2 = np.array([1 if (casa == 1) else 0 for casa in node])

    fp1 = sum(p1[0:2]) + sum(p1[3:5]) + sum(p1[6:8]) + \
          sum(p1[[0, 3, 6]]) + sum(p1[[1, 4, 7]]) + sum(p1[[2, 5, 8]])
    fp2 = sum(p2[0:2]) + sum(p2[3:5]) + sum(p2[6:8]) + \
          sum(p2[[0, 3, 6]]) + sum(p2[[1, 4, 7]]) + sum(p2[[2, 5, 8]])

    return fp1 - fp2

class jogoDaVelha:
    tabuleiro = np.zeros(9)

    def play(self,i,j,symbol):
        self.tabuleiro[(i-1) + (j-1)] = symbol

    def jprint(self):
        for i in range(0,len(self.tabuleiro)):
            print(self.tabuleiro[i],end=' ')
            if (i+1) % 3 == 0 and i != 0: print()


