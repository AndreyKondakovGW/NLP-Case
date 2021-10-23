
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
        with open(filename, mode='r') as f :
            description = re.split(r'Abstract\. |Contents|ABSTRACT|1\. INTRODUCTION|Keywords:|',f.read())[1].strip()
            print(re.split(r'Abstract\. |Contents|ABSTRACT|1\. INTRODUCTION|Keywords:|',f.read()))
        return description
