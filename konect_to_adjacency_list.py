import sys

input_file = open(sys.argv[1], 'r')
output_file = open(sys.argv[2], 'w')

old_lines = input_file.readlines()
old_lines = old_lines[2:]
old_lines = [line.split(' ') for line in old_lines]

node = 'NOT A NODE NAME'

new_lines = []
for old_line in old_lines:
    if old_line[0] == node:
        new_lines[-1] = new_lines[-1] + ' ' + old_line[1]
    else:
        node = old_line[0]
        new_lines.append(old_line[0] + ' ' + old_line[1])

for new_line in new_lines:
    output_file.write(new_line + '\n')

input_file.close()
output_file.close()