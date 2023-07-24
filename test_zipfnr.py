import subprocess
import zipfile
import os
import pytest
from zipfnr import TextReplaceZipProcessor, FilenameReplaceZipProcessor


def create_zip_file(filename):
    with zipfile.ZipFile(filename, "w") as zf:
        zf.writestr("test1.txt", "hello world")
        zf.writestr("test2.txt", "goodbye world")
        zf.writestr("subfolder/test3.txt", "nested hello")


def test_text_replace():
    create_zip_file("test_text.zip")
    processor = TextReplaceZipProcessor("test_text.zip", ".txt")
    processor.process_zip("hello", "hi")

    with zipfile.ZipFile("test_text.zip", "r") as zf:
        assert zf.read("test1.txt").decode("utf-8") == "hi world"
        assert zf.read("subfolder/test3.txt").decode("utf-8") == "nested hi"

    os.remove("test_text.zip")
    os.remove("test_text.zip.bak")


def test_filename_replace():
    create_zip_file("test_filename.zip")
    processor = FilenameReplaceZipProcessor("test_filename.zip", ".txt")
    processor.process_zip("test", "sample")

    with zipfile.ZipFile("test_filename.zip", "r") as zf:
        assert "sample1.txt" in zf.namelist()
        assert "subfolder/sample3.txt" in zf.namelist()

    os.remove("test_filename.zip")
    os.remove("test_filename.zip.bak")


def test_cli_text_replace():
    create_zip_file("test_cli_text.zip")
    result = subprocess.run(
        ["python", "zipfnr.py", "text", "test_cli_text.zip", ".txt", "hello", "hi"],
        capture_output=True,
    )
    assert result.returncode == 0

    with zipfile.ZipFile("test_cli_text.zip", "r") as zf:
        assert zf.read("test1.txt").decode("utf-8") == "hi world"
        assert zf.read("subfolder/test3.txt").decode("utf-8") == "nested hi"

    os.remove("test_cli_text.zip")
    os.remove("test_cli_text.zip.bak")


def test_cli_filename_replace():
    create_zip_file("test_cli_filename.zip")
    result = subprocess.run(
        [
            "python",
            "zipfnr.py",
            "filename",
            "test_cli_filename.zip",
            ".txt",
            "test",
            "sample",
        ],
        capture_output=True,
    )
    assert result.returncode == 0

    with zipfile.ZipFile("test_cli_filename.zip", "r") as zf:
        assert "sample1.txt" in zf.namelist()
        assert "subfolder/sample3.txt" in zf.namelist()

    os.remove("test_cli_filename.zip")
    os.remove("test_cli_filename.zip.bak")
