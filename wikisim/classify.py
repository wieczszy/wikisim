"""Scirpt to test the Wiki articles classification using CLI.
Run as 'python classify path/to/model article_title'
"""

import argparse
from model import WikiModel

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('model_file', type=str, help="Path to trained model file.")
    parser.add_argument('url', type=str, help='URL to the article.')
    args = parser.parse_args()

    model = WikiModel()
    model.load(args.model_file)
    R = model.classify(args.url)

    print("\n=== Classification for: ===")
    print(args.url + '\n')
    for r in R:
        print(r)