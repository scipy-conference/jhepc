import os

for i in range(1, 22):
    entry = 'entry%d' % i
    os.system(
        'convert -size x100 2013/%s/%s.png thumbnails/%s.png' %
        (entry, entry, entry))
