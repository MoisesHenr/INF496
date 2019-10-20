import os
import re

# gerar malhas
r = input("Deseja gerar novas rotas (s/n): ")

if r == "s" or r == "S":
	os.system("g++ malhas.cpp -o malhas")
	os.system("./malhas")

# atualizar .ini
a = input("Deseja atualizar *.ini (s/n): ")

if a == "s" or a == "S":
	ini = open("omnetpp.ini", "r")

	numRoutes = int(input("Informe o numero de rotas existentes: "))
	temp = ""

	for linha in ini:
		aux = re.split("[\. ]", linha) #split usando expressao regular para "." e " "
		if "turtleScript" in aux: #fazer esse passo em um for para que tenha xmldoc() o suficiente para cada malha
			temp += '*.host1.mobility.turtleScript = ${count='
			for i in range(numRoutes):
				if (i < numRoutes - 1):
					temp += 'xmldoc("routes/' + str(i) + '.xml"),'
				else:
					temp += 'xmldoc("routes/' + str(i) + '.xml")'
			temp += '}\n'
		else:
			temp += linha

	ini.close()

	#print(temp)

	ini = open("omnetpp.ini", "w")
	ini.writelines(temp)
	ini.close()

	print("Atualização do *.ini terminada")

# rodar simulação
s = input("Deseja rodar as simulações (s/n): ")

if s == "s" or s == "S":
	numS = int(input("Rodar simulações referentes a quantas malhas: "))

	for i in range(numS):
		# identificação do tempo limite de cada malha
		xml = open("routes/" + str(i) + ".xml", "r")
		linhas = xml.readlines()
		timeLimit = (len(linhas) - 3) * 10

		print("timeLimit: %d", timeLimit)

		# comando para simulação
		os.system("opp_run -m -n ../../../src:../../../examples:../../../tutorials:../.. --image-path=../../../images -l ../../../src/INET omnetpp.ini -u Cmdenv -c Infrastructure -r " + str(i) + " --sim-time-limit=" + str(timeLimit) + "s")

		# mudar o nome de saida para saida_i onde i é o indice
		os.rename("/home/moises/inet4/showcases/wireless/mobilitiesInfrastructure/results2IA/posTime.txt", "/home/moises/inet4/showcases/wireless/mobilitiesInfrastructure/results2IA/posTime_" + str(i) + ".txt")

		# passar script para "limpar" o arquivo *.tlog
		tlog = open("results/Infrastructure-" + str(i) + ".tlog", "r")
		temp = open("results2IA/assocResp_probeReq-" + str(i) + ".txt", "w") # substituir esse arquivo por um vetor

		for linha in tlog:
			aux = linha.split()
			if "AssocResp-OK" in aux:
				#if "InfrastructureShowcaseA.host1.wlan[0].radio" in aux:
				temp.writelines(linha)
			if "ProbeReq" in aux:
				if "InfrastructureShowcaseA.host1.wlan[0].radio" in aux:
					temp.writelines(linha)

		tlog.close()
		temp.close()

		# deletando *.tlog
		os.remove("results/Infrastructure-" + str(i) + ".tlog")
		os.remove("results/Infrastructure-count=xmldoc(#22routes#2f" + str(i) + ".xml#22)-#0.sca")
		os.remove("results/Infrastructure-count=xmldoc(#22routes#2f" + str(i) + ".xml#22)-#0.vci")
		os.remove("results/Infrastructure-count=xmldoc(#22routes#2f" + str(i) + ".xml#22)-#0.vec")

		# resumo dos probReq
		temp = open("results2IA/assocResp_probeReq-" + str(i) + ".txt", "r")
		tlog_r = open("results2IA/assocResp_probeReq-" + str(i) + "_r.txt", "w")

		linhas = temp.readlines()

		tlog_r.writelines(linhas[0])

		for i in range(1,len(linhas) - 1):
			aux1 = linhas[i-1]
			aux1 = aux1.split()
			aux2 = linhas[i]
			aux2 = aux2.split()
			aux3 = linhas[i+1]

			if "ProbeReq" in aux1 and "ProbeReq" in aux2 and "ProbeReq" in aux3:
				pass
			else:
				tlog_r.writelines(linhas[i])

		tlog_r.writelines(linhas[len(linhas) - 1])

	print("Simulações terminadas")
