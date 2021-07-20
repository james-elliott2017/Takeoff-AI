# main class for highlight_extractor
# Based on https://stackoverflow.com/a/62859169/562769

import csv
import os
import pandas as pd
import string

from typing import List, Tuple
import fitz

def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
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


def handle_page(page):
    wordlist = page.getText("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

    highlights = []
    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights


def main(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return highlights

def csv_save(fields,rows,file_name="highlight.csv"):
	with open(file_name, 'w') as f:
	      
	    # using csv.writer method from CSV package
	    write = csv.writer(f)
	      
	    write.writerow(fields)
	    for phrase in rows:
	    	write.writerow([_cleanText(phrase)])

def _cleanText(phrase):
	phrase = phrase.strip()
	phrase = ''.join(x for x in phrase if x in string.printable)
	#print(phrase)
	# phrase = phrase.encode("utf-8",'ignore')
	return phrase

def csv_to_xlsx(csv_path,xlsx_path = 'output.xlsx'):
	df_new = pd.read_csv(csv_path)
	writer = pd.ExcelWriter(xlsx_path)
	df_new.to_excel(writer, index = False)
	writer.save()

if __name__ == "__main__":
    highlights = main("02-117750_SPC_A.pdf")
    fields = ["highlights"]
    csv_out = "highlights.csv"
    #print(highlights,"\n\n")

    csv_save(fields,highlights,file_name=csv_out)
    csv_to_xlsx(csv_out)
    os.remove(csv_out)