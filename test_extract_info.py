from pprint import pprint
from extract_info import *

def main():
    UPLOAD_FOLDER = './testdata'
    dir = os.listdir(UPLOAD_FOLDER)
    results = []
    if len(dir) == 0:
        print("There is no file uploaded.")
    else:
        for p in Path(UPLOAD_FOLDER).glob("*.pdf"):
            # print(p)
            text = pdf_to_text(p)
            new_lines = clean_text(text)
            tokens = tokenize(new_lines)
            # print(tokens)
            results.append(extract_info(tokens))

    if results:
        pprint(results)
    else:
        print("It failed to crawl information from invoice.")


if __name__ == '__main__':
    main()
