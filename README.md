## USAGE
1. Get images + annotations data:
```shell
# get the training data
wget https://requestor-proxy.figure-eight.com/figure_eight_datasets/open-images/train-images-boxable.csv
wget https://requestor-proxy.figure-eight.com/figure_eight_datasets/open-images/train-annotations-bbox.csv

# get the test data
wget https://requestor-proxy.figure-eight.com/figure_eight_datasets/open-images/test-annotations-bbox.csv
wget https://requestor-proxy.figure-eight.com/figure_eight_datasets/open-images/test-images.csv
```

2. Get the labelmap that maps class labels to class IDs:
```shell
wget https://requestor-proxy.figure-eight.com/figure_eight_datasets/open-images/class-descriptions-boxable.csv
```

3. To download a specific objects:
```shell
cd downloader/

python download.py --images={PATH_TO_IMAGE_FILE}.csv --annots={PATH_TO_ANNOTATION_FILE}.csv --objects {SPACE_SEPARATE_OBJECT_NAMES} --dir={OUTPUT_DIR} --labelmap={PATH_TO_LABELMAP}.csv

# example
python download.py --images=/home/smr/projects/open-images-downloader/test-images.csv --annots=/home/smr/projects/open-images-downloader/test-annotations-bbox.csv --objects boat buoy --dir=/home/smr/projects/open-images-downloader/test --labelmap=/home/smr/projects/open-images-downloader/class-descriptions-boxable.csv
```
