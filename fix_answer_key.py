import sys


def usage(name):
    print "\nUSAGE: python " + str(name) + " <ans_key name> <chrom-num replacement>"
    print "\nEach line in the file not containing a \'>\' symbol will have the first"
    print "character (the chrom-num) replaced with the specified number given in"
    print "the third argument to this program. Fixed files will have the original"
    print "file name with \"fixed_\" prepended."


################################ START OF SCRIPT ####################################
if len(sys.argv) < 3:
    usage(sys.argv[0])
    sys.exit(1)

file_name = str(sys.argv[1])
if not "ans_" in file_name:
    print "Specified file name is not an answer key"
    sys.exit(1)
    
chrom_num = str(sys.argv[2])

read_file = open(file_name, "r")
write_file = open("fixed_" + file_name, "w")

for line in read_file:
    if ">" in line:
        write_file.write(line)
    else:
        write_file.write(chrom_num + line[1:])
