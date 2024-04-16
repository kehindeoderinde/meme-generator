"""FLASK APPLICATION"""

import json
import random
import subprocess
from pathlib import Path

import requests
from flask import Flask, Response, abort, render_template, request

from image_engine import ImageEngine, ImageModel
from meme_engine import MemeEngine
from quote_engine import Ingestor

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)

SAVE_PATH = "./static"
meme = MemeEngine(SAVE_PATH)


def setup():
    """Load all resources"""

    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    for file in quote_files:
        quotes.extend(Ingestor.parse(path=file))

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    # NOTE: os.walk is implemented in out ImageEngine class
    imgs = ImageEngine.retrieve_imgs(images_path)

    return quotes, imgs


quotes, imgs = setup()
# print(quotes)
# print(imgs)


@app.route("/")
def meme_rand():
    """Generate a random meme"""

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """User input for meme information"""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme"""

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.
    if request.method == "POST":
        if not request.form.get("image_url"):
            res = json.dumps({"error": "valid image url required"})
            abort(Response(res, 401))
        else:
            # print()
            # print(request.form)
            try:
                req = requests.get(request.form.get("image_url"), timeout=300)
                if (
                    req.headers.get("Content-Type") is not None
                    and req.headers.get("Content-Type") != "image/jpeg"
                ):
                    print("Invalid Img URL")
                    return render_template("meme_error.html")
            except Exception:
                print("Cannot download image")
                return render_template("meme_error.html")
            else:
                response = req.content
                filename = Path(request.form.get("image_url")).name

                with open(f"{SAVE_PATH}/{filename}", mode="wb") as f:
                    f.write(response)
                    img = ImageModel(parent_dir=SAVE_PATH, name=filename)

        if request.form.get("body") and request.form.get("author"):
            body = request.form.get("body")
            author = request.form.get("author")
        elif request.form.get("body"):
            body = request.form.get("body")
            if not request.form.get("author"):
                res = json.dumps({"error": "Author Required if Body is Used"})
                abort(Response(res, 401))
        else:
            print(
                "No author/body provided. \
                Selecting random quote from database"
            )
            quote = random.choice(quotes)
            body, author = (
                quote.body,
                quote.author,
            )
        path = meme.make_meme(img, body, author)

    # NOTE: Delete downloaded file from tmp storage folder
    status = subprocess.call(["rm", f"{SAVE_PATH}/{filename}"])
    if status != 0:
        print("Command failed with return code", status)
    return render_template("meme.html", path=path)


if __name__ == "__main__":
    app.run()
