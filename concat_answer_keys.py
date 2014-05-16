__author__ = 'james'

import sys
import os


def usage():
    print "USAGE: python " + str(sys.argv[0]) + "<ans-key dir> <genome ID>"


def get_num_from_file(file_name):
    """
    Returns the number portion in the name of the file as an int. Useful for sorting
    files by number. Assumes file of the format
    "<type>_genome<difficulty letter><chr num>.txt"
    """
    basename = file_name.partition('.')[0]
    first, second = basename.split('_')
    num = second.replace("genome", '')
    num = num[1:]
    return int(num)

def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    ans_sections = [
        ">COPY:",
        ">INVERSION:",
        ">STR:",
        ">INSERT:",
        ">DELETE:",
        ">SNP:"
    ]
    dir = str(sys.argv[1])
    genome_id = str(sys.argv[2])
    answer_key_name = "ans_" + genome_id + ".txt"

    print "Starting answer key..."
    with open(answer_key_name, 'w') as answer_file:
        answer_file.write(">" + genome_id + "\n")
        for ans_section in ans_sections:
            answer_file.write(ans_section + "\n")
            file_list = os.listdir(dir)
            file_list.sort(key=get_num_from_file)
            for file_name in file_list:
                try:
                    with open(dir + file_name, 'r') as current_file:
                        section_found = False
                        for line in current_file:
                            if section_found:
                                if '>' in line:
                                    break
                                answer_file.write(line)
                            else:
                                if '>' in line:
                                    if ans_section in line:
                                        section_found = True
                                        print "Writing " + \
                                              ans_section[1:len(ans_section) - 1] + \
                                              " from " + file_name
                except IOError as e:
                    sys.stderr.write("Error opening \'" + file_name + "\'\n")
                    sys.stderr.write(e.strerror + "\n")
                    sys.exit(1)

    print "DONE"


if __name__ == '__main__':
    main()