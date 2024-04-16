""" Meme engine module """

import os
import random
import textwrap
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
            print(img.size)
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
        wrapper = textwrap.TextWrapper(width=50)
        text = wrapper.fill(f'"{body}" - {author}')
        print(text)
        start_x = img.size[0] * 0.2
        start_y = img.size[1] * 0.2

        end_x = img.size[0] * 0.8
        end_y = img.size[1] * 0.8

        x = random.randint(start_x, end_x)
        y = random.randint(start_y, end_y)

        draw = ImageDraw.Draw(img)

        draw.multiline_text()

        # draw.multiline_text(
        #     (7.5, 450), f'"{body}" - {author}',
        #     align="center", font_size=22
        # )
        img.show()
        # return img

    def make_meme(self, img: ImageModel, body: str, author: str, width=500):
        """This generates a new meme with arguments provided"""

        parsed_img = self.read(img)

        resized_img = self.resize(parsed_img, width=width)

        self.add_text(img=resized_img, body=body, author=author)

        # try:
        #     save_path = f"{self.root_path}/meme_{random.randrange(100)}\
        #         .jpg"
        #     img.save(save_path)
        # except Exception:
        #     print(
        #         f"An error occured while saving image at \
        #         {save_path}"
        #     )
        # else:
        #     return save_path
