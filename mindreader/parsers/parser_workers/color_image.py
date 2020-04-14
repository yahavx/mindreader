import json
from mindreader.drivers.context import Context
from PIL import Image as PIL

from mindreader.objects import Snapshot


def parse_color_image(snapshot: Snapshot) -> dict:
    """Creates the color image of the snapshot."""
    size = snapshot.color_image.width, snapshot.color_image.height
    path = snapshot.color_image.data

    context = Context(path, is_file=True)
    data = context.load('color_image', byte=True)

    image = PIL.frombytes('RGB', size, data)

    image_path = context.get_file_path('color_image.png')
    image.save(image_path, 'PNG')

    width, height = size
    return dict(data_path=image_path, image_width=width, image_height=height)


parse_color_image.field = 'color_image'
