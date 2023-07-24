# Zip Find and Replace

## Description
Zip Find and Replace is a Python command-line tool that allows you to perform a find and replace on either the content of files within a ZIP archive or the file names themselves

## Features
- Perform find and replace on the content of files within a ZIP archive.
- Perform find and replace on the names of files within a ZIP archive.
- Automatically creates a backup of the original ZIP file before making any changes.

## Dependencies
Python 3.6 or later

## Usage

### Command Line Interface

```
python zipfnr.py [mode] [zipfile] [file_extension] [old_string] [new_string]
```

- **mode**: This is the operation mode, which can be either `text` (for find and replace within file content) or `filename` (for find and replace within filenames).
- **zipfile**: The path to the ZIP file to be processed.
- **file_extension**: The extension of files to be processed within the ZIP file (for example, `.txt`).
- **old_string**: The string to be replaced.
- **new_string**: The string to replace `old_string` with.

### Python API

This tool can also be imported and used within a Python script. Here's a basic example:

```python
from zipfnr import TextReplaceZipProcessor, FilenameReplaceZipProcessor

# Create a TextReplaceZipProcessor and process a ZIP file
processor = TextReplaceZipProcessor('my_file.zip', '.txt')
processor.process_zip('hello', 'hi')

# Create a FilenameReplaceZipProcessor and process a ZIP file
processor = FilenameReplaceZipProcessor('my_file.zip', '.txt')
processor.process_zip('old_name', 'new_name')
```

## Tests
The `pytest` Python testing framework is used for testing this tool. To run the tests, execute the following command in the project root directory:

```
pytest
```

## License
This project is licensed under the MIT License.