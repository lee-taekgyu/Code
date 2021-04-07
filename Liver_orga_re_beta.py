import sys
import time
import numpy as np

start_time = time.time()

Chromosome = []
for num in range(1,23):
	Chromosome.append('chr'+str(num))
Chromosome.extend(['chrX','chrY'])

cpg_dic = {}
cpg_sort_dic = {}

with open(sys.argv[1], 'r') as CpG:
	for cpg_line in CpG:
		cpg_line = cpg_line.strip()
		cpg_list = cpg_line.split('\t')
		cpg_chr = cpg_list[0]
		cpg_site = cpg_list[1]
		cpg_cov = cpg_list[2]
		cpg_pos = cpg_list[0] +'    '+cpg_list[1] +'    '+cpg_list[2]
		cpg_sort_dic[cpg_site] = cpg_cov
		cpg_dic[cpg_chr] = cpg_sort_dic



bed_dic = {}
bed_sort_dic = {}

with open(sys.argv[2], 'r') as bed:
	for bed_line in bed:
		bed_line = bed_line.strip()
		bed_list = bed_line.split('\t')
		bed_chr = bed_list[0]
		bed_pos = bed_list[1] +'    '+ bed_list[2]
		bed_enrich = bed_list[6]
		bed_sort_dic[bed_pos] = bed_enrich
		bed_dic[cpg_chr] = bed_sort_dic


result = {}
for chromosome in Chromosome:
	if chromosome == 'chr1':
		for bed_key in bed_dic.keys():
			Position = list(bed_dic[bed_key])
			Range = Position[0]
			start = Range.split('    ')[0]
			end = Range.split('    ')[1]
			for cpg_key in cpg_dic.keys():
				CpG_site = list(cpg_dic[cpg_key])[0]
				if int(start) <= int(CpG_site) <= int(end):
					result[bed_key] = cpg_dic[cpg_key][CpG_site]


ㅣ




print("Working Time, {} min".format((time.time()-start_time)/60))
