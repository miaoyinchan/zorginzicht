import nltk
import os
import PyPDF2
import re
from itertools import zip_longest
from pathlib import Path
from nltk.tokenize import word_tokenize
from pprint import pprint

# TODO: Ask customer_id from frontend url then save it in table Inovice.
# TODO: get more invoices to test

amount_keywords = ['totaal']
health_care_providers_id = [{"12076154": "tandarts"}, {"24437187": "preventie"}]
polis_keywords = ['polisnummer']
invoice_keywords = ['factuurnummer']
rubbish_words = [':', 'incl', 'excl', 'btw', '-', '.', '•', '€']
info_names = ['amount', 'caretype', 'polis number', 'invoice number']


def pdf_to_text(pdffile):
    pdffileobj=open(pdffile,'rb')
    pdfreader=PyPDF2.PdfFileReader(pdffileobj)
    x=pdfreader.numPages
    text = ""
    for i in range(x):
        pageobj = pdfreader.getPage(i)
        text += pageobj.extractText()
    # print(text)
    return text


def clean_text(text):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        for word in word_tokenize(line):
            if word.lower() not in rubbish_words:
                new_lines.append(word)

    return new_lines


def tokenize(new_lines):
    return [t for line in new_lines for t in word_tokenize(line)]


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


def only_amount(token):
    result = ''
    for l in token:
        if l.isnumeric() or l == ',':
            result += l
    return result


def only_number(token):
    result = ''
    for l in token:
        if l.isnumeric():
            result += l
    return result


def get_invoice_nr(tokens):
    for t1, t2 in zip_longest(tokens, tokens[1:]):
        # print("t1: ", t1)
        if t1.lower() in invoice_keywords:
            return ("invoice number", only_number(t2))


def get_amount(tokens):
    results = set()
    for t1, t2 in zip_longest(tokens, tokens[1:]):
        if t1.lower() in amount_keywords:
            # print(t1, t2)
            results.add(("amount", only_amount(t2)))

    return max(results)


def get_caretype(tokens):
    for t in tokens:
        for values in health_care_providers_id:
            value = values.get(t)
            if value:
                return ("caretype", value)


def get_polis_number(tokens):
    for t1, t2 in zip_longest(tokens, tokens[1:]):
        if t1.lower() in polis_keywords and has_numbers(t2) == True:
            # print(t1, t2)
            return ("policy number", only_number(t2))


def get_date(tokens):
    for t1, t2 in zip_longest(tokens, tokens[1:]):
        if t1.lower() == 'datum':
            # print(t1, t2)
            return ("invoice_date", t2)


def extract_info(tokens):
    final_res = set()
    final_res.add(get_invoice_nr(tokens))
    final_res.add(get_polis_number(tokens))
    final_res.add(get_caretype(tokens))
    final_res.add(get_amount(tokens))
    final_res.add(get_date(tokens))

   # Check if all needed info is available in invoice for extracting
    extracted_info_names = []
    for r in final_res:
        if r != None:
            extracted_info_names.append(r[0])

     # Put "NA in invoice" if the information is not available in invoice
    if len(extracted_info_names) < len(info_names):
        for e in info_names:
            # print(e)
            if e not in extracted_info_names:
                final_res.add((e, "NA"))
            # print("DEBUG:", final_res)

    # Remove None value from the result
    final_final_res = set()
    for e in final_res:
        if e != None:
            final_final_res.add(e)

    final_final_final_res = dict(final_final_res)

    return final_final_final_res


# def main():
#     UPLOAD_FOLDER = './uploads'
#     dir = os.listdir(UPLOAD_FOLDER)
#     results = []
#     if len(dir) == 0:
#         print("There is no file uploaded.")
#     else:
#         for p in Path(UPLOAD_FOLDER).glob("*.pdf"):
#             print(p)
#             text = pdf_to_text(p)
#             new_lines = clean_text(text)
#             tokens = tokenize(new_lines)
#             print(tokens)
#             results.append(extract_info(tokens))

#     if results:
#         pprint(results)
#     else:
#         print("It failed to crawl information from invoice.")


# if __name__ == '__main__':
#     main()
