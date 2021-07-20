# main class for highlight_extractor
# Based on https://stackoverflow.com/a/62859169/562769

import csv
import os
import pandas as pd
import string

from typing import List, Tuple
import fitz

class highlight_parser():
    def __init__(self,input_pdf,output_xlsx):
        #pdf parameters
        self.input_pdf = input_pdf

        #excel parameters
        self.output_xlsx = output_xlsx
        self.fields = ["Highlights"]
        self.csv_out = "temp_file.csv"

    def _parse_highlight(self,annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
        points = annot.vertices
        quad_count = int(len(points) / 4)
        sentences = []
        for i in range(quad_count):
            # where the highlighted part is
            r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

            words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
            sentences.append(" ".join(w[4] for w in words))
        sentence = " ".join(sentences)
        return sentence

    def _cleanText(self,phrase):
        phrase = phrase.strip()
        phrase = ''.join(x for x in phrase if x in string.printable)
        #print(phrase)
        # phrase = phrase.encode("utf-8",'ignore')
        return phrase


    def handle_page(self,page):
        wordlist = page.getText("words")  # list of words on page
        wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

        highlights = []
        annot = page.firstAnnot
        while annot:
            if annot.type[0] == 8:
                highlights.append(self._parse_highlight(annot, wordlist))
            annot = annot.next
        return highlights


    def main(self,filepath=None,static=False):
        if filepath != None:
            doc = fitz.open(filepath)
        else:
            doc = fitz.open(self.input_pdf)

        highlights = []
        for page in doc:
            highlights += self.handle_page(page)

        if static == True:
            return highlights
        else:
            #internal form for going direct from highlights to excel file
            self.csv_save(highlights,file_name=self.csv_out)
            self.csv_to_xlsx(self.csv_out,xlsx_path=self.output_xlsx,delete_csv=True)

    def csv_save(self,rows,file_name="highlight.csv"):
    	with open(file_name, 'w') as f:
    	      
    	    # using csv.writer method from CSV package
    	    write = csv.writer(f)
    	      
    	    write.writerow(self.fields)
    	    for phrase in rows:
    	    	write.writerow([self._cleanText(phrase)])

    def csv_to_xlsx(self,csv_path,xlsx_path = 'output.xlsx',delete_csv = True):
        df_new = pd.read_csv(csv_path)
        writer = pd.ExcelWriter(xlsx_path)
        df_new.to_excel(writer, index = False)
        writer.save()

        if delete_csv == True:
            os.remove(self.csv_out)

if __name__ == "__main__":
    input_pdf = r"pdf_input/test_highlight.pdf"
    output_file_name = r"excel outputs/highlights.xlsx"

    highlight_class = highlight_parser(input_pdf,output_file_name)
    highlight_class.main() #highlights text parser