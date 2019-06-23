"""This file is part added by Alados Automatizaciones for Oasis Controller.
"""


from PyQt5.QtGui import QPixmap, QColor, QImage
from PyQt5 import QtCore
from numpy import *
import os
import sys
import subprocess
import shutil
import PyPDF2
import multiprocessing
import stat

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

def convert_png2(fname: str, output_dir: str, dpi: int) -> None:
    """Convert a pdf to bitmap file
    pdf2png library

    Returns
    -------
    None
    """
    # XXX: esto tiene que resolverse con https://github.com/Belval/pdf2image/issues/69
    o = '%s.jpg' % os.path.basename(fname).split('.')[0]
    convert_from_path(fname,
                      output_folder=output_dir,
                      fmt='jpg',
                      transparent=True,
                      thread_count=4,
                      output_file=o,
                      dpi=dpi)

def convert_png(fname: str, output_dir: str, dpi: int) -> None:
    """Convert a pdf to bitmap file

    Returns
    -------
    None
    """
    svg_name, ext = os.path.splitext(os.path.basename(fname))
    out = subprocess.Popen(['inkscape', fname,
                            '--export-png=%s' % (os.path.join(output_dir,
                                                              svg_name + '.png')),
                            '-d %d' % (dpi)],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

try:
    from pdf2image  import convert_from_path
    convert_png = convert_png2
except ImportError:
    pass


class PDFConverter:
    def __init__(self):
        self.dpi = 300  # default dpi to 300
        self.type_file = 3  # type of file, 0 for nothing,
        # 1 for bitmap, 2 for vector
        # 3 for pdf
        self.file_path = ''
        self.file_name = ''
        self.pdf_content = list()
        self.working_dir = os.path.join(FILE_PATH, 'temp')

        if not os.access(self.working_dir, os.W_OK):
            os.chmod(self.working_dir, stat.S_IWUSR)

        if os.path.exists(self.working_dir):
            shutil.rmtree(self.working_dir)

        os.mkdir(self.working_dir)

        self.list_pages_name = list()
        self.number_of_pages = 0

        self.pdfReader = None
        self.pdfFileObj = None

    def open_file(self, file_path: str) -> int:
        """Open a file

        Parameters
        ----------
        file_path : str
            path where is the file

        Returns
        -------
        Return 3 if is secessfully
        -1 if file_path == ''
        1 if file not exist
        2 if not pdf
        """

        # is empty the file_path?
        if not len(file_path):
            self.type_file = 0
            return -1

        self.file_path = file_path

        # exist the file?
        if not os.path.exists(self.file_path) or not os.path.isfile(self.file_path):
            self.file_type = 0
            return 1

        extension = os.path.splitext(self.file_path)[1]

        # are u a pdf file?
        if not extension.lower() == '.pdf':
            self.type_file = 0
            self.type_path = ''
            return 2

        # yes I am a PDF file
        self.type_file = 3
        # save the name
        self.file_name = os.path.basename(self.file_path)

        # Open the PDF
        # if self.get_data_from_pdf() == 1:
        #     return 3
        # else:
        #     return 0

        self.CreatePDFObj()
        return 3

    def CreatePDFObj(self):
        """Create PDF Object"""
        self.pdfFileObj = open(self.file_path, 'rb')

        self.pdfReader = PyPDF2.PdfFileReader(self.pdfFileObj)
        self.number_of_pages = self.pdfReader.numPages

    def set_dpi(self, dpi: int) -> None:
        """Set DPI

        Parameters
        ----------
        dpi : int
            dpi
        """
        self.dpi = dpi

    def get_dpi(self) -> int:
        """Get DPI"""
        return self.dpi

    def save_content_from_linux(self) -> int:
        """Save content of the pdf form linux.

        Returns
        -------
        0  if failed
        1 successfull
        """
        out = subprocess.Popen(['pdftotext', '-layout', '-r',
                                str(self.dpi), self.file_path, '-'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        if stderr is not None:
            return 0
        self.pdf_content = str(stdout).split('\n')[0].split('\\n')

        return 1

    def save_content_from_windows(self) -> int:
        """Save the content of the pdf from windows.

        Returns
        -------
        0  if failed
        1 successfull
        """
        pdftotext_exe_path = os.path.join(FILE_PATH,
                                          'WinpdfTotext',
                                          'pdftotext.exe')

        out = subprocess.Popen([pdftotext_exe_path, '-layout', '-r',
                                str(self.dpi), self.file_path, '-'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()

        if stderr is not None:
            return 0

        self.pdf_content = str(stdout).split('\n')[0].split('\\n')
        return 1

    def get_data_from_pdf(self) -> int:
        """Extract data form PDF

        Returns
        -------
        1 if successfull
        0 if failed
        """

        if sys.platform is 'linux':
            result = self.save_content_from_linux()
        elif 'win' in sys.platform:
            result = self.save_content_from_windows()
        else:
            print("not supported systemOperating")
            return -1

        return result

    def split_pdf(self) -> None:
        """split pages of pdf on different pdf

        Returns
        -------
        None
        """

        if os.path.exists(self.working_dir):
            shutil.rmtree(self.working_dir)

        os.mkdir(self.working_dir)

        for i in range(self.number_of_pages):
            pdfWriter = PyPDF2.PdfFileWriter()
            outputpdf_name = self.file_name.split('.')[0] + str(i) + '.pdf'

            pdfWriter.addPage(self.pdfReader.getPage(i))

            with open(os.path.join(self.working_dir, outputpdf_name), 'wb') as f:
                pdfWriter.write(f)

    def convert_svg(self, fname: str, output_dir: str) -> None:
        """Convert a pdf to svg file

        Returns
        -------
        None
        """
        svg_name, ext = os.path.splitext(os.path.basename(fname))
        out = subprocess.Popen(['inkscape', fname,
                                '--export-plain-svg=%s' % (os.path.join(output_dir,
                                                                        svg_name + '.svg'))],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()

    def convert_pdf_to_svg(self) -> None:
        """Convert the pdf pages to svg

        Returns
        -------
        None
        """
        self.split_pdf()
        list_dir = os.listdir(self.working_dir)

        for ld in list_dir:
            self.convert_svg(os.path.join(self.working_dir,
                                          ld), self.working_dir)
        self.pdfFileObj.close()

    def remove_working_dir(self) -> None:
        """Remove the working dir

        Returns
        -------
        None
        """
        if os.path.exists(self.working_dir):
            shutil.rmtree(self.working_dir)

    def convert_png(self, fname: str, output_dir: str) -> None:
        """Convert a pdf to bitmap file

        Returns
        -------
        None
        """
        svg_name, ext = os.path.splitext(os.path.basename(fname))
        out = subprocess.Popen(['inkscape', fname,
                                '--export-png=%s' % (os.path.join(output_dir,
                                                                  svg_name + '.png')),
                                '-d %d' % (self.dpi)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()

    def convert_pdf_to_png2(self) -> None:
        """Convert the pdf page to png using
              Returns
        -------
        None
        """

        self.split_pdf()
        list_dir = os.listdir(self.working_dir)
        from pdf2image  import convert_from_path
        for ld in list_dir:
            # XXX: esto tiene que resolverse con https://github.com/Belval/pdf2image/issues/69
            o = '%s.png' % ld.split('.')[0]
            # o = ld.split('.')[0]
            convert_from_path(os.path.join(self.working_dir,
                                           ld),
                              output_folder=self.working_dir,
                              fmt='png',
                              thread_count=10,
                              transparent=True,
                              output_file=o,
                              dpi=self.dpi)

        self.pdfFileObj.close()

    def convert_pdf_to_png(self) -> None:
        """Convert the pdf pages to png

        Returns
        -------
        None
        """
        self.split_pdf()
        list_dir = os.listdir(self.working_dir)
        
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            res = [pool.apply_async(convert_png, (
                os.path.join(self.working_dir, ld), self.working_dir, self.dpi)) for ld in list_dir]
             
            [r.wait() for r in res]
        self.pdfFileObj.close()

