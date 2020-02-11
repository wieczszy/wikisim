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
