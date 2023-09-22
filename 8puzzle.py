import random
import numpy as np
import copy

class Puzzle:
    def __init__(self):
        self.matriz = []
        self.zeroPos = []
        self.movimentosRealizados = 0
        self.historicoMovimentos = []
        self.movimentoProibido = ()

    def embaralhaPuzzle(self):
        self.movimentosRealizados = 0
        self.matriz = [[],[],[]]
        numeros = [0,1,2,3,4,5,6,7,8]
        for i in range(3):
            for j in range(3):
                elementoSorteado = numeros.pop(random.randint(0, len(numeros)-1))
                self.matriz[i].append(elementoSorteado)

                if elementoSorteado == 0:
                    self.zeroPos = [i, j]

        print(self.matriz)

    def verificaTermino(self):
        if (self.matriz == [[1,2,3],[4,5,6],[7,8,0]]):
            return True
        else:
            return False

    def possiveisMovimentos(self):
        possiveisMovimentos = []
        x = self.zeroPos[1]
        y = self.zeroPos[0]

        if (y == 1):
            possiveisMovimentos.append((y-1, x))
            possiveisMovimentos.append((y+1, x))
        elif (y == 0):
            possiveisMovimentos.append((y+1, x))
        else:
            possiveisMovimentos.append((y-1, x))

        if (x == 1):
            possiveisMovimentos.append((y, x-1))
            possiveisMovimentos.append((y, x+1))
        elif (x == 0):
            possiveisMovimentos.append((y, x+1))
        else:
            possiveisMovimentos.append((y, x-1))

        return possiveisMovimentos

    def moverAleatorio(self):
        possiveisMovimentos = self.possiveisMovimentos()
        movimento = random.choice(possiveisMovimentos)
        self.moveZero(movimento)
    
    def moverManhatan(self):
        possiveisMovimentos = self.possiveisMovimentos()
        tabuleiros = self.calculaDistanciaManhatan(possiveisMovimentos)
        movimento = self.selecionaMovimento(tabuleiros)
        self.moveZero(movimento)

    def geraMatrizTemp(self, movimento):
        novaMatriz = copy.deepcopy(self.matriz)

        x = self.zeroPos[1]
        y = self.zeroPos[0]

        novoX = movimento[1]
        novoY = movimento[0]

        novaMatriz[y][x] = novaMatriz[novoY][novoX]
        novaMatriz[novoY][novoX] = 0

        return novaMatriz
    
    def pegaGoal(self, numero):
        matriz = [[1,2,3], [4,5,6], [7,8,0]]
        for i in range(3):
            for j in range(3):
                if matriz[i][j] == numero:
                    return (i, j)
        return False

    def calculaDistanciaManhatan(self, movimentos):
        tabuleiros = []
        novaMatriz = []
        for movimento in movimentos:
            matriz = self.geraMatrizTemp(movimento)
            distancia = 0
            for i in range(3):
                for j in range(3):
                    valor = matriz[i][j]
                    y = i
                    x = j
                    goal = self.pegaGoal(valor)
                    goalY = goal[0]
                    goalX = goal[1]
                    distancia += abs(y - goalY) + abs(x - goalX)
            tabuleiro = (matriz, movimento, distancia)
            tabuleiros.append(tabuleiro)
        return tabuleiros
    
    def selecionaMovimento(self, tabuleiros):
        movimentoSelecionado = ()
        distanciaAtual = 100
        for tabuleiro, movimento, distancia in tabuleiros:
            if distancia < distanciaAtual and movimento != self.movimentoProibido:
                movimentoSelecionado = movimento
                distanciaAtual = distancia
        return movimentoSelecionado

    def moveZero(self, novaPosicao):
        x = self.zeroPos[1]
        y = self.zeroPos[0]

        novoX = novaPosicao[1]
        novoY = novaPosicao[0]

        self.matriz[y][x] = self.matriz[novoY][novoX]
        self.matriz[novoY][novoX] = 0

        self.zeroPos = [novoY, novoX]

        self.movimentosRealizados += 1

        self.movimentoProibido = (y, x)

        print(self.matriz)

    def resolverPuzzleManhatan(self, numResolucoes):
        for i in range(numResolucoes):
            self.embaralhaPuzzle()
            while not self.verificaTermino():
                self.moverManhatan()
            self.historicoMovimentos.append(self.movimentosRealizados)
        self.printResultadosFinais()

    def resolverPuzzleAleatorio(self, numResolucoes):
        for i in range(numResolucoes):
            self.embaralhaPuzzle()
            while not self.verificaTermino():
                self.moverAleatorio()
            self.historicoMovimentos.append(self.movimentosRealizados)
        self.printResultadosFinais()

    def printResultadosFinais(self):
        media = np.mean(self.historicoMovimentos)
        maiorNumMovimentos = max(self.historicoMovimentos)
        menorNumMovimentos = min(self.historicoMovimentos)

        print("Quantidade de resoluções: {}".format(len(self.historicoMovimentos)))
        print("Quantidade de movimentos por resolução: {}".format(self.historicoMovimentos))
        print("Média de movimentos realizados: {}".format(media))
        print("Número de movimentos no pior desempenho: {}".format(maiorNumMovimentos))
        print("Número de movimentos no melhor desempenho: {}".format(menorNumMovimentos))

def main():
    puzzle = Puzzle()
    puzzle.resolverPuzzleManhatan(1)
    #puzzle.resolverPuzzleAleatorio(1)

if __name__ == "__main__":
    main()