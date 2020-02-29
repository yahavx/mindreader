from PIL import Image as PIL


def parse_color_image(context, snapshot):
    path = context.path('color_image.jpg')
    size = snapshot.color_image.width, snapshot.color_image.height
    image = PIL.new('RGB', size)
    image.putdata(snapshot.color_image.data)
    image.save(path)


parse_color_image.field = 'color_image'
