def lines_count(file_name):
    with open(file_name, 'rt') as f:
        return sum(1 for line in f) - 1


def merge_files(file1, file2):
    length1 = lines_count(file1)
    length2 = lines_count(file2)

    with open(file1, 'rt') as source1, open(file2, 'rt') as source2, open('dest.txt', 'at') as dest:
        dest.seek(0)
        dest.truncate()

        length = min(length1, length2)

        i1 = 0
        i2 = 0

        line1 = source1.readline()
        line2 = source2.readline()
        while i1 + i2 < length * 2:
            if line1 <= line2:
                dest.write(line1)
                i1 += 1
                line1 = source1.readline()
            else:
                dest.write(line2)
                i2 += 1
                line2 = source2.readline()

        while i1 < length1:
            dest.write(source1.readline())
            i1 += 1

        while i2 < length2:
            dest.write(source2.readline())
            i2 += 1


merge_files('sorted1.txt', 'sorted2.txt')
