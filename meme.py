"""MEME GENERATOR CLI APPLICATION."""

from pathlib import Path
import random
import argparse

# @TODO Import your Ingestor and MemeEngine classes
from quote_engine import Ingestor, QuoteModel
from image_engine import ImageEngine, ImageModel
from meme_engine import MemeEngine

from error_engine import InvalidFilePathError

QUOTE_BODY_LIMIT = 35
QUOTE_AUTHOR_LIMIT = 10


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        # NOTE: os.walk is implemented in out ImageEngine class
        imgs = ImageEngine.retrieve_imgs(images)

        img = random.choice(imgs)
    else:
        if not Path(path).exists():
            raise InvalidFilePathError(path)
        else:
            if not (
                Path(path).is_file
                and (
                    Path(path).suffix == ".png" or Path(path).suffix == ".jpg"
                )
            ):
                raise Exception(
                    "Path specified is not a valid image.\
                    Please only use paths to .jpg or .png files"
                )
            img = ImageModel(
                parent_dir=Path(path).parent, name=Path(path).name
            )
    if body is None:
        quote_files = [
            "./_data/DogQuotes/DogQuotesTXT.txt",
            "./_data/DogQuotes/DogQuotesDOCX.docx",
            "./_data/DogQuotes/DogQuotesPDF.pdf",
            "./_data/DogQuotes/DogQuotesCSV.csv",
        ]
        quotes = []
        for file in quote_files:
            quotes.extend(Ingestor.parse(path=file))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception("Author Required if Body is Used")
        quote = QuoteModel(body, author)

    meme = MemeEngine("./tmp")
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(
        description="CLI application to \
        generate memes with dog pictures and quotes"
    )
    parser.add_argument("-b", "--body", type=str)
    parser.add_argument("-a", "--author", type=str)
    parser.add_argument("-p", "--path", type=str)

    args = parser.parse_args()

    print(f"Meme saved at {generate_meme(args.path, args.body, args.author)}")
