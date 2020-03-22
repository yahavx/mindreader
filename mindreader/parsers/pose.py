import json


def parse_rotation(snapshot):
    snapshot = json.loads(snapshot)
    rotation = json.dumps(dict(
        x=snapshot["pose_rotation_x"],
        y=snapshot["pose_rotation_y"],
        z=snapshot["pose_rotation_z"],
        w=snapshot["pose_rotation_w"],))
    return rotation


parse_rotation.field = 'rotation'


def parse_translation(snapshot):
    snapshot = json.loads(snapshot)
    translation = json.dumps(dict(
        x=snapshot["pose_translation_x"],
        y=snapshot["pose_translation_y"],
        z=snapshot["pose_translation_z"]))
    return translation


parse_translation.field = 'translation'
