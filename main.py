import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import os

download_file=input("Vuoi scaricare i dati dal sito?")
if download_file=="yes":
    TARGET_URL = "https://www.ladispe.polito.it/corsi/ContrAutoInf270/"
    html = requests.get(TARGET_URL)
    soup = BeautifulSoup(html.text)
    a_tags = soup.find_all('a')
    i = 0
    for a in a_tags:
        if a['href'].endswith(".pdf"):
            response = requests.get(TARGET_URL + a.get('href'))
            pdf = open("pdf"+str(i)+".pdf", 'wb')
            pdf.write(response.content)
            pdf.close()
            i += 1

all_files = os.listdir()

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
