import unittest
from Oasis import PDFConverter
import os
import glob

TEST_FILE_PATH = os.path.dirname(os.path.abspath(__file__))


class TestPDFConverter(unittest.TestCase):
    def setUp(self):
        self.FILE_PATH = PDFConverter.FILE_PATH
        self.testing_PDF = os.path.join(TEST_FILE_PATH, 'test.pdf')

    def test_creation_working_dir(self):
        pdfconverter = PDFConverter.PDFConverter()
        tmp_path = os.path.join(
            self.FILE_PATH,
            'temp')

        self.assertEqual(os.path.exists(tmp_path), True)
        pdfconverter.remove_working_dir()
        self.assertEqual(os.path.exists(tmp_path), False)

    def test_open_pdf_file(self):
        pdfconverter = PDFConverter.PDFConverter()
        result = pdfconverter.open_file(self.testing_PDF)

        self.assertEqual(result, 3)
        self.assertEqual(pdfconverter.number_of_pages, 10)
        self.assertIsNotNone(pdfconverter.pdfFileObj)

    def test_convert_pdf_to_svg(self):
        pdfconverter = PDFConverter.PDFConverter()
        result = pdfconverter.open_file(self.testing_PDF)
        tmp_path = os.path.join(
            self.FILE_PATH,
            'temp', '*.svg')

        pdfconverter.convert_pdf_to_svg()
        tt = glob.glob(tmp_path)
        temp_path = list(map(lambda x: os.path.basename(x), tt))

        self.assertEqual(len(temp_path), 10)

        pdfconverter.remove_working_dir()
        self.assertEqual(os.path.exists(tmp_path), False)

    def test_convert_pdf_to_png(self):
        pdfconverter = PDFConverter.PDFConverter()
        result = pdfconverter.open_file(self.testing_PDF)
        tmp_path = os.path.join(
            self.FILE_PATH,
            'temp', '*.png')

        pdfconverter.convert_pdf_to_png()
        tt = glob.glob(tmp_path)
        temp_path = list(map(lambda x: os.path.basename(x), tt))
        self.assertEqual(len(temp_path), 10)

        pdfconverter.remove_working_dir()
        self.assertEqual(os.path.exists(tmp_path), False)


if __name__ == '__main__':
    unittest.main()
