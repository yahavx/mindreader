from PIL import Image as PIL
# from mindreader.drivers.message_queues.rabbit_mq import PBMQEncoder


# def parse_color_image(raw_snapshot, encoded=False):
#     if encoded:
#         snapshot = PBMQEncoder.snapshot_decode(raw_snapshot)
#     else:
#         snapshot = raw_snapshot
#     size = snapshot.color_image.width, snapshot.color_image.height
#     image = PIL.frombytes('RGB', size, snapshot.color_image.data)
#     return image


# parse_color_image.field = 'color_image'
