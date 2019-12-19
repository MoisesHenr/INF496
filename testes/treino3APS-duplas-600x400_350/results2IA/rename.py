import os

for i in range(1000):
    os.rename('./assocResp_probeReq-' + str(i) + '_r.txt', './assocResp_probeReq-' + str(i+1000) + '_r.txt')
    os.rename('./posTime_' + str(i) + '.txt', './posTime_' + str(i+1000) + '.txt')
