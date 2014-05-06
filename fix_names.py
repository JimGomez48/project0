import sys
import os


def usage(name):
    print "USAGE: " + str(name) + " <genome dir>"


if len(sys.argv) < 2:
    usage(sys.argv[0])
    sys.exit(1)

current_dir = str(sys.argv[1])

print "Fixing genome names in directory: " + current_dir

for file_name in os.listdir(current_dir):
    print "Fixing " + file_name + "..."
    if file_name.endswith(".txt"):
        with open(current_dir + file_name, 'r') as infile:
            lines = infile.readlines()
            lines[0] = ">genomeH1\n"

        with open(current_dir + file_name, 'w') as outfile:
            outfile.writelines(lines)