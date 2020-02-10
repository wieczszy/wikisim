import os
import random
import shutil

random.seed()

for root, dirs, files in os.walk('data/featured_articles'):
    for subdir in dirs:
        subdir_files = [f for f in os.listdir(os.path.join(root, subdir))]
        n = len(subdir_files) - 1
        l = int(0.2 * n)
        idxs = [random.randint(0, n) for _ in range(l)]
        training_files = [subdir_files[idx] for idx in idxs]
        test_dir = os.path.join('data', 'test_data', subdir)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        for file in training_files:
            src = os.path.join(root, subdir, file)
            dst = os.path.join(test_dir, file)
            shutil.move(src, dst)

