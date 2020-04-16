import numpy
import matplotlib
import matplotlib.pyplot as plt
from mindreader.drivers.context import Context
from mindreader.objects import Snapshot


def parse_depth_image(snapshot: Snapshot):
    """Creates the depth image of the snapshot."""
    size = snapshot.depth_image.height, snapshot.depth_image.width
    path = snapshot.depth_image.data

    context = Context(path, is_file=True)
    data = context.load('depth_image', is_json=True)

    shaped = numpy.reshape(data, size)
    fig = plt.imshow(shaped)
    fig.set_cmap(matplotlib.cm.RdYlGn)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    height, width = fig.get_size()

    image_path = context.get_file_path('depth_image.png')
    plt.savefig(image_path)

    return dict(data_path=image_path, width=width, height=height)


parse_depth_image.field = 'depth_image'
