""" Abstract class module """

from abc import ABC, abstractmethod
from typing import List
import subprocess
from pathlib import Path
import csv
from docx import Document
from error_engine import InvalidFileError
from .model import QuoteModel


class IngestorInterface(ABC):
    """Check if data can be ingested"""

    @classmethod
    @abstractmethod
    def can_ingest(cls, filepath: str) -> bool:
        """Check if file is ingestible"""

    @classmethod
    @abstractmethod
    def parse(cls, filepath: str) -> List[QuoteModel]:
        """Return list of quotes from file"""


class TextIngestor(IngestorInterface):
    """Ingests TXT using base abstract interface"""

    @classmethod
    def can_ingest(cls, filepath: str) -> bool:
        """Check if file is ingestible"""
        file_extension = Path(filepath).suffix
        if file_extension != ".txt":
            return False
        return True

    @classmethod
    def parse(cls, filepath: str) -> List[QuoteModel]:
        """Return list of quotes from TXT file"""
        quotes = []
        with open(filepath, mode="r", encoding="utf-8") as infile:
            for line in infile.readlines():
                if len(line.split(" - ")) == 2:
                    body, author = line.split(" - ")

                    quotes.append(QuoteModel(body, author))
        return quotes


class CSVIngestor(IngestorInterface):
    """Ingests CSV using base abstract interface"""

    @classmethod
    def can_ingest(cls, filepath: str) -> bool:
        """Check if file is ingestible"""
        file_extension = Path(filepath).suffix
        if file_extension != ".csv":
            return False
        return True

    @classmethod
    def parse(cls, filepath: str) -> List[QuoteModel]:
        """Return list of quotes from CSV file"""
        quotes = []
        with open(filepath, mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            next(reader)
            for line in reader:
                body, author = line
                quotes.append(QuoteModel(body, author))
        return quotes


class PDFIngestor(IngestorInterface):
    """Ingests PDF using base abstract interface"""

    @classmethod
    def can_ingest(cls, filepath: str) -> bool:
        """Check if file is ingestible"""
        file_extension = Path(filepath).suffix
        if file_extension != ".pdf":
            return False
        return True

    @classmethod
    def parse(cls, filepath: str) -> List[QuoteModel]:
        """Return list of quotes from PDFfile"""
        quotes = []
        tmp_filepath = "tmp.txt"

        call = subprocess.Popen(
            ["pdftotext", filepath, tmp_filepath], stdout=subprocess.PIPE
        )
        _, err = call.communicate()
        if err is not None:
            raise Exception("failed to create tmp file")

        status = call.wait()
        if status != 0:
            print("Command failed with return code", status)

        with open(tmp_filepath, mode="r", encoding="utf-8") as infile:
            lines = infile.readline().strip("\n").split(' "')
            for line in lines:
                body, author = line.replace('"', "").split(" - ")
                quotes.append(QuoteModel(body, author))

        status = subprocess.call(["rm", "-R", tmp_filepath])
        if status != 0:
            print("Command failed with return code", status)

        return quotes


class DocxIngestor(IngestorInterface):
    """Ingests DOCX using base abstract interface"""

    @classmethod
    def can_ingest(cls, filepath: str) -> bool:
        """Check if file is ingestible"""
        file_extension = Path(filepath).suffix
        if file_extension != ".docx":
            return False
        return True

    @classmethod
    def parse(cls, filepath: str) -> List[QuoteModel]:
        """Return list of quotes from DOCXfile"""
        with open(filepath, mode="rb") as infile:
            quotes = []
            document = Document(infile)
            for paragraph in document.paragraphs:
                if (
                    len(str(paragraph.text).replace('"', "")
                        .strip("").split(" - ")) == 2
                ):
                    body, author = (
                        str(paragraph.text).replace('"', "")
                        .strip("").split(" - ")
                    )
                    quotes.append(QuoteModel(body, author))

            return quotes


class Ingestor:
    """Ingestor class that selects right ingestor based on file path"""

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse and return retrieved quotes from file"""
        quotes = []
        if TextIngestor.can_ingest(path):
            quotes.extend(TextIngestor.parse(path))
        elif DocxIngestor.can_ingest(path):
            quotes.extend(DocxIngestor.parse(path))
        elif PDFIngestor.can_ingest(path):
            quotes.extend(PDFIngestor.parse(path))
        elif CSVIngestor.can_ingest(path):
            quotes.extend(CSVIngestor.parse(path))
        elif PDFIngestor.can_ingest(path):
            quotes.extend(PDFIngestor.parse(path))
        else:
            raise InvalidFileError(path)

        return quotes
