import json
from mindreader.drivers.context import Context
from . import data_dir
import numpy
import matplotlib
import matplotlib.pyplot as plt


def parse_depth_image(snapshot):
    snapshot = json.loads(snapshot)
    size = snapshot["depth_image_height"], snapshot["depth_image_width"]
    path = snapshot["depth_image_path"]
    # TODO: maybe use the path?
    context = Context.generate_from_snapshot(data_dir, snapshot)
    data = json.loads(context.load('depth_image'))
    shaped = numpy.reshape(data, size)
    plt.imshow(shaped,  cmap=matplotlib.cm.RdYlGn, interpolation='nearest')  # TODO: cmap=hot, interpolation='nearest'?
    # plt.colorbar()

    image_path = context.path('depth_image.png')
    plt.savefig(image_path)
    return json.dumps({'depth_image_path': image_path})


parse_depth_image.field = 'depth_image'
