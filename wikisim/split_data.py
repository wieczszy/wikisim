"""Script to separate test data from featured articles
downloaded using crawler.py.

Proportion of data to use for testing can be set in the
PROPORTION constant.
"""
import os
import random
import shutil

PROPORTION = 0.2

random.seed()

root_dir = 'data/featured_articles'
for root, dirs, files in os.walk(root_dir):
    for subdir in dirs:
        subdir_files = [f for f in os.listdir(os.path.join(root, subdir))]
        n = len(subdir_files) - 1
        l = int(PROPORTION * n)
        idxs = [random.randint(0, n) for _ in range(l)]
        test_files = [subdir_files[idx] for idx in idxs]
        dst = os.path.join('data', 'test_data', subdir)
        if not os.path.exists(dst):
            os.makedirs(dst)
        for file in test_files:
            src = os.path.join(root, subdir, file)
            shutil.move(src, dst)