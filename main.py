import testes_minmax
import minmax

#teste = jogoDaVelha.jogoDaVelha()

#minmax.alphabeta(teste.tabuleiro, 5, float('-inf'), float('inf'), teste.av_fun, teste.childIter, 1, True)

state = 'A'

_, bestmove = minmax.fs_alphabeta(state,20,float('-inf'),float('inf'),
                                        testes_minmax.evaluate,
                                        testes_minmax.testeRL,
                                        testes_minmax.is_terminal,0,True)

print(bestmove)
print()
_, bestmove = minmax.fs_alphabeta(state,20,float('-inf'),float('inf'),
                                        testes_minmax.evaluate,
                                        testes_minmax.testeLR,
                                        testes_minmax.is_terminal,0,True)

print(bestmove)
