import os


def reverse_file(fin, fout):
    with open(fin) as source, open(fout, 'w') as dest:
        source.seek(0, os.SEEK_END)
        file_size = source.tell()

        line = ''
        for pos in reversed(range(0, file_size)):
            source.seek(pos)
            char = source.read(1)

            if char != '\n':
                line = char + line
            else:
                dest.write(line + '\n')
                line = ''

            if pos == 0:
                dest.write(line)


reverse_file('lines.txt', 'lines2.txt')
