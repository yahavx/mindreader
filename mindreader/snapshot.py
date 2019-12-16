import datetime as dt

class Snapshot:

    def __repr__(self):
        timestamp = dt.datetime.fromtimestamp(self.timestamp).strftime("%d/%m/%y")
        translation = [float("%0.1f" % self.translation[i]) for i in range(3)]
        rotation = [float("%0.1f" % self.rotation[i]) for i in range(4)]
        hunger = float("%0.1f" % self.hunger)
        thirst = float("%0.1f" % self.thirst)
        exhaustion = float("%0.1f" % self.exhaustion)
        happiness = float("%0.1f" % self.happiness)

        line1 = f'{timestamp=}, {translation=}, {rotation=}'
        line2 = f'\t\t {hunger=}, {thirst=}, {exhaustion=}, {happiness=}'
        return f'Snapshot({line1}\n{line2})'

    def __str__(self):
        date = '01/01/2000'
        translation = [float("%0.1f" % self.translation[i]) for i in range(3)]
        rotation = [float("%0.1f" % self.rotation[i]) for i in range(4)]
        ci_size = f'{self.ci_height}x{self.ci_width}'
        di_size = f'{self.di_height}x{self.di_width}'
        line1 = f'Snapshot from {date} on {translation} / {rotation}'
        line2 = f'with a {ci_size} color image and a {di_size} width image.'
        return f'{line1} {line2}'
