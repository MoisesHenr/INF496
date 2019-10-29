# ler a matriz qValue e fazer comparações graficas
import random as random
import numpy as np
import matplotlib.pyplot as plt
import multiplot2 as mplt
import comp as comp

import pylab
pylab.rcParams['figure.figsize'] = (24.0, 8.0) # ajuste do tamanho da imagem gerada
plt.rc('figure', max_open_warning = 0) # ajuste para minimizar uso de memória

def plotComp(est_ac, numRota):
	fig, (ax1, ax2) = plt.subplots(1, 2)

	fig.suptitle('Simulador X Q-Learing --- Rota ' + str(numRota))
	# simulador
	mplt.plotAmb(ax1)
	ax1.legend(loc=0)

	# treinado
	mplt.plotAmb(ax2)
	ax2.legend(loc=0)

	leg = {'AP0':'white', 'AP1':'pink', 'AP2':'red', 'AP3':'green'}

	# sortear 10 rotas aleatorias dentre as possíveis e analisar
	vetComp = comp.compRotasVetor(est_ac, numRota)
	for indv, v in enumerate(vetComp):
		posx = int(v[0])
		posy = int(v[1])
		sim = v[2]
		tr = v[3]
		#print(posx, posy, sim, tr)
		if indv == 0:
			ax1.plot(posx, posy, marker="s", color=leg[sim])
			ax2.plot(posx, posy, marker="s", color=leg[tr])
		elif indv != len(vetComp) - 1:
			posxn = int(vetComp[indv + 1][0])
			posyn = int(vetComp[indv + 1][1])
			if posx > posxn: # aponta para a esquerda
				ax1.plot(posx, posy, marker=4, color=leg[sim])
				ax2.plot(posx, posy, marker=4, color=leg[tr])
			elif posx < posxn: # aponta para a direita
				ax1.plot(posx, posy, marker=5, color=leg[sim])
				ax2.plot(posx, posy, marker=5, color=leg[tr])
			elif posy > posyn: # aponta para baixo
				ax1.plot(posx, posy, marker=7, color=leg[sim])
				ax2.plot(posx, posy, marker=7, color=leg[tr])
			else: # aponta para cima
				ax1.plot(posx, posy, marker=6, color=leg[sim])
				ax2.plot(posx, posy, marker=6, color=leg[tr])
		else:
			ax1.plot(posx, posy, 'bo', color=leg[sim])
			ax2.plot(posx, posy, 'bo', color=leg[tr])

	# resultado
	#plt.show()
	plt.savefig('comparaçõesGraficosRotas/compRota_' + str(numRota) + '.svg')

###################################################################################################

#numRota = int(input("Digite número da rota que deseja comparar: "))

qValue = open("comparaçõesQvalue/qValue_999_R_0_C_0.txt", "r")

est_ac = {}
for linha in qValue:
	linha = linha.split()

	key = linha[0] + " " + linha[1] + " " + linha[2] 
	if linha[0] != linha[1]:
		est_ac[key] = {}
		for i in range(5, len(linha) - 1):
			action = linha[i]
			action = action.split(":")
			actionName = action[0]
			actionValue = float(action[1])
			est_ac[key][actionName] = actionValue

# Print da matriz Q-Value
'''for e in est_ac:
	print(e, ":", est_ac[e])'''

rotas = random.sample(range(0,1000), 50)

for nr in rotas:
	plotComp(est_ac, nr)
