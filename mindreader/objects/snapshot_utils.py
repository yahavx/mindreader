class Translation:
    """Defines the translation in a snapshot."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.z
        raise ValueError

    def __repr__(self):
        tran = [float("%0.1f" % self[i]) for i in range(3)]
        return f'Translation({tran[0]}, {tran[1]}, {tran[2]})'


class Rotation:
    """Defines the rotation in a snapshot."""

    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.z
        if item == 3:
            return self.w
        raise ValueError

    def __repr__(self):
        rot = [float("%0.1f" % self[i]) for i in range(4)]
        return f'Rotation({rot[0]}, {rot[1]}, {rot[2]}, {rot[3]})'


class Pose:
    """Defines the pose in a snapshot."""

    def __init__(self, translation: Translation, rotation: Rotation):
        self.translation = translation
        self.rotation = rotation

    def __repr__(self):
        return f'Pose({self.translation!r}, {self.rotation!r})'


class Image:
    """Defines an image of a snapshot. The data can be the data itself, or a path to a file that contains it."""

    def __init__(self, width: int, height: int, data):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self):
        return f'Image({self.width}x{self.height})'


class Feelings:
    def __init__(self, hunger: float, thirst: float, exhaustion: float, happiness: float):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

    def __repr__(self):
        hunger = self.hunger
        thirst = self.thirst
        exhaustion = self.exhaustion
        happiness = self.happiness
        return f'Feelings(hunger={hunger}, thirst={thirst}, exhaustion={exhaustion}, happiness={happiness})'


class SnapshotMetadata:
    """
    Defines the metadata of a snapshot.
    Can be only partially initialized.
    """

    def __init__(self, timestamp: int = 0, user_id: int = 0, snapshot_id: str = ''):
        self.timestamp = timestamp
        self.user_id = user_id
        self.snapshot_id = snapshot_id

    def __repr__(self):
        return f'Metadata(timestamp={self.timestamp}, user_id={self.user_id}, snapshot_id={self.snapshot_id})'
