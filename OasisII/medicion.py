from PDFConverter import PDFConverter
import time


c = PDFConverter()

c.open_file('../test/test.pdf')

starttime = time.time()
c.convert_pdf_to_png()
endtime = time.time()

print("Using Inkscape: %f" % (endtime - starttime))

cc = PDFConverter()

cc.open_file('../test/test.pdf')

starttime = time.time()
cc.convert_pdf_to_png2()
endtime = time.time()

print("Using pdf2image: %f" % (endtime - starttime))
