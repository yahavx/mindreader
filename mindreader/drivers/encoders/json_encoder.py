import json


def snap_encode(snapshot):
    # result = json.dumps(snapshot, cls=ComplexEncoder)
    result = json.dumps(snapshot, default=lambda o: o.__dict__ if type(o) != bytes else o.hex(), indent=4)
    return result


def snap_decode(json_snapshot):
    pass


def user_encode(user):
    return snap_encode(user)


def user_decode(user):
    pass
