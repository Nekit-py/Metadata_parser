from exif import Image
from pathlib import Path, PosixPath
from exif._constants import ATTRIBUTE_ID_MAP
import pandas as pd
import numpy as np


class MetadataParser:

    def __init__(self, folder: Path):
        self.atrs = tuple(ATTRIBUTE_ID_MAP.keys())
        self.folder = folder

    def get_exif_files(self, extension: str) -> list[Path]:
        """
        Getting all files of the required extension with metadata
        """
        condition_extensions = [file for file in self.folder.glob(f'**/{extension}')]
        self.exif_files = []
        for file in condition_extensions:
            with open(file, "rb") as my_file:
                try:
                    image = Image(my_file)
                except Exception as e:
                    print(e)
            if image.has_exif:
                self.exif_files.append(file)


    def get_file_md(self, image: Path) -> pd.DataFrame:
        """
        Getting the file metadata
        """
        with open(image, 'rb') as image_file:
                image_bytes = image_file.read()
        my_image = Image(image_bytes)
        df = pd.DataFrame(columns=self.atrs)
        df = df.append(
                pd.Series([my_image.get(atr, np.nan) for atr in self.atrs], index = df.columns),
                ignore_index=True
                )
        return df

    def get_result(self):
        """
        Saving metadata in excel
        """
        received_metadata= pd.DataFrame()
        for df in self.exif_files:
            received_metadata = received_metadata.append(self.get_file_md(df))
        received_metadata.to_excel(f'{self.folder.name}.xlsx', index=False)

if __name__ == "__main__":
    test_data = Path("images")
    m = MetadataParser(test_data)
    m.get_exif_files('*.jpg')
    m.get_result()
