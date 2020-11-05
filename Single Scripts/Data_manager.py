bad_words = [str(x) for x in range(101,200)]
bad_words.append('None')

with open('Dataset.txt') as oldfile, open('RDataset.txt', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)
