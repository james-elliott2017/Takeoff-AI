# main class for highlight_extractor
# Based on https://stackoverflow.com/a/62859169/562769

import csv
import os
import pandas as pd
import string
import numpy as np
import copy

from typing import List, Tuple
import fitz

class highlight_parser():
    def __init__(self,input_pdf,output_xlsx):
        #pdf parameters
        self.input_pdf = input_pdf
        self.shrink_constant = .55
        #excel parameters
        self.output_xlsx = output_xlsx
        self.fields = ["Highlights"]
        self.csv_out = "temp_file.csv"

    def _parse_highlight(self,annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
        def shrink_rect(r,scalar):
            """
            r should take form of (tl,br) or form of
            (TLcol,TLrow,BRcol,BRrow)
            """
            center_deltas = ((r[2]-r[0])/2,(r[3]-r[1])/2)
            center_y,center_x = (r[0]+center_deltas[0],r[1]+center_deltas[1])

            scaled_y,scaled_x = tuple(x*scalar for x in center_deltas)
            
            updated_r = (
                r[0],center_x-scaled_x,
                r[2],center_x+scaled_x)
            return updated_r
        ####################################
        points = annot.vertices
        if type(points) != type([]):
            return None
        quad_count = int(len(points) / 4)
        sentences = []
        for i in range(quad_count):
            # where the highlighted part is
            r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect
            r = shrink_rect(r,self.shrink_constant)
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


    def handle_page(self,page,split_colors=True):
        wordlist = page.getText("words")  # list of words on page
        wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

        #Organize by Color
        if split_colors == True:
            annot = page.firstAnnot
            self.fields = []
            while annot:
                if annot.colors["stroke"] not in self.fields:
                    self.fields.append(annot.colors["stroke"])
                annot = annot.next

            highlights = [[] for x in self.fields]
            annot = page.firstAnnot
            while annot:
                if annot.type[0] == 8:
                    color_column = self.fields.index(annot.colors["stroke"])
                    try:
                        clean_sentence = self._cleanText(self._parse_highlight(annot, wordlist))
                        highlights[color_column].append(clean_sentence)
                    except:
                        print("Failure with Highlight")
		

                annot = annot.next
        else:
            highlights = []
            annot = page.firstAnnot
            #Loop through all annotations & grab highlights
            while annot:
                if annot.type[0] == 8:
                    clean_sentence = self._cleanText(self._parse_highlight(annot, wordlist))
                    highlights.append(clean_sentence)    
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

    def _LoL_padding(self,list_of_lists,pad="N/A"):
        """
        LoL: List of Lists
        take in a list of list,
        find longs list,
        appends <pad = "N/A"> until
        list-of-list can be converted to np.array of square form.
        """
        max_len = 0
        for row in list_of_lists:
            if len(row) > max_len:
                max_len = len(row)

        final_list = copy.copy(list_of_lists)
        for idx,row in enumerate(list_of_lists):
            if len(row) < max_len:
                difference = max_len - len(row)
                for i in range(difference):
                    final_list[idx].append(pad)

        final_list = np.asarray(final_list)
        return final_list



    def csv_save(self,rows,file_name="highlight.csv"):
        with open(file_name, 'w') as f:
    	    # using csv.writer method from CSV package
            write = csv.writer(f)
            for phrase in rows:
                if type(phrase) != type([]):
                    #Single-Color .CSV Creation
                    write.writerow(self.fields) #header
                    write.writerow([phrase])
                else:
                    #Multi-Color .CSV Creation
                    headers = "".join(["column_"+str(x)+"~" for x in range(len(self.fields))])

                    array = self._LoL_padding(rows)
                    array = array.transpose()
                    np.savetxt(f,array,fmt="%s",delimiter="~",header=headers
                        ,comments="")
                    break

    def csv_to_xlsx(self,csv_path,xlsx_path = 'output.xlsx',delete_csv = True):
        df_new = pd.read_csv(csv_path,delimiter="~")
        writer = pd.ExcelWriter(xlsx_path)
        df_new.to_excel(writer, index = False)
        writer.save()

        if delete_csv == True:
            os.remove(self.csv_out)

if __name__ == "__main__":
    input_pdf = r"pdf_input/test_highlight.pdf"
    output_file_name = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\highlight_extractor\excel outputs\highlights.xlsx"

    highlight_class = highlight_parser(input_pdf,output_file_name)
    highlight_class.main() #highlights text parser