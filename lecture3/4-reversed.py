import os
import tempfile


def reverse_file(fin, fout):
    with open(fin, 'rt') as source, open(fout, 'wt') as dest:
        tmp = tempfile.TemporaryFile(mode='r+t')

        file_size = os.path.getsize('lines.txt')
        for i in range(file_size // 1024, -1, -1):
            source.seek(i * 1024)
            data = source.read(1024)
            tmp.write(data[::-1])

        tmp.seek(0)

        for line in tmp:
            dest.write(line[::-1])


reverse_file('lines.txt', 'lines2.txt')
