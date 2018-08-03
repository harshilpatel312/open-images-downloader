import urllib.request
import os
import argparse
import errno
import pandas as pd
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
from time import time as timer

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


def get_ooi_labelmap(labelmap):
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


def generate_download_list(annotations, labelmap, base_url):
    '''
    Parse through input annotations dataframe, find ImageID's of objects of interest,
    and get download urls for the corresponding images

    :param annotations: annotations dataframe
    :param labelmap: dictionary of object labels and codes
    :param base_url: basename of url
    :return: list of urls to download
    '''
    # create an empty dataframe
    df_download = pd.DataFrame(columns=['ImageID', 'LabelName'])

    # append dataframes to empty df according to conditions
    for key, value in labelmap.items():
        # find ImageID's in original annots dataframe corresponding to ooi's codes
        df_download = df_download.append(annotations.loc[annotations['LabelName'] == value, ['ImageID', 'LabelName']])

    ######################
    url_download_list = []

    for idx, row in df_download.iterrows():
        # get name of the image
        image_name = row['ImageID'] + ".jpg"

        # check if the image exists in directory
        if not os.path.exists(os.path.join(OUTPUT_DIR, image_name)):
            # form url
            url = os.path.join(base_url, image_name)

            url_download_list.append(url)

    return url_download_list


def download_objects_of_interest(download_list):
    def fetch_url(url):
        try:
            urllib.request.urlretrieve(url, os.path.join(OUTPUT_DIR, url.split("/")[-1]))
            return url, None
        except Exception as e:
            return None, e

    start = timer()
    results = ThreadPool(20).imap_unordered(fetch_url, download_list)

    df_pbar = tqdm(total=len(download_list), position=1, desc="Download %: ")

    for url, error in results:
        df_pbar.update(1)
        if error is None:
            pass  # TODO: find a way to do tqdm.write() with a refresh
            # print("{} fetched in {}s".format(url, timer() - start), end='\r')
        else:
            pass  # TODO: find a way to do tqdm.write() with a refresh
            # print("error fetching {}: {}".format(url, error), end='\r')


def main():
    # read images and get base_url
    df_images = pd.read_csv(IMAGES)
    base_url = os.path.dirname(df_images['image_url'][0])  # used to download the images

    # read labelmap
    df_oid_labelmap = pd.read_csv(LABELMAP)  # open images dataset (oid) labelmap
    ooi_labelmap = get_ooi_labelmap(df_oid_labelmap)  # objects of interest (ooi) labelmap

    # read annotations
    df_annotations = pd.read_csv(ANNOTATIONS)

    print("\nGenerating download list for the following objects: ", [k for k, v in ooi_labelmap.items()])

    # get url list to download
    download_list = generate_download_list(annotations=df_annotations,
                                           labelmap=ooi_labelmap,
                                           base_url=base_url)

    # download objects of interest
    download_objects_of_interest(download_list)

    print("\nFinished downloads.")


if __name__ == '__main__':
    main()
