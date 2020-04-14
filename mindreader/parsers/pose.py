import json

from mindreader.objects import Snapshot


def parse_pose(snapshot: Snapshot):
    """Returns the position of the snapshot."""
    rotation = dict(
        x=snapshot.pose.rotation.x,
        y=snapshot.pose.rotation.y,
        z=snapshot.pose.rotation.z,
        w=snapshot.pose.rotation.w)
    translation = dict(
        x=snapshot.pose.translation.x,
        y=snapshot.pose.translation.y,
        z=snapshot.pose.translation.z)
    print(rotation)
    print(translation)
    return json.dumps({'rotation': rotation, 'translation': translation})


parse_pose.field = 'pose'
