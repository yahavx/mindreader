import json


def parse_rotation(context, snapshot):
    rotation = json.dumps(dict(
        x = snapshot.pose.translation.x,
        y=snapshot.pose.translation.y,
        z=snapshot.pose.translation.z))
    context.save('rotation.json', rotation)


parse_rotation.field = 'rotation'

