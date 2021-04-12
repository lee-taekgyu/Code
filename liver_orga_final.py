import time
import numpy as np

start_time = time.time()

Chromosome = []
for num in range(1,23):
    Chromosome.append('chr' + str(num))
Chromosome.extend(['chrX','chrY'])


for chr in Chromosome:
    cpg_dic = {}
    with open('MD2_pilot.txt' ,'r') as CPG:
        for line in CPG:
            cpg_list = line.strip().split('\t')
            if cpg_list[0] == chr:
                cpg_dic[cpg_list[1]] = ','.join(cpg_list[2:])
                cpg_character = ",".join(cpg_list[2:])
                cpg_character = cpg_character.split(';')
                cpg_character = ','.join(cpg_character)
                cpg_character = cpg_character.split(',')
                cpg_character = cpg_character[0::4] + cpg_character[1::4]
                cpg_character = ','.join(cpg_character)  # c,c,c,uc,uc,uc
                cpg_dic[cpg_list[1]] = cpg_character

    bed_dic = {}
    result = {}
    Total = {}
    with open('ENCFF592AII.bed', 'r' ) as bed:
        for bed_line in bed:
            bed_list = bed_line.strip().split('\t')
            if bed_list[0] == chr:
                Start = int(bed_list[1])
                End = int(bed_list[2])
                for cpg_site in list(cpg_dic.keys()):
                    if Start <= int(cpg_site) <= End:
                        if chr + ' ' + str(Start) +' '+ str(End) not in result:
                            result[chr + ' ' + str(Start) + ' ' + str(End)] = cpg_dic[cpg_site]
                        else:
                            result[chr + ' ' + str(Start) + ' ' + str(End)] += ';'+cpg_dic[cpg_site]
                    else:
                        continue

    with open('result_sum.txt', 'a') as handle:
        for key in result.keys():
            Coverage = result[key].split(',')
            Coverage = ','.join(Coverage)
            Coverage = Coverage.replace(',' ,';')
            Coverage = Coverage.split(';')
            Coverage = list(map(int, Coverage))
            character = str(sum(Coverage[0::6]))+ ' '+ str(sum(Coverage[3::6])) +' ' + str(sum(Coverage[1::6])) +' ' + str(sum(Coverage[4::6])) +' ' + str(sum(Coverage[2::6])) +' ' + str(sum(Coverage[5::6]))
            handle.write(key + '\t' + character + '\n')


    with open('result_mean.txt', 'a') as handle:
        for key in result.keys():
            Coverage = result[key].split(',')
            Coverage = ','.join(Coverage)
            Coverage = Coverage.replace(',' ,';')
            Coverage = Coverage.split(';')
            Coverage = list(map(int, Coverage))
            character = str(np.around(np.mean(Coverage[0::6]),2))+ ' '+ str(np.around(np.mean(Coverage[3::6]),2))+' ' + str(np.around(np.mean(Coverage[1::6]),2)) +' ' + str(np.around(np.mean(Coverage[4::6]),2)) +' ' + str(np.around(np.mean(Coverage[2::6]),2)) +' ' + str(np.around(np.mean(Coverage[5::6]),2))
            handle.write(key + '\t' + character + '\n')


print("Working Time {} sec." .format(round(time.time() - start_time,2)))
