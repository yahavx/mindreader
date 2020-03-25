import json
from mindreader.drivers.context import Context
from PIL import Image as PIL
from . import data_dir


def parse_color_image(snapshot):
    snapshot = json.loads(snapshot)
    size = snapshot["color_image_width"], snapshot["color_image_height"]
    path = snapshot["color_image_path"]  # we can determine the path from the context now, so don't need this really
    # TODO: maybe use the path?
    context = Context.generate_from_snapshot(snapshot)
    data = context.load('color_image', byte=True)
    image = PIL.frombytes('RGB', size, data)

    image_path = context.path('color_image.png')  # save it to the same directory, can be changed if needed
    image.save(image_path, 'PNG')
    width, height = size
    return json.dumps({'data_path': image_path, 'image_width': width, 'image_height': height})


parse_color_image.field = 'color_image'
