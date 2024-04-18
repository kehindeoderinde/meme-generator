""" Meme engine module """

import os
import random
from textwrap import wrap
from PIL import Image, ImageDraw
from image_engine import ImageModel


class MemeEngine:
    """Generate me from Image and Quote"""

    def __init__(self, output_dir: str):
        # Check if out dir provided exists, if not create it
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            self.root_path = output_dir
        else:
            print(
                f"Destination for meme folder not found!!!\
                Creating {output_dir}"
            )
            try:
                os.mkdir(output_dir, mode=0o777)
            except Exception as e:
                print(
                    f"An error occured while creating directory \
                    {output_dir} - {e}"
                )
            else:
                self.root_path = output_dir

    def read(self, img: ImageModel) -> Image.Image:
        """Read image from Image Model"""
        try:
            res = Image.open(f"{img.parent_dir}/{img.name}")
        except Exception:
            print("Error reading image provided to meme engine")
        else:
            return res

    def resize(self, img: Image.Image, width: int) -> Image.Image:
        """Resize image to be used for meme"""
        try:
            img_width = img.size[0]
            img_height = img.size[1]
            width_diff_pcnt = width / float(img_width)
            height_size = int((float(img_height) * float(width_diff_pcnt)))
            res = img.resize((width, height_size))
        except Exception:
            print("Error resizing image provided to meme engine")
        else:
            return res

    def add_text(self, img: Image.Image, body: str, author: str):
        """Add text to resized meme image"""
        # Adding bounds to where text can be in \
        # image so it does not run out of bounds
        start_x, end_x = int(img.size[0] * 0.1), int(img.size[0] * 0.9)
        start_y, end_y = int(img.size[1] * 0.1), int(img.size[1] * 0.9)

        # Create meme text
        text = f'"{body}" - {author}'

        # Set up to draw text on Image
        draw = ImageDraw.Draw(img)

        # Determine starting point for text wrap
        start_point_width = random.randint(start_x, end_x)
        wrap_width = int(end_x - start_point_width)

        # Check if width for text is sufficient
        while start_point_width > end_x / 4:
            start_point_width = random.randint(start_x, end_x)
            wrap_width = int(end_x - start_point_width)

        # Wrap meme text
        wrapper = wrap(text=text, width=30)

        # Check if height for text is allowed
        start_point_height = random.randint(start_y, end_y)
        wrap_height = int(end_y - start_point_height)

        while (len(wrapper) * 30) + start_point_height > end_y:
            start_point_height = random.randint(start_y, end_y)
            wrap_height = int(end_y - start_point_height)

        for line in wrapper:
            draw.text(
                xy=(start_point_width, start_point_height),
                text=line.upper(),
                align="center",
                font_size=22,
            )
            start_point_height += 30

        # img.show()
        return img

    def save_to_location(self, img: Image.Image) -> str:
        """Save image to location with random name"""
        try:
            save_path = f"{self.root_path}/meme_{random.randrange(100)}.jpg"
            img.save(save_path)
        except Exception:
            print(
                f"An error occured while saving image at \
                {save_path}"
            )
        else:
            return save_path

    def make_meme(self, img: ImageModel, body: str, author: str, width=500):
        """This generates a new meme with arguments provided"""

        parsed_img = self.read(img)

        resized_img = self.resize(parsed_img, width=width)

        meme = self.add_text(img=resized_img, body=body, author=author)

        meme_path = self.save_to_location(meme)

        return meme_path
