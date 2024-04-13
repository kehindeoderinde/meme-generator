''' Meme engine module '''
import os
import random
from PIL import Image, ImageDraw
from image_engine import ImageModel

class MemeEngine:
    '''Generate me from Image and Quote'''
    
    def __init__(self, output_dir: str):
        # Check if out dir provided exists, if not create it
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            self.root_path = output_dir
        else:
            print(f'Destination for meme folder not found!!! Creating {output_dir}')
            try:
                os.mkdir(output_dir, mode=0o777)
            except Exception as e:
                print(f'An error occured while creating directory {output_dir} - {e}')
            else:
                self.root_path = output_dir
        
    def make_meme(self, img: ImageModel, text: str, author: str, width=500) -> str:
        '''This generates a new meme with arguments provided'''
        
        with Image.open(f'{img.parent_dir}/{img.name}') as img:
            img = img.resize((width, width))
            draw = ImageDraw.Draw(img)
            draw.multiline_text((7.5, 450), f'"{text}" - {author}', align='center', font_size=22)
            # img.show()
            try:
                save_path = f'{self.root_path}/meme_{random.randrange(100)}.jpg'
                img.save(save_path)
            except Exception:
                print(f'An error occured while saving image at {save_path}')
            else:    
                return save_path
    