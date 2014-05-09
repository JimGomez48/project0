__author__ = 'Joseph'

def Test_Answer_Key(ref_genome_file, prv_genome_file, ans_key, allowable_range, verbose=False):
    ref_genome = ''
    prv_genome = ''
    bad_ans_list = []
    with open(ref_genome_file, 'r') as gen_file:
        for line in gen_file:
            if line.startswith('>'):
                pass
            else:
                line = line.rstrip('\n')
                ref_genome += line
    with open(prv_genome_file, 'r') as gen_file:
        for line in gen_file:
            if line.startswith('>'):
                pass
            else:
                line = line.rstrip('\n')
                prv_genome += line
    with open(ans_key, 'r') as answers:
        type = ''
        for line in answers:
            if line.startswith('>'):
                line = line.strip()
                type = line[1:-1]
            else:
                if type == 'SNP':
                    ref_allele = line.split(',')[1]
                    prv_allele = line.split(',')[2]
                    posn = int(line.split(',')[3])
                    found = False
                    for i in range(posn - allowable_range, posn + allowable_range + 1):
                        if ref_genome[i] == ref_allele:
                            temp_ref = ref_genome[i-allowable_range:i] + prv_allele + \
                                       ref_genome[i+1:i+allowable_range+1]
                            for j in range(posn - allowable_range, posn + allowable_range):
                                temp_prv = prv_genome[j-allowable_range:j+allowable_range+1]
                                if temp_prv[:allowable_range] == temp_ref[:allowable_range] or \
                                                temp_prv[allowable_range:] == temp_ref[allowable_range:]:
                                    found = True
                    if not found:
                        bad_ans_list.append(str(posn) + ',SNP Error,' + ref_allele + ',' + prv_allele)
                elif type == 'COPY':
                    seq = line.split(',')[1]
                    for posn in line.split(',')[2:]:
                        posn = int(posn.rstrip())
                        found = False
                        for i in range(posn - allowable_range, posn + allowable_range + 1):
                            if prv_genome[i:i+len(seq)] == seq:
                                found = True
                        if not found:
                            bad_ans_list.append(str(posn) + ',COPY Error,' + seq)
                elif type == 'INVERSION':
                    seq = line.split(',')[1]
                    posn = int(line.split(',')[2])
                    found = False
                    for i in range(posn - allowable_range, posn + allowable_range + 1):
                        if prv_genome[i:i+len(seq)] == seq[::-1]:
                            found = True
                    inverted = True
                    for i in range(posn - allowable_range, posn + allowable_range + 1):
                        if prv_genome[i:i+len(seq)] == seq:
                            inverted = False
                    if not inverted:
                        bad_ans_list.append(str(posn) + ',INV not inverted,' + seq)
                    elif not found:
                        bad_ans_list.append(str(posn) + ',INV not found,' + seq)
                elif type == 'DELETE':
                    seq = line.split(',')[1]
                    posn = int(line.split(',')[2])
                    found = False
                    for i in range(posn - allowable_range, posn + allowable_range + 1):
                        for j in range(posn - allowable_range, posn + allowable_range + 1):
                            if ref_genome[i:i+len(seq)] == seq:
                                temp_ref = ref_genome[i-2:i] + ref_genome[i+len(seq):i+len(seq)+3]
                                if prv_genome[j-2:j+3] == temp_ref:
                                    found = True
                    if not found:
                        bad_ans_list.append(str(posn) + ',DELETE error,' + seq)
                elif type == 'INSERT':
                    seq = line.split(',')[1]
                    posn = int(line.split(',')[2])
                    found = False
                    for i in range(posn - allowable_range, posn + allowable_range + 1):
                        if prv_genome[i:i+len(seq)] == seq:
                            found = True
                    if not found:
                        bad_ans_list.append(str(posn) + ',INSERT error,' + seq)
                elif type == 'STR':
                    seq = line.split(',')[1].rstrip()
                    repeat = int(line.split(',')[2]) / 2
                    seq = seq * repeat
                    posn = int(line.split(',')[3])
                    prv_found = False
                    ref_found = False
                    for i in range(posn - 20, posn + 21):
                        if prv_genome[i:i+len(seq)] == seq:
                            prv_found = True
                    for i in range(posn - 20, posn + 21):
                        if ref_genome[i:i+len(seq)] == seq:
                            ref_found = True
                    if not prv_found:
                        bad_ans_list.append(str(posn) + ',STR not found,' + seq)
                    #if ref_found:
                    #    bad_ans_list.append(str(posn) + ',STR not modified,' + seq)
    if len(bad_ans_list) > 0:
        for line in bad_ans_list:
            if not verbose:
                print line
            else:
                posn = int(line.split(',')[0])
                print 'Error: ' + line.rstrip()
                print 'Genomes surrounding position: ' + str(posn)
                print '%11s' % 'V'
                print 'Ref: ' + ref_genome[posn - 10:posn + 100]
                print 'Prv: ' + prv_genome[posn - 10:posn + 100]
                print '\n'

def main():
    prv_file_path = 'private_STRtest.txt'
    ref_file_path = 'ref_STRtest.txt'
    ans_file_path = 'ans_STRtest.txt'
    Test_Answer_Key(ref_file_path, prv_file_path, ans_file_path, 5, True)

if __name__ == '__main__':
    main()