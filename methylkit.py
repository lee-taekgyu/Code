import sys


chromosome = ['1','10','11','12','13','14','15','16','17','18','19','2','20','21','3','4','5','6','7','8','9','X','Y']

for i in chromosome:
        CpG_Site = []
        range_start = []
        range_end = []
        with open(sys.argv[1], 'r') as handle1:
                for line in handle1:
                        if line.startswith("bin"):
                                continue
                        line = line.strip().split('\t')
                        Chr = line[1]
                        if Chr == i:
                                Start = line[2]
                                CpG_Site.append(Start)

        with open(sys.argv[2], 'r') as handle2:
                for line2 in handle2:
                        if line2.startswith('chr'):
                                continue
                        line2 = line2.strip().split('\t')
                        Chr2 = line2[0]
                        if Chr2 == i:
                                Start2 = line2[1]
                                End2 = line2[2]
                                range_start.append(Start2)
                                range_end.append(End2)



        range_start = list(map(int,range_start))
        range_end = list(map(int,range_end))
        CpG_Site = list(map(int, CpG_Site))


        for i,j in zip(range_start, range_end):
                Sum = 0
                for k in CpG_Site:
                        if k in range(i,j):
                                Sum += 1
                print(Sum)
