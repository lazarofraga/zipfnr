"""
This module provides tools for processing zip files.

It includes the abstract base class `ZipProcessor` and two concrete implementations
`TextReplaceZipProcessor` and `FilenameReplaceZipProcessor` that modify either the 
content of the files or the filenames in the zip file.
"""

import os
import shutil
import zipfile
from abc import ABC, abstractmethod
import logging
import argparse


logging.basicConfig(level=logging.INFO)


class ZipProcessor(ABC):
    """
    An abstract base class for processors that can modify the contents or filenames of
    files within a zip file.

    The class takes a file path and target extension as input, and provides a method
    `process_zip` to process the zip file.
    """

    def __init__(self, file_path, target_ext):
        """
        Initializes the `ZipProcessor`.

        Parameters:
            file_path (str): The path to the zip file.
            target_ext (str): The file extension of the files to be processed.
        """
        self.file_path = file_path
        self.target_ext = target_ext
        self.backup_path = f"{file_path}.bak"
        logging.info(
            f"Initializing ZipProcessor with file: {file_path} and target extension: {target_ext}"
        )

    def process_zip(self, find_string, replace_string):
        """
        Processes the zip file, performing find and replace operations either on
        the file content or the filename, depending on the concrete implementation.

        Parameters:
            find_string (str): The string to find.
            replace_string (str): The string to replace `find_string` with.
        """
        logging.info(f"Making a backup copy of the original file: {self.file_path}")
        shutil.copy(self.file_path, self.backup_path)

        logging.info("Processing the zip file")
        with zipfile.ZipFile(self.file_path, "r") as zin:
            with zipfile.ZipFile(f"{self.file_path}.tmp", "w") as zout:
                for item in zin.infolist():
                    if item.filename.endswith(self.target_ext):
                        data = zin.read(item.filename)
                        data, item.filename = self.process_item(
                            data, item.filename, find_string, replace_string
                        )
                    else:
                        data = zin.read(item.filename)
                    zout.writestr(item, data)

        logging.info(
            "Cleaning up and replacing the original file with the processed file"
        )
        os.remove(self.file_path)
        os.rename(f"{self.file_path}.tmp", self.file_path)

    @abstractmethod
    def process_item(self, data, filename, find_string, replace_string):
        """
        An abstract method that processes a single item within the zip file.
        The concrete implementation of this method in derived classes decides
        what kind of processing occurs.
        """
        pass


class TextReplaceZipProcessor(ZipProcessor):
    """
    A `ZipProcessor` that performs find and replace operations on the content of
    files within the zip file.
    """

    def process_item(self, data, filename, find_string, replace_string):
        """
        Performs find and replace operations on the content of a file.

        Parameters:
            data (bytes): The content of the file.
            filename (str): The name of the file.
            find_string (str): The string to find.
            replace_string (str): The string to replace `find_string` with.

        Returns:
            tuple: The processed content and the unchanged filename.
        """
        logging.info(f"Performing text replacement in file: {filename}")
        text = data.decode("utf-8")
        text = text.replace(find_string, replace_string)
        return text.encode("utf-8"), filename


class FilenameReplaceZipProcessor(ZipProcessor):
    """
    A `ZipProcessor` that performs find and replace operations on the filenames within
    the zip file.
    """

    def process_item(self, data, filename, find_string, replace_string):
        """
        Performs find and replace operations on the filename.

        Parameters:
            data (bytes): The content of the file.
            filename (str): The name of the file.
            find_string (str): The string to find.
            replace_string (str): The string to replace `find_string` with.

        Returns:
            tuple: The unchanged content and the processed filename.
        """
        logging.info(f"Performing filename replacement: {filename}")
        return data, filename.replace(find_string, replace_string)


def main():
    parser = argparse.ArgumentParser(
        description="Process a zip file, replacing text within files or filenames based on the user's choice."
    )
    parser.add_argument(
        "mode",
        type=str,
        choices=["text", "filename"],
        help="The mode of operation. 'text' will replace text within files, 'filename' will replace text within filenames.",
    )
    parser.add_argument(
        "filepath", type=str, help="The path to the zip file to process."
    )
    parser.add_argument(
        "extension", type=str, help="The extension of the files to process."
    )
    parser.add_argument("find", type=str, help="The text to find.")
    parser.add_argument(
        "replace", type=str, help="The text to replace the found text with."
    )

    args = parser.parse_args()

    if args.mode == "text":
        processor = TextReplaceZipProcessor(args.filepath, args.extension)
    else:
        processor = FilenameReplaceZipProcessor(args.filepath, args.extension)

    processor.process_zip(args.find, args.replace)


if __name__ == "__main__":
    main()
