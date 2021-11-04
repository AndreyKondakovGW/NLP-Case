
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import io


class Parser(object):
    @staticmethod
    def parsePDF(filename):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams) 
        fp = filename
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
            interpreter.process_page(page)

        fp.close()
        device.close()
        text = retstr.getvalue()
        retstr.close()
        
        with open(os.path.dirname(os.path.abspath(__file__)) + '\..\..\\tmp\out.txt', mode='w', encoding='utf-8') as f :
            f.write(text)
        return text

    @staticmethod
    def getDescription(filename):
        with open(filename, mode='r', encoding='utf-8', errors="replace") as f :
            description = re.split(r'ABSTRACT|1. INTRODUCTION|Keywords:|Contents|Abstract. |1. Introduction',f.read())[1].strip()
        return description

    def get_text_from_pdf(filename):
        Parser.parsePDF(filename)
        filename = os.path.dirname(os.path.abspath(__file__)) + '\..\..\\tmp\out.txt'
        with open(filename, mode='r', encoding='utf-8', errors="replace") as f :
            text = f.read()
        return text

    @staticmethod
    def get_description_from_pdf(filename):
        Parser.parsePDF(filename)
        description = Parser.getDescription(os.path.dirname(os.path.abspath(__file__)) + '\..\..\\tmp\out.txt')
        return description
