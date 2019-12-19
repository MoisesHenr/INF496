import ref as refinamento

#####################################################################################################################

def compSimTr_old(est_ac, numEp, num, vRec, indR, vConst, indC):
	print('##########################################################')
	print('##############Comparação_' + str(num) + '_R_' + str(indR) + '_C_' + str(indC) + '_Iniciada##############')
	print('##########################################################')

	tempMedioSim = {'AP0':[0, 0], 'AP1':[0, 0], 'AP2':[0, 0], 'AP3':[0, 0]} # estrutura para armazenar qual o tempo médio de cada AP --- primeiro elemento armazena o tempo total e o segundo armazena quantos intervalos ouveram
	tempMedioTr = {'AP0':[0, 0], 'AP1':[0, 0], 'AP2':[0, 0], 'AP3':[0, 0]} # estrutura para armazenar qual o tempo médio de cada AP --- primeiro elemento armazena o tempo total e o segundo armazena quantos intervalos ouveram

	for i in range(numEp):
		dadosRef = refinamento.ref("../results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "../results2IA/posTime_" + str(i) + ".txt")

		tempListAp = []

		apIniSim = 'AP0'
		listApSim = []
		apTr = 'AP0'
		for ind, d in enumerate(dadosRef): # iteração em cada elemento do dado para ver no map treinado onde se conectar e qual proximo estado
			if dadosRef[ind-1][2] != d[2]:
				# simulador
				if ind == 0:
					apIniSim = d[1]
					listApSim.append(d)
				if ind != 0:
					# simulador
					apAtualSim = d[1]
					if apAtualSim != apIniSim:
						listApSim.append(dadosRef[ind-1])
						listApSim.append(d)
						apIniSim = d[1]
					# treinado
					try:
						el = est_ac[(dadosRef[ind-1][2], d[2], apTr)]
					except:
						apTr = 'AP0'
						el = est_ac[(dadosRef[ind-1][2], d[2], apTr)]

					elk = list(el.keys())
					elv = list(el.values())
					indM = elv.index(max(elv))
					apTr = elk[indM]

					tempListAp.append([d[0], apTr, dadosRef[ind-1][2], d[2]])
				# simulador
				if ind == (len(dadosRef) - 1):
					listApSim.append(d)

		# simulador
		for iL, l in enumerate(listApSim):
			if iL % 2 == 0 and iL != (len(listApSim)-1):
				t = int(listApSim[iL+1][0]) - int(l[0]) + 1 # tempo a frente - tempo atual
				tempMedioSim[l[1]][0] += t
				tempMedioSim[l[1]][1] += 1

		# treinado
		apIniTr = 'AP0'
		listApTr = []
		for ind, d in enumerate(tempListAp): # iteração em cada elemento do dado para ver no map treinado onde se conectar e qual proximo estado
			if ind == 1:
				apIniTr = d[1]
				listApTr.append(d)
			if ind != 0 and ind != 1:
				apAtual = d[1]
				if apAtual != apIniTr:
					listApTr.append(tempListAp[ind-1])
					listApTr.append(d)
					apIniTr = d[1]
			if ind == (len(tempListAp) - 1):
				listApTr.append(d)

		for iL, l in enumerate(listApTr):
			if iL % 2 == 0 and iL != (len(listApTr)-1):
				t = int(listApTr[iL+1][0]) - int(l[0]) + 1 # tempo a frente - tempo atual
				tempMedioTr[l[1]][0] += t
				tempMedioTr[l[1]][1] += 1

	# salvar arquivo de comparação
	comp = open('comparaçõesTempo/comp_tempApSimTr_' + str(num) + '_R_' + str(indR) + '_C_' + str(indC) + '.txt', 'w')
	aux = 'Tempo médio conectado em cada AP: ' + str(vRec[indR]) + str(vConst[indC]) + '\n\n'
	comp.writelines(aux)
	comp.writelines('AP --- [tempo conectado, número de intervalos]\n')
	comp.writelines('AP --- tempo médio\n\n')
	interSim = 0
	interTr = 0

	# simulador --- treinado
	mediaPTM = 0
	mediaPI = 0
	comp.writelines('Resultados simulador --- Resultados treino:\n')
	for t in tempMedioSim:
		aux = str(t) + ' --- ' + str(tempMedioSim[t]) + ' --- ' + str(tempMedioTr[t]) + '\n'
		comp.writelines(aux)

		# calculo das porcentagens
		strPorc = ''
		# calculo da porcentagem do tempo médio
		tmSim = 0
		if tempMedioSim[t][1] != 0:
			tmSim = tempMedioSim[t][0]/tempMedioSim[t][1]
		tmTr = 0
		if tempMedioTr[t][1] != 0:
			tmTr = tempMedioTr[t][0]/tempMedioTr[t][1]
		porcTm = 0
		if tmSim != 0:
			porcTm = (tmTr/tmSim)*100

		if t == 'AP0':
			if porcTm >= 100:
				strPorc = 'Piorou Tm ' + str(porcTm-100) + '%'
			else:
				strPorc = 'Melhorou Tm ' + str(100-porcTm) + '%'
		else:
			if porcTm >= 100:
				mediaPTM = mediaPTM + porcTm - 100 # calculo da média de melhora do tempo médio conectado
				strPorc = 'Melhorou Tm ' + str(porcTm-100) + '%'
			else:
				mediaPTM = mediaPTM - (100 - porcTm) # calculo da média de melhora do tempo médio conectado
				strPorc = 'Piorou Tm ' + str(100-porcTm) + '%'

		# calculo da porcentagem do número de intervalos
		iSim = tempMedioSim[t][1]
		iTr = tempMedioTr[t][1]
		porcI = 0
		if iSim != 0:
			porcI = (iTr/iSim)*100

		if t == 'AP0':
			if porcI >= 100:
				strPorc += ' --- Melhorou Ni ' + str(porcI-100) + '%'
			else:
				strPorc += ' --- Piorou Ni ' + str(100-porcI) + '%'
		else:
			if porcI >= 100:
				mediaPI = mediaPI - (porcI - 100) # calculo da média de melhora dos intervalos conectados
				strPorc += ' --- Piorou Ni ' + str(porcI-100) + '%'
			else:
				mediaPI = mediaPI + 100 - porcI # calculo da média de melhora dos intervalos conectados
				strPorc += ' --- Melhorou Ni ' + str(100-porcI) + '%'

		aux = str(t) + ' --- ' + str(tmSim) + ' --- ' + str(tmTr) + ' --- ' + strPorc + '\n'
		comp.writelines(aux)
		if t != 'AP0':
			interSim += iSim
			interTr += iTr
	comp.writelines('\n')
	aux = 'Número de intervalos conectado: ' + str(interSim) + ' --- ' + str(interTr) + '\n\n'
	comp.writelines(aux)
	aux = 'Porcentagem tempos médios: ' + str(mediaPTM) + '%\n'
	comp.writelines(aux)
	aux = 'Porcentagem intervalos: ' + str(mediaPI) + '%\n'
	comp.writelines(aux)

	comp.close()

	print('##########################################################')
	print('##############Comparação' + str(num) + '_R_' + str(indR) + '_C_' + str(indC) + '_Finalizada##############')
	print('##########################################################\n')

def compSimTr(est_ac, numEp, num, vRec, indR, vConst, indC):
	print('##########################################################')
	print('##############Comparação_' + str(num) + '_R_' + str(indR) + '_C_' + str(indC) + '_Iniciada##############')
	print('##########################################################')

	tempMedioSim = {'AP0':[0, 0], 'AP1':[0, 0], 'AP2':[0, 0], 'AP3':[0, 0]} # estrutura para armazenar qual o tempo médio de cada AP --- primeiro elemento armazena o tempo total e o segundo armazena quantos intervalos houveram
	tempMedioTr = {'AP0':[0, 0], 'AP1':[0, 0], 'AP2':[0, 0], 'AP3':[0, 0]} # estrutura para armazenar qual o tempo médio de cada AP --- primeiro elemento armazena o tempo total e o segundo armazena quantos intervalos houveram

	apAtual = 'AP0' # treinamento inicia desconectado
	for i in range(numEp):
		dadosRef = refinamento.ref("../results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "../results2IA/posTime_" + str(i) + ".txt")
		for indiceDado, d in enumerate(dadosRef):
			keyDadosRef = d[1]
			if indiceDado == 0:
				tempMedioSim[keyDadosRef][1] += 1
				#tempMedioTr[apAtual][1] += 1
			if indiceDado != 0 and d[2] != dadosRef[indiceDado-1][2]: # caso em que ele fica parado
				#print(d)
				tempMedioSim[keyDadosRef][0] += 1 # armazenamento de tempo total do simulador
				if d[1] != dadosRef[indiceDado-1][1]: # houve troca de AP no simulador
					tempMedioSim[keyDadosRef][1] += 1

				Pb = dadosRef[indiceDado-1][2] # posição anterior
				P = d[2] # posição atual
				AP = d[1] # ponto de acesso em que esta conectado
				S = Pb, P, AP # estado atual

				listaAcoes = est_ac[S] # extrai a lista de ações disponíveis para o estado
				listaAcoesk = list(listaAcoes.keys())
				listaAcoesv = list(listaAcoes.values())
				indM = listaAcoesv.index(max(listaAcoesv))
				apTr = listaAcoesk[indM]
				
				tempMedioTr[apTr][0] += 1
				if apAtual != apTr: # houve troca de AP no treinamento
					apAtual = apTr # atualiza qual é o AP atual
					tempMedioTr[apTr][1] += 1
	
	'''for tms in tempMedioSim:
		print(tms, "--- sim:", tempMedioSim[tms])
	for tmt in tempMedioTr:
		print(tmt, "--- tr:", tempMedioTr[tmt])'''

	# salvar os dados em arquivo
	comp = open('comparaçõesTempo/comp_tempApSimTr_' + str(num) + '_R_' + str(indR) + '_C_' + str(indC) + '.txt', 'w')
	aux = 'Tempo médio conectado em cada AP: ' + str(vRec[indR]) + str(vConst[indC]) + '\n\n'
	comp.writelines(aux)
	comp.writelines('[tempo conectado, número de intervalos]\n')
	comp.writelines('AP --- Simulador --- Treinamento --- Porcentagem Simulador --- Porcentagem Treinamento\n')
	comp.writelines('AP --- tempo médio\n\n')

	tmTotalSim = 0
	tmAPSim = 0
	niAPSim = 0
	tmTotalTr = 0
	tmAPTr = 0
	niAPTr = 0
	for keyComp in tempMedioSim: # chaves são iguais para ambos dicionários
		# simulador
		tempoConSim = tempMedioSim[keyComp][0] # tempo conectado 
		numInterSim = tempMedioSim[keyComp][1] # número de intervalos
		tmSim = 0
		if numInterSim != 0:
			tmSim = tempoConSim/numInterSim

		# treinamento
		tempoConTr = tempMedioTr[keyComp][0] # tempo conectado
		numInterTr = tempMedioTr[keyComp][1] # número de intervalos
		tmTr = 0
		if numInterTr != 0:
			tmTr = tempoConTr/numInterTr
		
		# escrita dos dados por AP
		porcAPtm = 0
		if keyComp == 'AP0': # para o AP0 a melhora é o oposto dos demais APs
			if tmTr != 0:
				porcAPtm = (tmSim-tmTr)*100/tmTr
		else:
			if tmSim != 0:
				porcAPtm = (tmTr-tmSim)*100/tmSim
			
		porcAPni = 0
		if numInterTr != 0:
			porcAPni = (numInterSim-numInterTr)*100/numInterTr
		
		aux = str(keyComp) + " --- [" + str(tempoConSim) + ", " + str(numInterSim) + "] --- [" + str(tempoConTr) + ", " + str(numInterTr) + "] --- " + str(porcAPtm) + " --- " + str(porcAPni) + "\n"
		comp.writelines(aux)
		aux = str(keyComp) + " --- " + str(tmSim) + " --- " + str(tmTr) + "\n"
		comp.writelines(aux)

		# verificação dos tempos e intervalos
		tmTotalSim += tempoConSim
		tmTotalTr += tempoConTr

		if keyComp != 'AP0':
			tmAPSim += tempoConSim
			tmAPTr += tempoConTr
			niAPSim += numInterSim
			niAPTr += numInterTr

	aux = "\nTempo total --- " + str(tmTotalSim) + " --- " + str(tmTotalTr) + "\n"
	comp.writelines(aux)
	aux = "Tempo total conectado --- " + str(tmAPSim) + " --- " + str(tmAPTr) + "\n"
	comp.writelines(aux)
	aux = "Total de intervalos conectados --- " + str(niAPSim) + " --- " + str(niAPTr) + "\n"
	comp.writelines(aux)

	porcTotaltm = (tmAPTr-tmAPSim)*100/tmAPSim
	aux = "\nPorcentagem de melhora total do tempo conectado --- " + str(porcTotaltm) + "\n"
	comp.writelines(aux)
	porcTotalni = (niAPSim-niAPTr)*100/niAPTr
	aux = "Porcentagem de melhora total do número de intervalos --- " + str(porcTotalni) + "\n"
	comp.writelines(aux)

	porcMediatmSim = tmAPSim/niAPSim
	porcMediatmTr = tmAPTr/niAPTr
	aux = "\nPorcentagem de melhora do tempo médio conectado --- " + str((porcMediatmTr-porcMediatmSim)*100/porcMediatmSim) + "\n"
	comp.writelines(aux)

	comp.close()

	print('##########################################################')
	print('##############Comparação' + str(num) + '_R_' + str(indR) + '_C_' + str(indC) + '_Finalizada##############')
	print('##########################################################\n')

#####################################################################################################################

def compRotas(est_ac, rota, indR, indC):
	dadosRef = refinamento.ref("../results2IA/assocResp_probeReq-" + str(rota) + "_r.txt", "../results2IA/posTime_" + str(rota) + ".txt")

	# salvar arquivo de comparação
	comp = open('comparaçõesRotas/comp_' + str(rota) + '_R_' + str(indR) + '_C_' + str(indC) + '.txt', 'w')

	ap = 'AP0'
	for ind, d in enumerate(dadosRef): # iteração em cada elemento do dado para ver no map treinado onde se conectar e qual proximo estado
		if ind != 0:
			try:
				el = est_ac[(dadosRef[ind-1][2], d[2], ap)]
			except:
				ap = 'AP0'
				el = est_ac[(dadosRef[ind-1][2], d[2], ap)]

			elk = list(el.keys())
			elv = list(el.values())
			indM = elv.index(max(elv))
			#print(d[2], '-', ap, '-', el, elk[ind])
			ap = elk[indM]

			#print(d[0], 'pos:', d[2], 'AP sim:', d[1], 'AP tr:', ap)
			aux = d[0] + " " + dadosRef[ind-1][2] + " " + d[2] + ' --- AP sim: ' + d[1] + ' --- AP tr: ' + ap + '\n'
			comp.writelines(aux)

	comp.close()

#####################################################################################################################

def compRotasVetor(est_ac, rota):
	dadosRef = refinamento.ref("../results2IA/assocResp_probeReq-" + str(rota) + "_r.txt", "../results2IA/posTime_" + str(rota) + ".txt")

	# em vez de escrever e salvar --- gerar um vetor com as comparações
	vComp = []

	ap = 'AP0'
	for ind, d in enumerate(dadosRef): # iteração em cada elemento do dado para ver no map treinado onde se conectar e qual proximo estado
		if ind != 0 and dadosRef[ind-1][2] != d[2]:
		#if dadosRef[ind-1][2] != d[2]:
			# ajustes para conseguir consultar a est_ac lida de arquivo
			try:
				key = "('" + dadosRef[ind-1][2] + "', '" + d[2] + "', '" + ap + "')"
				el = est_ac[key]
			except:
				ap = 'AP0'
				key = "('" + dadosRef[ind-1][2] + "', '" + d[2] + "', '" + ap + "')"
				el = est_ac[key]

			elk = list(el.keys())
			elv = list(el.values())
			indM = elv.index(max(elv))
			#print(d[2], '-', ap, '-', el, elk[ind])
			ap = elk[indM]

			# (posiçãoX, posiçãoY, ap simulador, ap treino)
			pos = d[2].split(',')
			posX = pos[0][1:]
			posY = pos[1]
			vComp.append((posX, posY, d[1], ap))

	return vComp
