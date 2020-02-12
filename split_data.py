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

root_dir = 'wikisim/data/featured_articles'
for root, dirs, files in os.walk(root_dir):
    for subdir in dirs:
        subdir_files = [f for f in os.listdir(os.path.join(root, subdir))]
        n = len(subdir_files) - 1
        l = int(PROPORTION * n)
        idxs = [random.randint(0, n) for _ in range(l)]
        idxs = random.sample(range(0, n), l)
        test_files = [subdir_files[idx] for idx in idxs]
        test_dir = os.path.join('data', 'test_data', subdir)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        for file in test_files:
            src = os.path.join(root, subdir, file)
            dst = os.path.join(test_dir, file)
            shutil.move(src, dst)