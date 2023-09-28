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
        self.idPredAtual = 1
        self.firstPrint = 1

    def embaralhaPuzzle(self):
        self.movimentosRealizados = 0
        self.matriz = [[],[],[]]
        self.idPredAtual = 1
        numeros = [0,1,2,3,4,5,6,7,8]
        for i in range(3):
            for j in range(3):
                elementoSorteado = numeros.pop(random.randint(0, len(numeros)-1))
                self.matriz[i].append(elementoSorteado)

                if elementoSorteado == 0:
                    self.zeroPos = [i, j]

    def verificaTermino(self):
        if (self.matriz == [[1,2,3],[4,5,6],[7,8,0]]):
            return True
        else:
            return False
    
    def posicaoZero(self, matriz):
        xy = ()
        for i in range(3):
            for j in range(3):

                if matriz[i][j] == 0:
                    xy = (i,j)

        return xy

    def verificaAdiciona(self, y, x, yAnt, xAnt, pred, possiveisMovimentos, matriz):
        if (y != yAnt and x != xAnt):
            possiveisMovimentos.append((y, x, pred, self.idPredAtual, matriz))
            self.idPredAtual += 1
        return possiveisMovimentos

    def verificaAdicionaOrdenado(self, y, x, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila):
        movimento = (y,x)
        novaMatriz = self.geraMatrizTempMemoria(matriz, movimento)
        peso = self.distanciaManhatan(novaMatriz)
        pesoAcumulado += peso
        if (y != yAnt and x != xAnt):
            possiveisMovimentos.append((y, x, pred, self.idPredAtual, matriz, pesoAcumulado, peso))
            movimentosFila = self.insereOrdenado(movimentosFila, (y, x, pred, self.idPredAtual, matriz, pesoAcumulado, peso))
            self.idPredAtual += 1
        return possiveisMovimentos, movimentosFila

    def insereOrdenado(self, fila, elemento):
        listaOrdenada = sorted(fila + [elemento], key=lambda x: x[5])
        return listaOrdenada

    def possiveisMovimentos(self, pred=0, matriz=[], movimentoAnterior=()):
        possiveisMovimentos = []
        x = self.zeroPos[1]
        y = self.zeroPos[0]
        xAnt = -1
        yAnt = -1
        if matriz != []:
            xy = self.posicaoZero(matriz)
            x = xy[1]
            y = xy[0]
        else:
            matriz = self.matriz
        
        if movimentoAnterior != () and movimentoAnterior != False:
            xAnt = movimentoAnterior[1]
            yAnt = movimentoAnterior[0]

        if (y == 1):
            possiveisMovimentos = self.verificaAdiciona(y-1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz)
            possiveisMovimentos = self.verificaAdiciona(y+1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz)
        elif (y == 0):
            possiveisMovimentos = self.verificaAdiciona(y+1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz)
        else:
            possiveisMovimentos = self.verificaAdiciona(y-1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz)

        if (x == 1):
            possiveisMovimentos = self.verificaAdiciona(y, x-1, yAnt, xAnt, pred, possiveisMovimentos, matriz)
            possiveisMovimentos = self.verificaAdiciona(y, x+1, yAnt, xAnt, pred, possiveisMovimentos, matriz)
        elif (x == 0):
            possiveisMovimentos = self.verificaAdiciona(y, x+1, yAnt, xAnt, pred, possiveisMovimentos, matriz)
        else:
            possiveisMovimentos = self.verificaAdiciona(y, x-1, yAnt, xAnt, pred, possiveisMovimentos, matriz)

        return possiveisMovimentos
    
    def possiveisMovimentosOrdenados(self, pesoAcumulado = 0, pred=0, matriz=[], movimentoAnterior=(), possiveisMovimentos = [], movimentosFila = []):
        x = self.zeroPos[1]
        y = self.zeroPos[0]
        xAnt = -1
        yAnt = -1
        if matriz != []:
            xy = self.posicaoZero(matriz)
            x = xy[1]
            y = xy[0]
        else:
            matriz = self.matriz
        
        if movimentoAnterior != () and movimentoAnterior != False:
            xAnt = movimentoAnterior[1]
            yAnt = movimentoAnterior[0]

        if (y == 1):
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y-1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y+1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)
        elif (y == 0):
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y+1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)
        else:
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y-1, x, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)

        if (x == 1):
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y, x-1, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y, x+1, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)
        elif (x == 0):
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y, x+1, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)
        else:
            possiveisMovimentos, movimentosFila = self.verificaAdicionaOrdenado(y, x-1, yAnt, xAnt, pred, possiveisMovimentos, matriz, pesoAcumulado, movimentosFila)

        return possiveisMovimentos, movimentosFila

    def moverAleatorio(self):
        possiveisMovimentos = self.possiveisMovimentos()
        movimento = random.choice(possiveisMovimentos)
        self.moveZero(movimento)
    
    def moverManhatan(self):
        possiveisMovimentos = self.possiveisMovimentos()
        tabuleiros = self.calculaDistanciaManhatan(possiveisMovimentos)
        movimento = self.selecionaMovimento(tabuleiros)
        self.moveZero(movimento)
    
    def moverBFS(self):
        possiveisMovimentos = self.possiveisMovimentos()
        movimentosFila = copy.deepcopy(possiveisMovimentos)
        tabuleiros = self.BFS(possiveisMovimentos, movimentosFila)
        movimento = self.selecionaTabuleiro(tabuleiros)
        ordemMovimentos = self.tracaMovimentos(movimento, possiveisMovimentos)
        for mov in ordemMovimentos:
            self.moveZero(mov)
    
    def moverUniformCost(self):
        possiveisMovimentos, movimentosFila = self.possiveisMovimentosOrdenados()
        tabuleiros = self.uniformCost(possiveisMovimentos, movimentosFila)
        movimento = self.selecionaTabuleiro(tabuleiros)
        ordemMovimentos = self.tracaMovimentos(movimento, possiveisMovimentos)
        for mov in ordemMovimentos:
            self.moveZero(mov)
    
    def tracaMovimentos(self, movimento, possiveisMovimentos):
        ordemMovimentos = []
        predZero = False
        while not predZero:
            mov = (movimento[0], movimento[1])
            ordemMovimentos.append(mov)
            pred = movimento[2]
            if pred != 0:
                movimento = self.procuraMovimento(pred, possiveisMovimentos)
            else:
                predZero = True
        ordemMovimentos.reverse()
        return ordemMovimentos
    
    def procuraMovimento(self, idMovimento, possiveisMovimentos):
        for movimento in possiveisMovimentos:
            if idMovimento == movimento[3]:
                return movimento
        return False

    def geraMatrizTemp(self, movimento):
        novaMatriz = copy.deepcopy(self.matriz)

        x = self.zeroPos[1]
        y = self.zeroPos[0]

        novoX = movimento[1]
        novoY = movimento[0]

        novaMatriz[y][x] = novaMatriz[novoY][novoX]
        novaMatriz[novoY][novoX] = 0

        return novaMatriz

    def geraMatrizTempMemoria(self, matriz, movimento):

        xy = self.posicaoZero(matriz)
        x = xy[1]
        y = xy[0]

        novoX = movimento[1]
        novoY = movimento[0]

        matriz[y][x] = matriz[novoY][novoX]
        matriz[novoY][novoX] = 0

        return matriz
    
    def pegaGoal(self, numero):
        matriz = [[1,2,3], [4,5,6], [7,8,0]]
        for i in range(3):
            for j in range(3):
                if matriz[i][j] == numero:
                    return (i, j)
        return False

    def calculaDistanciaManhatan(self, movimentos):
        tabuleiros = []
        for movimento in movimentos:
            matriz = self.geraMatrizTemp(movimento)
            distancia = self.distanciaManhatan(matriz)
            tabuleiro = (matriz, movimento, distancia)
            tabuleiros.append(tabuleiro)
        return tabuleiros

    def distanciaManhatan(self, matriz):
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
        return distancia
    
    def BFS(self, movimentos, movimentosFila):
        tabuleiros = []
        distanciaZero = False
        while movimentosFila != [] and not distanciaZero:
            movimento = movimentosFila.pop(0)
            predecessor = movimento[3]
            if predecessor == 0:
                matriz = self.geraMatrizTemp(movimento)
            else:
                matriz = self.geraMatrizTempMemoria(movimento[4], movimento)
            movimentoAnterior = self.procuraMovimento(predecessor-1, movimentos)
            possiveisMovimentos = self.possiveisMovimentos(predecessor, matriz, movimentoAnterior)
            movimentos.extend(possiveisMovimentos)
            movimentosFila.extend(possiveisMovimentos)
            distancia = self.distanciaManhatan(matriz)
            tabuleiro = (matriz, movimento, distancia)
            tabuleiros.append(tabuleiro)
            if distancia == 0:
                distanciaZero = True

        return tabuleiros

    def uniformCost(self, movimentos, movimentosFila):
        tabuleiros = []
        distanciaZero = False
        while movimentosFila != [] and not distanciaZero:
            movimento = movimentosFila.pop(0)
            predecessor = movimento[3]
            if predecessor == 0:
                matriz = self.geraMatrizTemp(movimento)
            else:
                matriz = self.geraMatrizTempMemoria(movimento[4], movimento)
            movimentoAnterior = self.procuraMovimento(predecessor-1, movimentos)
            distancia = self.distanciaManhatan(matriz)
            pesoAcumulado = movimento[5]
            movimentos, movimentosFila = self.possiveisMovimentosOrdenados(pesoAcumulado, predecessor, matriz, movimentoAnterior, movimentos, movimentosFila)
            tabuleiro = (matriz, movimento, distancia)
            tabuleiros.append(tabuleiro)
            if distancia == 0:
                distanciaZero = True

        return tabuleiros
    
    def selecionaMovimento(self, tabuleiros):
        movimentoSelecionado = ()
        distanciaAtual = 100
        for tabuleiro, movimento, distancia in tabuleiros:
            if distancia < distanciaAtual and movimento != self.movimentoProibido:
                movimentoSelecionado = movimento
                distanciaAtual = distancia
        return movimentoSelecionado

    def selecionaTabuleiro(self, tabuleiros):
        movimentoSelecionado = ()
        for tabuleiro, movimento, distancia in tabuleiros:
            if distancia == 0:
                movimentoSelecionado = movimento
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
    
    def resolverPuzzleBFS(self, numResolucoes):
        for i in range(numResolucoes):
            self.embaralhaPuzzle()
            self.moverBFS()
            self.historicoMovimentos.append(self.movimentosRealizados)
        self.printResultadosFinais()
    
    def resolverPuzzleUC(self, numResolucoes):
        for i in range(numResolucoes):
            self.embaralhaPuzzle()
            self.moverUniformCost()
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
    #puzzle.resolverPuzzleManhatan(1)
    #puzzle.resolverPuzzleAleatorio(1)
    #puzzle.resolverPuzzleBFS(1)
    puzzle.resolverPuzzleUC(1)

if __name__ == "__main__":
    main()