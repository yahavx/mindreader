import datetime as dt


class Snapshot:
    def __init__(self, timestamp, pose, color_image, depth_image, feelings):
        self.timestamp = timestamp
        self.pose = pose
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self):
        date = dt.datetime.fromtimestamp(self.timestamp / 1000).strftime("%d/%m/%y")
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
        date = dt.datetime.fromtimestamp(self.timestamp / 1000).strftime("%d/%m/%y")
        translation = [float("%0.1f" % self.pose.translation[i]) for i in range(3)]
        rotation = [float("%0.1f" % self.pose.rotation[i]) for i in range(4)]
        ci_size = f'{self.color_image.height}x{self.color_image.width}'
        di_size = f'{self.depth_image.height}x{self.depth_image.width}'
        line1 = f'Snapshot from {date} on {translation} / {rotation}'
        line2 = f'with a {ci_size} color image and a {di_size} width image.'
        return f'{line1} {line2}'


class Pose:
    def __init__(self, translation, rotation):
        self.translation = translation
        self.rotation = rotation

    def __repr__(self):
        return f'Pose({self.translation!r}, {self.rotation!r})'


class Translation:
    def __init__(self, x, y, z):
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
    def __init__(self, x, y, z, w):
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


class Image:
    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self):
        return f'Image({self.width}x{self.height})'


class Feelings:
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

    def __repr__(self):
        hunger =  self.hunger
        thirst = self.thirst
        exhaustion = self.exhaustion
        happiness = self.happiness
        return f'Feelings({hunger=}, {thirst=}, {exhaustion=}, {happiness=})'
