import datetime as dt
from .snapshot_utils import Pose, Image, Feelings, SnapshotMetadata


class Snapshot:
    """
    This class describes the snapshot object of the mindreader package.
    Any changes to this class should be considered carefully.
    """

    def __init__(self, pose: Pose, color_image: Image, depth_image: Image, feelings: Feelings,
                 metadata: SnapshotMetadata):
        self.pose = pose
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings
        self.metadata = metadata

    def __repr__(self):
        date = dt.datetime.fromtimestamp(self.metadata.timestamp / 1000).strftime("%d/%m/%y")
        translation = [float("%0.1f" % self.pose.translation[i]) for i in range(3)]
        rotation = [float("%0.1f" % self.pose.rotation[i]) for i in range(4)]
        hunger = float("%0.1f" % self.feelings.hunger)
        thirst = float("%0.1f" % self.feelings.thirst)
        exhaustion = float("%0.1f" % self.feelings.exhaustion)
        happiness = float("%0.1f" % self.feelings.happiness)

        line1 = f'{date=}, {translation=}, {rotation=}'
        line2 = f'\t\t {hunger=}, {thirst=}, {exhaustion=}, {happiness=}'
        return f'Snapshot({line1}\n{line2})'

    def __str__(self):
        date = dt.datetime.fromtimestamp(self.metadata.timestamp / 1000).strftime("%d/%m/%y")
        translation = [float("%0.1f" % self.pose.translation[i]) for i in range(3)]
        rotation = [float("%0.1f" % self.pose.rotation[i]) for i in range(4)]
        ci_size = f'{self.color_image.height}x{self.color_image.width}'
        di_size = f'{self.depth_image.height}x{self.depth_image.width}'
        line1 = f'Snapshot from {date} on {translation} / {rotation}'
        line2 = f'with a {ci_size} color image and a {di_size} width image.'
        return f'{line1} {line2}'