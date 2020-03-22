import json
from mindreader.drivers.context import Context
from PIL import Image as PIL
from . import data_dir


def parse_color_image(snapshot):
    snapshot = json.loads(snapshot)
    size = snapshot["color_image_width"], snapshot["color_image_height"]
    path = snapshot["color_image_path"]
    with open(path, 'rb') as f:
        data = f.read()
    image = PIL.frombytes('RGB', size, data)

    context = Context.generate_from_snapshot(data_dir, snapshot)
    image_path = context.path('color_image.png')
    image.save(image_path, 'PNG')
    return json.dumps({'color_image_path': image_path})


parse_color_image.field = 'color_image'
