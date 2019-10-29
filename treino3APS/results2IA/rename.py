import os

for i in range(1000):
    os.rename('./assocResp_probeReq-' + str(8000+i) + '_r.txt', './assocResp_probeReq-' + str(i) + '_r.txt')
    os.rename('./posTime_' + str(8000+i) + '.txt', './posTime_' + str(i) + '.txt')