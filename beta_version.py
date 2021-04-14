import sys
import time
import numpy as np

Chromosome = []
for num in range(1,23):
	Chromosome.append('chr'+str(num))
Chromosome.extend(['chrX','chrY'])

data_files = sys.argv[3:]  #Bismark CpG report file

for chromosome in Chromosome:
	data_dict = {}
	Pos_dict = {}
	for dfile in data_files:
		dopen = open(dfile)
		dlines = dopen.readlines()
		dopen.close()
		data_dict[dfile] = {}
		for dline in dlines:
			line = dline.strip().split('\t')
			Chr = line[0]
			Position = line[1]
			if line[3] == '0':
				Description = line[3], line[4], str(0), line[6]
			else:
				Description = line[3], line[4], str(round(int(line[3]) / (int(line[3]) + int(line[4]))*100,2)), line[6]
			Description = ';'.join(Description)
			if Chr == chromosome:
				data_dict[dfile][Position] = Description

	with open(sys.argv[3], 'r') as handle0:  #input bed file
		for line0 in handle0:
			line0 = line0.strip().split('\t')
			Chr0 = line0[0]
			Position0 = line0[1]
			if Chr0 == chromosome:
				Pos_dict[Position0] = Chr0
				
	key_Position = data_dict[dfile].keys()
	key_Chromosome = Pos_dict.keys()	

	with open(sys.argv[1]+'_total_merge.txt', 'a') as handle1:   # name 
		for key in key_Position:
			handle1.write(Pos_dict[key] + '\t' + key)
			for dfile in data_files:
				handle1.write('\t' + data_dict[dfile][key])
			handle1.write('\n')

	data_dict.clear()
	Pos_dict.clear()

with open(sys.argv[1] + '_filtered_merge.txt' , 'w') as final_merge:
	with open(sys.argv[1]+'_total_merge.txt', 'r') as merge_file:
		for line in merge_file:
			line_list = line.strip().split('\t')
			Tissue = line_list[2].split(';')
			Early = line_list[3].split(';')
			Late = line_list[4].split(';')
			if int(Tissue[0]) + int(Tissue[1]) < 10 or int(Early[0]) + int(Early[1]) < 10 or int(Late[0]) + int(Late[1]) < 10:
				continue
			else:
				final_merge.write('\t'.join(line_list) + '\n')

for chr in Chromosome:
    cpg_dic = {}
    with open(sys.argv[1]+'_filtered_merge.txt' ,'r') as CPG:          #filtered file
        for line in CPG:
            cpg_list = line.strip().split('\t')
            if cpg_list[0] == chr:
                cpg_dic[cpg_list[1]] = ','.join(cpg_list[2:])
                cpg_character = ",".join(cpg_list[2:])
                cpg_character = cpg_character.split(';')
                cpg_character = ','.join(cpg_character)
                cpg_character = cpg_character.split(',')
                cpg_character = cpg_character[0::4] + cpg_character[1::4]
                cpg_character = ','.join(cpg_character) 
                cpg_dic[cpg_list[1]] = cpg_character

    bed_dic = {}
    result = {}
    Total = {}
    with open(sys.argv[2], 'r' ) as bed:       #reference CpG bed file
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

    with open(sys.argv[1] + '_sum.txt', 'a') as handle:             #Sum value
        for key in result.keys():
            Coverage = result[key].split(',')
            Coverage = ','.join(Coverage)
            Coverage = Coverage.replace(',' ,';')
            Coverage = Coverage.split(';')
            Coverage = list(map(int, Coverage))
            character = str(sum(Coverage[0::6]))+ ' '+ str(sum(Coverage[3::6])) +' ' + str(sum(Coverage[1::6])) +' ' + str(sum(Coverage[4::6])) +' ' + str(sum(Coverage[2::6])) +' ' + str(sum(Coverage[5::6]))
            handle.write(key + '\t' + character + '\n')

    with open(sys.argv[1] + '_mean.txt', 'a') as handle:            #Mean value
        for key in result.keys():
            Coverage = result[key].split(',')
            Coverage = ','.join(Coverage)
            Coverage = Coverage.replace(',' ,';')
            Coverage = Coverage.split(';')
            Coverage = list(map(int, Coverage))
            character = str(np.around(np.mean(Coverage[0::6]),2))+ ' '+ str(np.around(np.mean(Coverage[3::6]),2))+' ' + str(np.around(np.mean(Coverage[1::6]),2)) +' ' + str(np.around(np.mean(Coverage[4::6]),2)) +' ' + str(np.around(np.mean(Coverage[2::6]),2)) +' ' + str(np.around(np.mean(Coverage[5::6]),2))
            handle.write(key + '\t' + character + '\n')

print("Working Time {} sec." .format(round(time.time() - start_time,2)))
