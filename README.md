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
python download.py --images={IMAGE_FILE}.csv --annots={ANNOTATION_FILE}.csv --objects {SPACE_SEPARATE_OBJECT_NAMES} --dir={OUTPUT_DIR} --labelmap={LABELMAP}.csv

# example
python download.py --images=test-images.csv --annots=test-annotations-bbox.csv --objects boat buoy --dir=test --labelmap=class-descriptions-boxable.csv
```
