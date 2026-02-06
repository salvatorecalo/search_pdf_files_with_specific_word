import os
from pypdf import PdfReader

dir_path = input("Insert the directory in which you want to search: ")
word_to_search = input("Insert the word to search: ")
os.chdir(f"./{dir_path}")
subfolders = os.listdir(".")
for folder in subfolders:
    if os.path.isdir(folder):
        os.chdir(folder)
        all_files = os.listdir(".")
        for file in all_files:
            reader = PdfReader(file)
            for i in range (len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                if word_to_search in text.lower():
                    print(f"TROVATO FILE {file}")
        os.chdir("../")