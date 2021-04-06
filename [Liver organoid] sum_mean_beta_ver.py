import time
import numpy as np
import sys

start_time = time.time()
cpg_dic = {}
with open(sys.argv[1] ,'r' ) as CpG:
    for cpg_line in CpG:
        cpg_line = cpg_line.strip()
        cpg_list = cpg_line.split('\t')
        cpg_chr = cpg_list[0]
        cpg_site = cpg_list[1]
        cpg_pos = cpg_list[0] + ' ' + cpg_list[1]
        cpg_cov = []
        for num in range(2,len(cpg_list)):
            cov = cpg_list[num].split(';')[0:2]
            cov = ','.join(cov)
            cpg_cov.append(cov)
        cpg_cov = ', '.join(str(e) for e in cpg_cov)
        cpg_cov = cpg_cov.replace(' ', '')
        cpg_dic[cpg_pos] = cpg_cov


bed_dic = {}
with open(sys.argv[2],'r') as bed:
    for bed_line in bed:
        bed_line = bed_line.strip()
        bed_list = bed_line.split('\t')
        bed_chr = bed_list[0]
        bed_pos = bed_list[0] + ' ' + bed_list[1] + ' ' + bed_list[2]
        bed_dic[bed_pos] = bed_list[6]

Chromosome = []
for num in range(1,23):
    Chromosome.append('chr'+str(num))
Chromosome.extend(['chrX','chrY'])

cpg_check = []
Total_dic = {}

for chromosome in Chromosome:
    cpg_check.clear()
    for bed_key in bed_dic.keys():
        if bed_key in Total_dic:
            next
        else:
            if bed_key.split(' ')[0] == chromosome:
                start_site = bed_key.split(' ')[1]
                end_site = bed_key.split(' ')[2]
                for cpg_key in cpg_dic.keys():
                    if cpg_key.split(' ')[0] == chromosome:
                        cpg = cpg_key.split(' ')[1]
                        if int(start_site) <= int(cpg) <= int(end_site):
                            cpg_check.append(cpg)
                            if cpg in cpg_check:
                                next
                                if bed_key not in Total_dic:
                                    Total_dic[bed_key] = bed_dic[bed_key] + ' ' + cpg_dic[cpg_key]
                                else:
                                    Total_dic[bed_key] += ',' + cpg_dic[cpg_key]

with open(sys.argv[2]+'result.txt','w') as handle:
    for key in Total_dic.keys():
        handle.write(key.split(' ')[0] + '\t' + key.split(' ')[1] + '\t' + key.split(' ')[2] + '\t' + Total_dic[key].split(' ')[0] + '\t' + Total_dic[key].split(' ')[1] + '\n')

with open(sys.argv[2]+'SUM.txt', 'w') as note:
    with open('result.txt','r') as handle:
        for line in handle:
            line = line.strip().split('\t')
            cov = line[4]
            cov = cov.split(',')
            cov = list(map(int,cov))
            character = str(sum(cov[0::6]))+';'+str(sum(cov[1::6])) + ';' + str(sum(cov[2::6]))
            note.write(line[0] + '\t' + line[1] + '\t' +line[2] + '\t' +line[3] + '\t' +character + '\n')


with open(sys.argv[2]+'MEAN.txt', 'w') as note:
    with open('result.txt','r') as handle:
        for line in handle:
            line = line.strip().split('\t')
            cov = line[4]
            cov = cov.split(',')
            cov = list(map(int,cov))
            character = str(np.around(np.mean(cov[0::6]),2))+';'+str(np.around(np.mean(cov[1::6]),2)) + ';' + str(np.around(np.mean(cov[2::6]),2))
            note.write(line[0] + '\t' + line[1] + '\t' +line[2] + '\t' +line[3] + '\t' +character + '\n')

print("Working Time : {} sec".format(time.time()-start_time))
