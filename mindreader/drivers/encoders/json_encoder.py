import json


class JSONEncoder:
    def user_encode(self, user):
        return json.dumps(user.__dict__, indent=4)

    def user_decode(self, json_user):
        return json.loads(json_user)

    def snapshot_encode(self, snapshot):
        return json.dumps(snapshot.__dict__, indent=4)

    def snapshot_decode(self, json_snapshot):
        return json.loads(json_snapshot)
