import sys

Chromosome = []
for num in range(1,23):
	Chromosome.append('chr'+str(num))
Chromosome.extend(['chrX','chrY'])

CpG_site = []

for chromosome in Chromosome:
	with open(sys.argv[2], 'r') as diff:
		for diff_line in diff:
			if diff_line.startswith('""'):
				continue
			diff_line = diff_line.strip().split('"')
			diff_chr = diff_line[3]
			if diff_chr == chromosome:
				diff_CpG = diff_line[4].split(',')[1]
				CpG_site.append(diff_CpG)

	Position_dic = {}
	with open (sys.argv[1], 'r') as gtf:
		for gtf_line in gtf:
			gtf_line = gtf_line.strip().split('\t')
			gtf_chr = gtf_line[0]
			if gtf_chr == chromosome:
				gtf_local = gtf_line[2]
				gtf_start = gtf_line[3]
				gtf_end = gtf_line[4]
				gtf_Description = gtf_line[8].split(';')[0]
				gtf_Gene_name = gtf_Description.split('"')[1]
				Position_dic[gtf_local + " " + gtf_start] = {}
				Position_dic[gtf_local + " " + gtf_start] = gtf_start, gtf_end, gtf_Gene_name 

	for key in Position_dic.keys():
		start = Position_dic[key][0]
		end = Position_dic[key][1]
		for number in range(len(CpG_site)):
			if int(start) <= int(CpG_site[number]) <= int(end):
				print(Position_dic[key][2] + '\t' + key.split(" ")[0])
