import sys
from os import listdir
from os.path import isfile, join
from PIL import Image

path = './plots'
plotfiles = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
images = list(map(Image.open, plotfiles))

widths, heights = zip(*(i.size for i in images))

max_width = max(widths)
sum_height = sum(heights)

new_im = Image.new('RGB', (max_width, sum_height), (255, 255, 255))

y_offset = 0
for im in images:
  new_im.paste(im, (int((max_width - im.size[0])/2),y_offset))
  y_offset += im.size[1]

new_im.save('result_kret.jpg')