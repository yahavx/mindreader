from mindreader.objects import Snapshot


def parse_feelings(snapshot: Snapshot):
    """Returns the feeling of the snapshot."""
    feelings = dict(
        hunger=snapshot.feelings.hunger,
        thirst=snapshot.feelings.thirst,
        exhaustion=snapshot.feelings.exhaustion,
        happiness=snapshot.feelings.happiness)
    return feelings


parse_feelings.field = "feelings"
