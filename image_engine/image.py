'''Store images models for use'''
import os
from pathlib import Path
from typing import List
from .model import ImageModel

class ImageEngine:
    '''Image engine'''
    IMG_TYPES_ALLOWED = set(['.png', '.jpg'])
        
    @classmethod
    def retrieve_imgs(cls, src_path: str) -> List[ImageModel]:
        '''Retrieve all imgs in a directory'''
        
        all_files = []
        for root_dir, _, files in os.walk(src_path):
            all_files.extend([{'parent_dir': root_dir, 'name': file} for file in files])
        
        # Create image models for every valid image file in directory
        images = [ImageModel(name=file['name'], parent_dir=file['parent_dir']) for file in all_files if Path(file['name']).suffix in cls.IMG_TYPES_ALLOWED]

        return images