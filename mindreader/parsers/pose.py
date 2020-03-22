import json


def parse_rotation(snapshot):
    snapshot = json.loads(snapshot)
    rotation = json.dumps(dict(
        x=snapshot["pose_rotation_x"],
        y=snapshot["pose_rotation_y"],
        z=snapshot["pose_rotation_z"],))
    return rotation


parse_rotation.field = 'rotation'


def parse_translation(snapshot):
    translation = json.dumps(dict(
        x=snapshot.pose.translation.x,
        y=snapshot.pose.translation.y,
        z=snapshot.pose.translation.z))
    context.save('translation.json', translation)


parse_translation.field = 'translation'
