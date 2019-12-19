def dadosProbeAssoc(nomeArq, dados):
	arq = open(nomeArq, "r")

	for i, linha in enumerate(arq):
		linha = linha.split()
		#print(i, "---", linha)

		# extração dos dados: [em quem está conectado, 
		#					   posição temporal]
		aux = []
		if "ProbeReq" in linha:
			aux.append("AP0") # desconectado
			aux.append(linha[7]) # posição temporal
			aux.append(linha[8] + linha[9] + linha[10]) #posição espacial
		else:
			temp = linha[1]
			temp = temp.split(".")
			aux.append(temp[1]) # numero do AP
			linha = arq.readline()
			linha = linha.split()
			aux.append(linha[7]) # posição temporal
			aux.append(linha[8] + linha[9] + linha[10]) #posição espacial

		#print(i, "---", aux)
		dados.append(aux)

	arq.close()

def compPos(nomeArq, dados, dadosPA): # complemento dos dados de posição
	arq = open(nomeArq, "r")

	for i, linha in enumerate(arq):
		if i != 0:
			linha = linha.split()
			#print(linha)

			# ajuste por cada segundo [posição temporal, em quem está conectado, posição espacial]
			aux = []

			# extração do ponto de acesso em que o host esta conectado, dado a maior proximidade temporal nos 2 arrays
			ind = 0
			for j in range(len(dadosPA)):
				temp = float(dadosPA[j][1]) - float(linha[0])
				if temp < 0:
					ind = j
				else:
					break

			aux.append(linha[0])
			aux.append(dadosPA[ind][0])
			aux.append(linha[2] + linha[3] + linha[4])

			dados.append(aux)

	arq.close()

####################################################################

def ref(assocRespFile, posTimeFile):
	# dados de ProbeReq e de AssocResp-OK
	dadosPA = []
	dadosProbeAssoc(assocRespFile, dadosPA)
	# dados de posição associadoss com o AP em que está conectado
	dadosPosPA = []
	compPos(posTimeFile, dadosPosPA, dadosPA)

	return dadosPosPA

####################################################################
