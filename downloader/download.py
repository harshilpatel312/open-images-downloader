import urllib.request
import os
import argparse
import errno
import pandas as pd

argparser = argparse.ArgumentParser(description='Download specific objects from Open-Images dataset')
argparser.add_argument('-a','--annots',
                        help='path to annotations file (.csv)')
argparser.add_argument('-o','--objects', nargs='+',
                        help='download images of these objects')
argparser.add_argument('-d','--dir',
                        help='path to output directory')
argparser.add_argument('-l','--labelmap',
                        help='path to labelmap (.csv)')
argparser.add_argument('-i','--images',
                        help='path to file containing links to images (.csv)')

args = argparser.parse_args()

# parse arguments
ANNOTATIONS = args.annots
OUTPUT_DIR = args.dir
OBJECTS = args.objects
LABELMAP = args.labelmap
IMAGES = args.images

# make OUTPUT_DIR if not present
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print("Created {} directory\n".format(OUTPUT_DIR))

# check if input files are valid, raise FileNotFoundError if not found
if not os.path.exists(ANNOTATIONS):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ANNOTATIONS)
elif not os.path.exists(LABELMAP):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), LABELMAP)

def main():
    # read annotations
    df_annot = pd.read_csv(ANNOTATIONS)

    # read labelmap
    df_labelmap = pd.read_csv(LABELMAP)

    # read images and get base_url
    df_images = pd.read_csv(IMAGES)
    base_url = os.path.dirname(df_images['image_url'][0]) # used to download the images

    # find codes of objects to download from the labelmap
    object_codes = {}
    for idx, row in df_labelmap.iterrows():
        if any(obj.lower() in row[1].lower() for obj in OBJECTS):
            d[obj] = row[0]

    for idx, row in df_annot.iterrows():
        # check if any objects in object_code is in row:
        if any(obj in row['LabelName'] for obj in object_codes):

            # get name of the image
            image_name = row['ImageID'] + ".jpg"

            # check if the image exists in directory
            if not os.path.exists(os.path.join(OUTPUT_DIR, image_name)):
                URL = os.path.join(base_url, image_name)

                try:
                    urllib.request.urlretrieve(URL, os.path.join(OUTPUT_DIR, image_name))
                except:
                    print("Problem downloading ", image_name)

        print('Iteration: {0}/{1}'.format(idx, df_annot.size), end='\r')

if __name__ == '__main__':
    main()
