import os

for i in range(1, 22):
    entry = 'entry%d' % i
    os.system('convert 2013/%s/%s.png -trim thumbnails/%s.png' %
              (entry, entry, entry))
    cmd = ('convert thumbnails/%s.png -set '
           'option:size "%%[fx:min(w,h)]x%%[fx:min(w,h)]" '
           ' xc:none +swap -gravity center -composite thumbnails/%s.png' %
           (entry, entry))
    os.system(cmd)

    os.system('convert 2013/%s/%s.png -trim carousel/%s.png' %
              (entry, entry, entry))

