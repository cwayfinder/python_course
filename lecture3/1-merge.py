def merge_files(file1, file2):
    with open(file1, 'rt') as source1, open(file2, 'rt') as source2, open('dest.txt', 'wt') as dest:
        line1 = source1.readline()
        line2 = source2.readline()
        while line1 or line2:
            num1 = int(line1) if line1 else float('inf')
            num2 = int(line2) if line2 else float('inf')
            if num1 < num2:
                dest.write('{}\n'.format(num1))
                line1 = source1.readline()
            else:
                dest.write('{}\n'.format(num2))
                line2 = source2.readline()


merge_files('sorted1.txt', 'sorted2.txt')
