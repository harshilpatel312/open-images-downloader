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
    Given labelmap of all objects in Open Images dataset, get labelmap of objects of interest

    :param labelmap: dataframe containing object labels with respective label codes
    :return: dictionary containing object labels and codes of
                          user-inputted objects
    '''

    object_codes = {}
    for idx, row in labelmap.iterrows():
        if any(obj.lower() in row[1].lower() for obj in OBJECTS):
            object_codes[row[1].lower()] = row[0]

    return object_codes


def get_download_info(df, labelmap):
    '''
    Parse through input dataframe and get ImageID's of objects of interest

    :param df: annotations dataframe
    :param labelmap: dictionary of object labels and codes
    :return: dataframe with annotations
    '''
    ret_df = pd.DataFrame(columns=['ImageID', 'LabelName'])

    for key, value in labelmap.items():
        ret_df = ret_df.append(df.loc[df['LabelName'] == value, ['ImageID', 'LabelName']])

    return ret_df


def download_objects_of_interest(download_info, base_url):
    '''
    Download objects of interest

    :param download_info: dataframe containing download info
    :param base_url: basename of url
    :return: None
    '''

    download_pbar = TqdmUpTo(unit='B', unit_scale=True, miniters=1, position=3)
    df_pbar = tqdm(total=download_info.size, position=1, desc="Dataframe progress")

    for idx, row in download_info.iterrows():
        df_pbar.update(1)

        # get name of the image
        image_name = row['ImageID'] + ".jpg"

        # check if the image exists in directory
        if not os.path.exists(os.path.join(OUTPUT_DIR, image_name)):
            # form url
            url = os.path.join(base_url, image_name)

            try:
                download_pbar.set_description(url.split('/')[-1])
                # download image
                urllib.request.urlretrieve(url,
                                           os.path.join(OUTPUT_DIR, image_name),
                                           reporthook=download_pbar.update_to)
            except:
                pass  # TODO


def main():
    # read images and get base_url
    df_images = pd.read_csv(IMAGES)
    base_url = os.path.dirname(df_images['image_url'][0])  # used to download the images

    # read labelmap
    df_full_labelmap = pd.read_csv(LABELMAP)
    # get labelmap for objects of interest (ooi)
    ooi_labelmap = get_object_codes(df_full_labelmap)
    print("\nDownloading the following objects:", [k for k, v in ooi_labelmap.items()])

    # read annotations
    df_annotations = pd.read_csv(ANNOTATIONS)
    # get annotations of just objects of interest
    df_download = get_download_info(df_annotations, ooi_labelmap)

    # download objects of interest
    download_objects_of_interest(download_info=df_download, base_url=base_url)

    print("\nFinished downloads.")

if __name__ == '__main__':
    main()
