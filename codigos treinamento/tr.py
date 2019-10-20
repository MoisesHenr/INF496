import ref as refinamento
import random as random

def treinamento(numEp, est, est_ac, vRec, vConst):
	for i in range(numEp): # a cada episodio pegar uma das rotas já geradas e fazer as associaçoes dos pontos de acesso disponíveis para aquela posição
		dadosRef = refinamento.ref("../results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "../results2IA/posTime_" + str(i) + ".txt")
		for ind, dado in enumerate(dadosRef):
			if ind != 0 and ind != (len(dadosRef) - 1):
				#print(ind, dado)
				Pb = dadosRef[ind - 1][2] # posição anterior
				P = dado[2] # posição atual
				Pn = dadosRef[ind + 1][2] # próxima posição
				AP = dado[1] # ponto de acesso em que esta conectado
				S = Pb, P, AP # estado atual
				# double q-learning
				
				####################################
				'''# proximo ponto de acesso VERSÃO1
				APn = random.choice(list(est[P]))'''
				####################################
				# proximo ponto de acesso VERSÃO2
				APn = random.choice(list(est[P]))
				rand = random.randint(0, 1)
				if rand == 0:
					listKey = list(est_ac[S].keys())
					listValue = list(est_ac[S].values())
					APn = listKey[listValue.index(max(listValue))] 
				##################################################
				
				Sn = P, Pn, APn
				A = APn
				if P != Pn: # agente não ficou parado
					try:
						MA = max(est_ac[Sn].values())
					except:
						A = 'AP0'
						APn = 'AP0'
						Sn = P, Pn, APn
						MA = max(est_ac[Sn].values())

					R = vRec[0]
					if AP != APn: # mudança de ponto de acesso ou desconecção
						R = vRec[1]
					elif A == 'AP0': # não houve mudança de ponto de acesso mas o agente está desconectado
						R = vRec[2]

					try:
						est_ac[S][A] = est_ac[S][A] + vConst[0] * (R + vConst[1] * MA - est_ac[S][A])
					except: # caso não exista o AP predito
						A = 'AP0'
						est_ac[S][A] = est_ac[S][A] + vConst[0] * (R + vConst[1] * MA - est_ac[S][A])
