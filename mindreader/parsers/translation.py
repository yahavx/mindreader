import json


def parse_translation(context, snapshot):
    translation = json.dumps(dict(
        x=snapshot.pose.translation.x,
        y=snapshot.pose.translation.y,
        z=snapshot.pose.translation.z))
    context.save('translation.json', translation)


parse_translation.field = 'translation'
