from mindreader import Reader

sample = "./mindreader/sample.mind"
reader = Reader(sample)

i = 0
for snapshot in reader:
    print(snapshot)
    i+=1
    if i == 10:
        break


def snap():
    r = Reader("sample.mind.gz")
    return r.get_snapshot()


def read2():
    return Reader("sample.mind.gz")
