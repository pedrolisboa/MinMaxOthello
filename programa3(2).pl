tabuleiro(5).

/*Preenche uma lista com todas as casas do tabuleiro. Durante o jogo, as casas descobertas sao removidas da lista.
O jogador ira encerrar a partida quando a lista estiver vazia.*/
preencher_lista_tabuleiro(N, R) :-
	bagof(P, pair(N, P), R).

pair(N, [X,Y]) :-
	between(1, N, X),
	between(1, N, Y).

escolher_jogada([L,C],Lista) :- 
    write('01'),
	length(Lista,N),
	write('02'),
	Z is N+1,
	write('03'),
	randset(1,Z,[J|_]), nth0(J,Lista,[L,C]),
	write('04'),
	consult('programa2.pl'),
	posicao(L,C),
	write('05').
escolher_jogada(_,_):-write('06').



percorrer_fronteira([],[],_,_).

/*Caso nao conclusivo*/ 
percorrer_fronteira([[Casa,Valor] | Fronteira],Lista_Tabuleiro, Minas, NovasMinas) :-
	write('50-2'),nl,
	vizinhos(Casa,Vizinhanca), /*Casas vizinhas*/
	write('51-2'),nl,
	diferenca(Vizinhanca,Lista_Tabuleiro,Vizinhanca_Coberta), /*Casas vizinhas ainda nao abertas*/
	write('52-2'),nl,
	diferenca(Vizinhanca,Minas, Vizinhanca_Coberta_Desconhecida), /*Remove casas que conhecidamente tem minas*/
	write('52-2,5'),nl,
	length(Vizinhanca_Coberta_Desconhecida,K),			 /*Numero da casa é igual ao numero de casas vizinhas*/
	write('53-2'),nl,
	Valor <> K,						 /*inconclusivo*/
	write('54-2'),nl,
	percorrer_fronteira(Fronteira,Nova_Lista, Minas,RecNovasMinas),
	write('55-2'),nl.

/*Caso mina encontrada*/ 
percorrer_fronteira([[Casa,Valor] | Fronteira],Lista_Tabuleiro, Minas, NovasMinas) :-
	write('50-1-1'),nl,
	vizinhos(Casa,Vizinhanca), /*Casas vizinhas*/
	write('151'),nl,
	diferenca(Vizinhanca,Lista_Tabuleiro,Vizinhanca_Coberta), /*Casas vizinhas ainda nao abertas*/
	write('152'),nl,
	diferenca(Vizinhanca,Minas, Vizinhanca_Coberta_Desconhecida), /*Remove casas que conhecidamente tem minas*/
	write('153'),nl,
	length(Vizinhanca_Coberta_Desconhecida,K),			 /*Numero da casa é igual ao numero de casas vizinhas*/
	write('154'),nl,
	write(Valor),nl,
	write(K),nl,
	Valor = K;						 
	write('155'),nl,
	percorrer_fronteira(Fronteira,Nova_Lista, Minas,RecNovasMinas),
	write('156'),nl,
	append(Vizinhanca_Coberta,RecNovasMinas,NovasMinas).			 /*Adiciona as novas minas descobertas na lista de minas*/

/*Novas regras para determinação de minas podem ser inseridas no formato deste predicado*/





jogar([],_).
jogar(Lista,Minas) :-
	write('0'),
	escolher_jogada(Jogada,Lista),
	write('1'),
	consult('jogo.pl'),
	write('2'),
	findall([L,C],valor(L,C,R),Casas_Descobertas), /*Remover casas descobertas da lista do tabuleiro*/
	write('3'),
	diferenca(Lista, Casas_Descobertas, Nova_Lista),
	write('4'),
	findall([[L,C],R],valor(L,C,R),Fronteira ), /*Fronteira Formato: [[X,Y],R]*/
	write('5'),
	percorrer_fronteira(Fronteira,Nova_Lista,Minas,MinasEncontradas),
	write('6'),
	append(MinasEncontradas,Minas,Nova_Lista_Minas),
	write('7'),
	diferenca(Nova_Lista,MinasEncontradas,Nova_Lista_Sem_Minas),
	write('8'),
	jogar(Nova_Lista_Sem_Minas,Nova_Lista_Minas).
	

mainAI:-	tabuleiro(N),preencher_lista_tabuleiro(N,Lista),
	  		jogar(Lista,[]).

:-mainAI.