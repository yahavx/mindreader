import datetime as dt


class Snapshot:  # this snapshot implementation is used from the server and forward in the pipeline
    def __init__(self, user_id, snapshot_id, timestamp, pose, color_image_path, color_image_width, color_image_height,
                 depth_image_path, depth_image_width, depth_image_height, feelings):
        self.user_id = user_id  # user of the snapshot
        self.timestamp = timestamp
        self.snapshot_id = snapshot_id
        self.pose_translation_x = pose.translation.x
        self.pose_translation_y = pose.translation.y
        self.pose_translation_z = pose.translation.z
        self.pose_rotation_x = pose.rotation.x
        self.pose_rotation_y = pose.rotation.y
        self.pose_rotation_z = pose.rotation.z
        self.pose_rotation_w = pose.rotation.w
        self.color_image_path = color_image_path
        self.color_image_width = color_image_width
        self.color_image_height = color_image_height
        self.depth_image_path = depth_image_path
        self.depth_image_width = depth_image_width
        self.depth_image_height = depth_image_height
        self.feelings_hunger = feelings.hunger
        self.feelings_thirst = feelings.thirst
        self.feelings_exhaustion = feelings.exhaustion
        self.feelings_happiness = feelings.happiness

    def __repr__(self):
        date = dt.datetime.fromtimestamp(self.timestamp / 1000).strftime("%d/%m/%y")
        translation = [float("%0.1f" % self.pose_translation_x), float("%0.1f" % self.pose_translation_y),
                       float("%0.1f" % self.pose_translation_z)]
        rotation = [float("%0.1f" % self.pose_rotation_x), float("%0.1f" % self.pose_rotation_y),
                    float("%0.1f" % self.pose_rotation_z), float("%0.1f" % self.pose_rotation_w)]
        hunger = float("%0.1f" % self.feelings_hunger)
        thirst = float("%0.1f" % self.feelings_thirst)
        exhaustion = float("%0.1f" % self.feelings_exhaustion)
        happiness = float("%0.1f" % self.feelings_happiness)

        line1 = f'{date=}, {translation=}, {rotation=}'
        line2 = f'\t\t {hunger=}, {thirst=}, {exhaustion=}, {happiness=}'
        return f'Snapshot({line1}\n{line2})'

    def __str__(self):
        date = dt.datetime.fromtimestamp(self.timestamp / 1000).strftime("%d/%m/%y")
        translation = [float("%0.1f" % self.pose_translation_x), float("%0.1f" % self.pose_translation_y),
                       float("%0.1f" % self.pose_translation_z)]
        rotation = [float("%0.1f" % self.pose_rotation_x), float("%0.1f" % self.pose_rotation_y),
                    float("%0.1f" % self.pose_rotation_z), float("%0.1f" % self.pose_rotation_w)]
        ci_size = f'{self.color_image_height}x{self.color_image_width}'
        di_size = f'{self.depth_image_height}x{self.depth_image_width}'
        line1 = f'Snapshot from {date} on {translation} / {rotation}'
        line2 = f'with a {ci_size} color image and a {di_size} width image.'
        return f'{line1} {line2}'
