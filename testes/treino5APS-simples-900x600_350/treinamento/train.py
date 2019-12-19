"""Versão onde o estado é uma tupla (posição anterior, posição atual, ponto de acesso)""" 
'''900x600'''

import random as random
import ref as refinamento
import tr as treinamento
import comp as comparacao

import multiprocessing as mp

tamX = 90
tamY = 60

def montaQvalue(est):
    # Montagem da matriz Q-Value 
    est_ac_temp = {} # map de estados e ações temporario
    est_ac = {}
    for y in range(tamY+1):
        for x in range(tamX+1):
            if x % 10 == 0:
                posX = x*10
                posY = y*10
                
                # !!!!!!!AQUI HÁ REDUNDÂNCIA POIS NÃO CONSEGUI RESOLVER O PROBLEMA DE ESTADOS FALTANDO, ENTÃO COLOQUEI ESTADOS A MAIS QUE NUNCA SERÃO ACESSADOS!!!!!!! OBS: TENTAR RESOLVER PARA EVITAR GASTO DE MEMÓRIA

                k = '(' + str(posX) + ',' + str(posY) + ',0)' # key base da matriz auxiliar
                kl = '(' + str(posX - 10) + ',' + str(posY) + ',0)' # key left
                kr = '(' + str(posX + 10) + ',' + str(posY) + ',0)' # key right
                ku = '(' + str(posX) + ',' + str(posY - 10) + ',0)' # key up
                kd = '(' + str(posX) + ',' + str(posY + 10) + ',0)' # key down

                est_ac_temp[kl, k] = est[k]
                est_ac_temp[kr, k] = est[k]
                est_ac_temp[ku, k] = est[k]
                est_ac_temp[kd, k] = est[k]

    for y in range(tamY+1):
        for x in range(tamX+1):
            if y % 10 == 0:
                posX = x*10
                posY = y*10
                
                # !!!!!!!AQUI HÁ REDUNDÂNCIA POIS NÃO CONSEGUI RESOLVER O PROBLEMA DE ESTADOS FALTANDO, ENTÃO COLOQUEI ESTADOS A MAIS QUE NUNCA SERÃO ACESSADOS!!!!!!! OBS: TENTAR RESOLVER PARA EVITAR GASTO DE MEMÓRIA

                k = '(' + str(posX) + ',' + str(posY) + ',0)' # key base da matriz auxiliar
                kl = '(' + str(posX - 10) + ',' + str(posY) + ',0)' # key left
                kr = '(' + str(posX + 10) + ',' + str(posY) + ',0)' # key right
                ku = '(' + str(posX) + ',' + str(posY - 10) + ',0)' # key up
                kd = '(' + str(posX) + ',' + str(posY + 10) + ',0)' # key down

                est_ac_temp[kl, k] = est[k]
                est_ac_temp[kr, k] = est[k]
                est_ac_temp[ku, k] = est[k]
                est_ac_temp[kd, k] = est[k]

    for e in est_ac_temp:
        for a in est_ac_temp[e]:
            est_ac[e[0], e[1], a] = {}
            for act in est_ac_temp[e]: # adiciona as ações para cada estado
                est_ac[e[0], e[1], a][act] = 0.0
    
    # ajuste para evitar desconexões desnecessárias
    for e in est_ac:
        est_ac[e]['AP0'] = -0.0001

    return est_ac.copy()

def salvaQvalue(est_ac, iNumEp, indVr, indVc):
    print('##########################################################')
    print('#################SalvamentoQValueIniciado#################')
    print('##########################################################')

    # salvar QValue em arquivo
    arq = open("comparaçõesQvalue/qValue_" + str(iNumEp) + "_R_" + str(indVr) + "_C_" + str(indVc) + ".txt", "w")
    for s in est_ac:
        aux = str(s) + " : { "
        for a in est_ac[s]:
            aux = aux + str(a) + ":" + str(est_ac[s][a]) + " "
        aux += "}\n"
        arq.writelines(aux)

    arq.close()

    print('##########################################################')
    print('################SalvamentoQValueFinalizado################')
    print('##########################################################')

def treina(nRotas, nIter, est, vRec, indVr, vConst, indVc):
    est_ac = montaQvalue(est)
    '''for e in est_ac:
        print(e, ":", est_ac[e])'''

    print('##########################################################')
    print('######################TreinoIniciado######################')
    print('##########################################################')
    for iNumEp in range(nIter):
        if iNumEp < nIter / 10:
            treinamento.treinamento(nRotas, est, est_ac, vRec[indVr], vConst[indVc])
        else:
            treinamento.treinamento(nRotas, est, est_ac, vRec[indVr], vConst[indVc])

        if (iNumEp + 1) % (nIter/10) == 0:
            print("Iteração número:", iNumEp + 1)
        if iNumEp == ((nIter/10)-1) or iNumEp == ((nIter/2)-1) or iNumEp == (nIter-1):
            comparacao.compSimTr(est_ac, nRotas, iNumEp, vRec, indVr, vConst, indVc)
            salvaQvalue(est_ac, iNumEp, indVr, indVc)

    print('##########################################################')
    print('#####################TreinoFinalizado#####################')
    print('##########################################################\n')
    # comparação detalhada de rotas após o treino
    '''for i in rotas:
        comparacao.compRotas(est_ac, i, indVr, indVc)'''	

############################################################################################################################
############################################################################################################################
############################################################################################################################

# Montagem da matriz auxiliar de posições disponíveis
est = {}

for y in range(tamY+1):
    for x in range(tamX+1):
        if x % 10 == 0:
            posX = x*10
            posY = y*10
            est['(' + str(posX) + ',' + str(posY) + ',0)'] = {'AP0'}

for y in range(tamY+1):
    for x in range(tamX+1):
        if y % 10 == 0:
            posX = x*10
            posY = y*10
            est['(' + str(posX) + ',' + str(posY) + ',0)'] = {'AP0'}

# Montagem da matriz auxiliar de pontos de acesso disponíveis por posição
'''nRotas = int(input("Número de rotas: "))
nIter = int(input("Número de iterações: "))
tipo = input("Rodar sequencial ou paralelo (s|p): ")'''
nRotas = 10000
nIter = 1000
tipo = "p"

for i in range(nRotas):
    dadosRef = refinamento.ref("../results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "../results2IA/posTime_" + str(i) + ".txt")

    for dado in dadosRef:
        est[dado[2]].add(dado[1])

'''for e in est:
    print(e, ":", est[e])'''

# variações dos treinamentos
vRec = [[1,-1,-1],[1,-1,-1],[1,-1,-1],[1,-1,-1],[1,-1,-1]]
vConst = [[0.1,0.9]]
#rotas = random.sample(range(0,1000), 3)

for indVr, vr in enumerate(vRec):
    for indVc, vc in enumerate(vConst):
        if tipo == 's':
            treina(nRotas, nIter, est, vRec, indVr, vConst, indVc)
        else:
            p = mp.Process(target=treina, args=(nRotas, nIter, est, vRec, indVr, vConst, indVc,)) 
            p.start()


# Print da matriz Q-Value treinada
#for e in est_ac:
#   print(e, ":", est_ac[e])
