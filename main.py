from copy import deepcopy
import time
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import os
import pikepdf

import requests
from bs4 import BeautifulSoup
import time
import re

def download_file_from_website():
    TARGET_URL = "https://www.ladispe.polito.it/corsi/ContrAutoInf270/"
    html = requests.get(TARGET_URL)
    soup = BeautifulSoup(html.text, features="lxml")
    a_tags = soup.find_all('a')
    for a in a_tags:
        href = a.get('href')
        if href and href.endswith(".pdf"):
            text_content = a.get_text(strip=True)
            clean_name = re.sub(r'[\\/*?:"<>|\n\r\t]', '', text_content)
            clean_name = clean_name.strip()
            if not clean_name:
                clean_name = href.split('/')[-1].replace('.pdf', '')
            file_url = TARGET_URL + href
            response = requests.get(file_url)
            with open(f"{clean_name}.pdf", 'wb') as pdf:
                pdf.write(response.content)    
            print(f"Salvato: {clean_name}.pdf")
            time.sleep(1)
            
def search_word_in_files(all_files: list):
    word_to_search = input("Che parola vuoi cercare nei pdf? ")
    for file in all_files:
        if file.endswith(".pdf") and os.path.isfile(file):
            reader = PdfReader(file, strict=False)
            print(f"Sto cercando in {file}")
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                if word_to_search.lower() in text.lower():
                    print(f"Word trovata in {file}")
                    
def decrypt(pdf_files: list):
    i = 0
    for file in pdf_files:
        try:
            with pikepdf.open(file, allow_overwriting_input=True) as pdf:
                pdf.save(file)
            print(f"Ho salvato {file} aggirando i permessi di Taragna")
            i+=1
            os.remove(file)
        except Exception as e:
            print(e)
            continue
        

    
def main():
    download_file=input("Vuoi scaricare i dati dal sito? (yes/no): ")
    if download_file=="yes":
       download_file_from_website()
    all_files = os.listdir()
    list_copy = deepcopy(all_files)
    for file in all_files:
        if not os.path.isfile(file) or not file.endswith(".pdf"):
            list_copy.remove(file)
    choise = int(input("What do you want to do?\n1.Search word in file\n2. Decrypt pdf\n3. delete all pdf\nEnter the option:"))
    match (choise):
        case 1:
            search_word_in_files(list_copy)
        case 2:
            decrypt(list_copy)
        case 3:
            for file in list_copy:
                os.remove(file)
main()
