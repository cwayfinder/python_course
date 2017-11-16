import collections


def most_common_words(file_name):
    with open(file_name, 'rt') as source:
        dictionary = {}

        for line in source:
            words = line.split()
            for word in words:
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

        c = collections.Counter(dictionary)

        return [t[0] for t in c.most_common(10)]


print(most_common_words('text.txt'))
