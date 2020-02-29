from mindreader.utils.reader import Reader


sample = "./mindreader/sample.mind"
reader = Reader(sample)

i = 0
for snapshot in reader:
    print(snapshot)
    i+=1
    if i == 10:
        break