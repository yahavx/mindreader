import datetime as dt

class Snapshot:

    def __repr__(self):
        timestamp = self.timestamp
        translation = [float("%0.2f" % self.translation[i]) for i in range(3)]
        rotation = [float("%0.2f" % self.rotation[i]) for i in range(4)]
        hunger = float("%0.2f" % self.hunger)
        thirst = float("%0.2f" % self.thirst)
        exhaustion = float("%0.2f" % self.exhaustion)
        happiness = float("%0.2f" % self.happiness)

        line1 = f'{timestamp=}, {translation=}, {rotation=}'
        line2 = f'\t\t {hunger=}, {thirst=}, {exhaustion=}, {happiness=}'
        return f'Snapshot({line1}\n{line2})'
