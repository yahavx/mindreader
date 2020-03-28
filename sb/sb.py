from mindreader import Reader
from mindreader.drivers.databases import init_database
from mindreader.server.server import _convert_objects_format
from mindreader.drivers.encoders.json_encoder import JSONEncoder
from bson.json_util import dumps


sample = "./mindreader/sample.mind"
# reader = Reader(sample)
#
# i = 0
# for snapshot in reader:
#     print(snapshot)
#     i+=1
#     if i == 10:
#         break


def snap():
    r = Reader("sample.mind.gz")
    return r.get_snapshot()


def read2():
    return Reader("./sample.mind.gz")


def s():
    r = Reader("sample.mind.gz")
    user = r.get_user()
    snapshot = r.get_snapshot()
    user, snapshot = _convert_objects_format(user, snapshot)
    encoder = JSONEncoder()
    return encoder.snapshot_decode(encoder.snapshot_encode(snapshot))


def s2():
    r = Reader("sample.mind.gz")
    user = r.get_user()
    snapshot = r.get_snapshot()
    user, snapshot = _convert_objects_format(user, snapshot)
    encoder = JSONEncoder()
    return encoder.snapshot_decode(snapshot)


def u():
    r = Reader("sample.mind.gz")
    user = r.get_user()
    snapshot = r.get_snapshot()
    user, snapshot = _convert_objects_format(user, snapshot)
    return user


def db():
    db = init_database("mongodb://127.0.0.1:27017")
    return db