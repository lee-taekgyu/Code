import sys
import re
import argparse

fastq_data = sys.argv[1]
forward_barcode = sys.argv[2]
reverse_barcode = sys.argv[3]
forward_primer = sys.argv[4]
reverse_primer = sys.argv[5]

with open(sys.argv[1], 'r') as handle:
        for line in handle:
                P = re.compile('^[ATCG]{2,}$')
                line = line.strip()
                m = P.match(line)
                if m:
                        line = m.group()
                        if sys.argv[2] in line:
                                forward_seq = line.split(sys.argv[2])
                                forward_seq = forward_seq[1]
                                if forward_seq.startswith(sys.argv[4]):
                                        forward_seq = forward_seq.split(sys.argv[4])
                                        forward_seq = forward_seq[1]

                        elif sys.argv[3] in line:
                                reverse_seq = line.split(sys.argv[3])
                                reverse_seq = reverse_seq[1]
