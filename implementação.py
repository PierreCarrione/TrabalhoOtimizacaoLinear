from builtins import print, range, len
import numpy as np
import time


#Variáveis que serão utilizadas para os cálculos
valor = None
peso = None
markedObjects = None
viz = None
capacityMaxI = None
currentCapacityI = None
qtdObjetos = None
qtdMochilas = None
delta = 0
aleatory = 0
neperiano = 2.718
tipoSolucao = None
start = time.time()


#Gerador de instâncias.Função que irá gerar instâncias com valores, pesos e capacidades das mochilas de forma randomica
#Essas instâncias serão salvas no formato txt
def genInstances(qtdObjts , qtdMochilas, rangeMax , nomeArquivoSalvar):
    valor = np.random.randint(1,high=rangeMax, size=(qtdObjts,1))
    peso = np.random.randint(1, high=rangeMax, size=(qtdObjts,1))
    capacityMaxI = np.random.randint(10, high=rangeMax, size=(qtdMochilas,1))
    matriz = np.concatenate((peso, valor), axis=1)
    with open(nomeArquivoSalvar, "w") as arq:
        np.savetxt(arq,np.array([[qtdMochilas],[qtdObjts]]),fmt='%d')
        np.savetxt(arq, capacityMaxI, fmt='%d')
        np.savetxt(arq, matriz, fmt='%d')
        arq.close()

#Leitor de instâncias.Função que irá ler os valores de um arquivo txt
def loadValues(nomeArquivo):
    global valor, peso, markedObjects,capacityMaxI,qtdObjetos,qtdMochilas,currentCapacityI

    with open(nomeArquivo, "r") as arquivo:
        conteudo = arquivo.readlines()

    qtdMochilas = int(conteudo[0])
    qtdObjetos = int(conteudo[1])
    markedObjects = np.zeros((qtdMochilas, qtdObjetos))
    capacityMaxI = np.zeros(qtdMochilas)
    currentCapacityI = np.zeros(qtdMochilas)
    valor = np.zeros(qtdObjetos)
    peso = np.zeros(qtdObjetos)

    for i in range(2,qtdMochilas+2):
        capacityMaxI[i-2] = int(conteudo[i])

    for i in range(2+qtdMochilas,qtdObjetos+2+qtdMochilas):
        aux = conteudo[i].split()
        peso[i-2-qtdMochilas] = int(aux[0])
        valor[i-2-qtdMochilas] = int(aux[1])


#Função que irá gerar uma nova vizinhança(matriz) para cada mochila
def genNewViz(matrizObjMarked):
    rand = np.random.randint(qtdObjetos)
    novoVizinho = matrizObjMarked.copy()
    p = 0

    for y in range(qtdMochilas):
        while p < 3:#Serve para gerar 3 vizinhos aleatorios
            while verifyNeighborhood(novoVizinho, rand, y) is True:
                rand = np.random.randint(qtdObjetos)

            if novoVizinho[y][rand] == 1:
                novoVizinho[y][rand] = 0
            else:
                novoVizinho[y][rand] = 1
                if verifyPesosLinha(novoVizinho[y],y) is False:#Verifica se adicionando o novo item rand não extrapolou o peso máximo da mochila
                    novoVizinho[y][rand] = 0 #Se sim, não adiciona o item
            rand = np.random.randint(qtdObjetos)
            p = p + 1
        p = 0

        if verifyEmpty(novoVizinho,y) is True:#Caso ele gere uma vizinhança nula, irá retornar uma vizinhança com pelo menos 1 objeto
            for i in range(len(novoVizinho[y])):
                if verifyNeighborhood(novoVizinho,i,y) is False:
                    novoVizinho[y][i] = 1
                    break

    return novoVizinho

#Função que verifica se uma determinada mochila está sem item.Retorna true caso a mesma não possua nenhum item.
def verifyEmpty(matrizObjMarked, primeiroIndice):
    sum = 0
    for i in range(len(matrizObjMarked[primeiroIndice])):
        if matrizObjMarked[primeiroIndice][i] == 0:
            sum = sum + 1

    if sum == len(matrizObjMarked[primeiroIndice]):
        return True

    return False

#Função que verifica a vizinhança das outras mochilas.Retorna False caso não tenha vizinho
def verifyNeighborhood(matrizObjMarked, segundoIndice, qualMochila):
    true = 0

    for i in range(len(matrizObjMarked)):
        if i != qualMochila and matrizObjMarked[i][segundoIndice] == 0:
            true = true + 1

    if true == (len(matrizObjMarked) - 1):
        return False

    return True

#Função que calcula a soma de todos os itens em todas as mochilas.
def calcSumValTotal(matrizObjetos):
    sum = 0
    for i in range(len(matrizObjetos)):
        for y in range(len(matrizObjetos[i])):
            if matrizObjetos[i][y] == 1:
                sum = sum + valor[y]
    return sum

#Função que calcula a soma dos pesos dos itens de cada mochila
def calcPesoTotal(matrizObjMarked):
    for i in range(len(matrizObjMarked)):
        for y in range(len(matrizObjMarked[i])):
            if matrizObjMarked[i][y] == 1:
                currentCapacityI[i] = currentCapacityI[i] + peso[y]


#Função que verifica se a soma dos pesos da mochila passada não extrapola a sua capacidade máxima.Retorna False caso extrapole
def verifyPesosLinha(vetor, indiceMochila):
    aux = 0
    for i in range(len(vetor)):
        if vetor[i] == 1:
            aux = aux + peso[i]

    if aux > capacityMaxI[indiceMochila]:
        return False

    return True


loadValues('PC_IT_M75_N375_SL143588.txt')
print("Valores :",valor)
print("Pesos :",peso)
print("Capacidades :",capacityMaxI)

#------------------------------------------ Gerando Solução Inicial ------------------------------------------#
print("Escolha uma das opções para gerar a solução inicial: \n1 - Gulosa\n2 - Custo/Benefício\n3 - Aleatória")
answer = int(input())

if answer == 1:
    tipoSolucao = "Gulosa"
    for i in range(len(markedObjects)):
        for y in range(len(valor)):
            if verifyNeighborhood(markedObjects,y,i) is False:
                if (peso[y] + currentCapacityI[i] <= capacityMaxI[i]):
                    markedObjects[i][y] = 1
                    currentCapacityI[i] = currentCapacityI[i] + peso[y]

elif answer == 2:
    custoBeneficio = valor / peso
    aux = custoBeneficio.copy()
    maior = 0
    indice = -1
    tipoSolucao = "Custo/Benefício"

    for p in range(len(currentCapacityI)):#For que percorre cada mochila
        for i in range(len(markedObjects[p])):#For que percorre todos os custos/beneficios
            for y in range(len(valor)):#For que percorre o valor de todos os itens e retorna o maior custo/benefício dentre eles
                if custoBeneficio[y] > maior:
                    maior = custoBeneficio[y]
                    indice = y

            if verifyNeighborhood(markedObjects, indice, p) is False:
                if peso[indice] + currentCapacityI[p] <= capacityMaxI[p]:
                    markedObjects[p][indice] = 1
                    currentCapacityI[p] = currentCapacityI[p] + peso[indice]
                    aux[indice] = 0
            custoBeneficio[indice] = 0
            maior = 0
        custoBeneficio = aux.copy()#Essa variável auxiliar server para passar para a variável custoBeneficio os valores já marcados
        #Pois durante o fim da execução do for i todos os elementos estarão com 0

else:
    verify = 0
    tipoSolucao = "Aleatória"

    for i in range(len(currentCapacityI)):
        while currentCapacityI[i] <= capacityMaxI[i]:
            rand = np.random.randint(qtdObjetos)

            if verifyNeighborhood(markedObjects, rand, i) is False:
                if peso[rand] + currentCapacityI[i] <= capacityMaxI[i]:
                    markedObjects[i][rand] = 1
                    currentCapacityI[i] = currentCapacityI[i] + peso[rand]
                    verify = verify + 1
                elif aleatory > 4:
                    break
                else:
                    aleatory = aleatory + 1
        #Essa parte me garante que caso os valores aleatórios que foram gerados não retornarem nenhuma solução
        #Essa parte retorna uma solução gulosa
        if verify == 0:
            currentCapacityI[i] = 0
            for y in range(len(valor)):
                if verifyNeighborhood(markedObjects, y, i) is False:
                    if (peso[y] + currentCapacityI[i] <= capacityMaxI[i]):
                        markedObjects[i][y] = 1
                        currentCapacityI[i] = currentCapacityI[i] + peso[y]
        verify = 0
        aleatory = 0
#----------------------------------------------- Fim -----------------------------------------------#


print("Solução inicial", tipoSolucao , ":\n", markedObjects)
print("Valor total dos itens : ", calcSumValTotal(markedObjects))
print("Peso total dos itens : ", currentCapacityI)


#------------------------------------------ Simulated Annealing ------------------------------------------#
tempCorrente = 300
bestSolution = markedObjects.copy()
iterT = 0
alfa = 0.95
SAmax = 15

while tempCorrente > 0.01:
    while iterT < SAmax:#Condição de equilíbrio
        viz = genNewViz(markedObjects)
        new = calcSumValTotal(viz)
        atual = calcSumValTotal(markedObjects)
        delta = new - atual

        if delta > 0:
            markedObjects = viz.copy()
            best = calcSumValTotal(bestSolution)
            if (new - best) > 0:
                bestSolution = viz.copy()
        else:
            if delta < 0:
                x = np.random.randint(1, high=11)/10
                if x < round(neperiano ** (delta/tempCorrente), 1):
                    markedObjects = viz.copy()
        iterT = iterT + 1

    tempCorrente = tempCorrente * alfa #Resfriamento
    iterT = 0
#------------------------------------------ Fim Simulated Annealing ------------------------------------------#


end = time.time()
currentCapacityI.fill(0)#Preencho com zero para recalcular os novos pesos totais de cada mochila
print("Solução obtida pelo simulated annealing : \n",bestSolution)
calcPesoTotal(bestSolution)
print("Valor total dos itens : ", calcSumValTotal(bestSolution))
print("Peso total dos itens : ", currentCapacityI)
print("Tempo de execução : ", end-start)


