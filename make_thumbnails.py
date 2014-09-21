import os
import argparse
from glob import glob


parser = argparse.ArgumentParser()
parser.add_argument("folder", type=int)
args = parser.parse_args()
folder = args.folder
filenames = glob("%s/*" % folder)

for filename in filenames:
    entry = os.path.basename(filename)

    os.system('convert %s/%s/%s.png -trim thumbnails/%s_%s.png' %
              (folder, entry, entry, folder, entry))
    cmd = ('convert thumbnails/%s_%s.png -set '
           'option:size "%%[fx:min(w,h)]x%%[fx:min(w,h)]" '
           ' xc:none +swap -gravity center -composite thumbnails/%s_%s.png' %
           (folder, entry, folder, entry))
    os.system(cmd)

    os.system('convert %s/%s/%s.png -trim carousel/%s_%s.png' %
              (folder, entry, entry, folder, entry))
