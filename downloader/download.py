import urllib.request
import os
import argparse
import errno
import pandas as pd
from utils import *
from tqdm import tqdm

argparser = argparse.ArgumentParser(description='Download specific objects from Open-Images dataset')
argparser.add_argument('-a', '--annots',
                       help='path to annotations file (.csv)')
argparser.add_argument('-o', '--objects', nargs='+',
                       help='download images of these objects')
argparser.add_argument('-d', '--dir',
                       help='path to output directory')
argparser.add_argument('-l', '--labelmap',
                       help='path to labelmap (.csv)')
argparser.add_argument('-i', '--images',
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
    print("\nCreated {} directory\n".format(OUTPUT_DIR))

# check if input files are valid, raise FileNotFoundError if not found
if not os.path.exists(ANNOTATIONS):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ANNOTATIONS)
elif not os.path.exists(LABELMAP):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), LABELMAP)


def get_object_codes(labelmap):
    '''
    :param labelmap: dataframe containing object labels with respective label codes
    :return object_codes: dictionary containing object labels and codes of
                          user-inputted objects
    '''
    object_codes = {}
    for idx, row in labelmap.iterrows():
        if any(obj.lower() in row[1].lower() for obj in OBJECTS):
            object_codes[row[1].lower()] = row[0]

    return object_codes


def download_objects_of_interest(annotations, labelmap, base_url):
    download_pbar = TqdmUpTo(unit='B', unit_scale=True, miniters=1, position=3)
    df_pbar = tqdm(total=annotations.size, position=1, desc="Dataframe progress")

    for idx, row in annotations.iterrows():
        df_pbar.update(1)

        # check if any objects in object_code is in row:
        if any(obj in row['LabelName'] for obj in labelmap.values()):

            # get name of the image
            image_name = row['ImageID'] + ".jpg"

            # check if the image exists in directory
            if not os.path.exists(os.path.join(OUTPUT_DIR, image_name)):
                url = os.path.join(base_url, image_name)

                try:
                    download_pbar.set_description(url.split('/')[-1])
                    urllib.request.urlretrieve(url,
                                               os.path.join(OUTPUT_DIR, image_name),
                                               reporthook=download_pbar.update_to)
                except:
                    pass  # TODO


def main():
    # read annotations
    df_annotations = pd.read_csv(ANNOTATIONS)

    # read labelmap
    df_full_labelmap = pd.read_csv(LABELMAP)

    # read images and get base_url
    df_images = pd.read_csv(IMAGES)
    base_url = os.path.dirname(df_images['image_url'][0])  # used to download the images

    # get labelmap for objects of interest (ooi)
    ooi_labelmap = get_object_codes(df_full_labelmap)
    print("\nDownloading the following objects:", [k for k, v in ooi_labelmap.items()])

    # download objects of interest
    download_objects_of_interest(annotations=df_annotations,
                                 labelmap=ooi_labelmap,
                                 base_url=base_url)


if __name__ == '__main__':
    main()
