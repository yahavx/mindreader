import json

from mindreader.objects.user import User

class JSONEncoder:
    def user_encode(self, user):
        return json.dumps(user, default=lambda o: o.__dict__, indent=4)

    def user_decode(self, json_user):
        return json.loads(json_user)

    def snapshot_encode(self, snapshot):
        return json.dumps(snapshot, default=lambda o: o.__dict__, indent=4)

    def snapshot_decode(self, json_snapshot):
        return json.loads(json_snapshot)
