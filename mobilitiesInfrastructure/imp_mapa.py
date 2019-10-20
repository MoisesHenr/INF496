"""Versão onde o estado é uma tupla (posição, ponto de acesso)"""

import ref as refinamento
import re

est = {}

for y in range(41):
	for x in range(61):
		if x % 10 == 0:
			posX = x*10+20
			posY = y*10+10
			est['(' + str(posX) + ',' + str(posY) + ',0)'] = {'AP0'}

for y in range(41):
	for x in range(61):
		if y % 10 == 0:
			posX = x*10+20
			posY = y*10+10
			est['(' + str(posX) + ',' + str(posY) + ',0)'] = {'AP0'}

n = int(input("Número de rotas: "))
for i in range(n):
	dadosRef = refinamento.ref("results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "results2IA/posTime_" + str(i) + ".txt")

	for dado in dadosRef:
		#print(dado)
		est[dado[2]].add(dado[1])

#for e in est:
#	print(e, ":", est[e])

# montagem do map Q value
est_ac = {} # map de estados e ações
i = 0
for e in est:
	i += 1
	for a in est[e]: # cria os estados 
		est_ac[e, a] = {}
		for act in est[e]: # adiciona as ações para cada estado
			est_ac[e, a][act] = 0.0

print()

########################
# Etapa 1 do treinamento
########################

print('##########################################################')
print('#########################ETAPA1###########################')
print('##########################################################\n')

# FÓRMULA Q-LEARNING
# Q(S,A) = Q(S,A) + ALPHA[R + GAMA * MAX Q(S',a) - Q(S,A)]
for i in range(n):
	dadosRef = refinamento.ref("results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "results2IA/posTime_" + str(i) + ".txt")
	
	for ind, d in enumerate(dadosRef):
		if ind < (len(dadosRef) - 1):
			#print("DADO i:", d, ", DADO i+1:", dadosRef[ind + 1])
			P = d[2] # posição
			Pn = dadosRef[ind + 1][2] # próxima posição
			AP = d[1] # ponto de acesso
			APn = dadosRef[ind +1][1] # próximo ponto de acesso
			S = P, AP 
			Sn = Pn, APn
			A = AP
			R = 1
			if AP != APn: # mudança de ponto de acesso ou desconecção
				R = -2
			elif A == 'AP0': # não houve mudança de ponto de acesso mas o agente está desconectado
				R = -1
			MA = max(est_ac[Sn].values())

			est_ac[S][A] = est_ac[S][A] + 0.5 * (R + 0.5 * MA - est_ac[S][A])

'''for e in est_ac:
	print(e, ":", est_ac[e])'''

########################
# Etapa 2 do treinamento
########################

print('##########################################################')
print('#########################ETAPA2###########################')
print('##########################################################\n')

for i in range(n):
	dadosRef = refinamento.ref("results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "results2IA/posTime_" + str(i) + ".txt")
	
	for ind, d in enumerate(dadosRef):
		if ind < (len(dadosRef) - 1):
			P = d[2] # posição
			Pn = dadosRef[ind + 1][2] # próxima posição
			AP = d[1] # ponto de acesso
			APn = dadosRef[ind +1][1] # próximo ponto de acesso
			S = P, AP 
			Sn = Pn, APn
			A = AP
			R = 1
			if AP != APn: # mudança de ponto de acesso ou desconecção
				R = -2
			elif A == 'AP0': # não houve mudança de ponto de acesso mas o agente está desconectado
				R = -1
			MA = max(est_ac[Sn].values())

			for key in est_ac[(P, 'AP0')]: 
				est_ac[(P, key)][A] = est_ac[(P, key)][A] + 0.5 * (R + 0.5 * MA - est_ac[(P, key)][A])


#for e in est_ac:
#	print(e, ":", est_ac[e])

print('##########################################################')
print('#####################TreinoFinalizado#####################')
print('##########################################################\n')

yMax = 41
xMax = 61

for i in range(4):
	m = []
	for y in range(yMax):
		linha = []
		for x in range(xMax):
			linha.append('-')
		m.append(linha)
	
	# salvar mapa com APs
	for elem in est_ac:
		if elem[1] == 'AP' + str(i):
			elk = list(est_ac[elem].keys())
			elv = list(est_ac[elem].values())
			ind = elv.index(max(elv))
			ap = elk[ind]
			#print(elk, '---', elv, '---', ind, '---', elk[ind])

			#print(elem[0], '---', ap)
			pos = elem[0][1:-1]
			pos = re.split(',', pos)
			x = int((int(pos[0]) - 20) / 10)
			y = int((int(pos[1]) - 10) / 10)
			#print(x, '-', y)

			if ap == 'AP0':
				ap = '0'
			elif ap == 'AP1':
				ap = '1'
			elif ap == 'AP2':
				ap = '2'
			else:
				ap = '3'

			m[y][x] = ap

	for y in range(yMax):
		for x in range(xMax):
			print(m[y][x], end=' ')
		print()

	mapa = open('mapaAP_1000_' + str(i) + '.txt', 'w')
	for y in range(yMax):
		aux = ''
		for x in range(xMax):
			aux += m[y][x] + ' '
		aux +=  '\n'
		mapa.writelines(aux)

	mapa.close()

