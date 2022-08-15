import os
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join
import time

import numpy as np
import pandas as pd
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import requests

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from Config.sql_config import engine
import mysql.connector


# POST
def regex_court_sentence_file():
    """
    Function to regex the folder with the only file, and returns us the data. It deletes the file also.
    :return:
    """
    mypath = r"C:\Users\lenovo\PycharmProjects\pythonProject\pdf"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in onlyfiles:
        newstr = os.path.join(mypath, i)
        reader = PdfReader(newstr)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        ## ROJ

        m = re.search('[R][o][j].*', text)
        if m:
            roj = m.group(0)
            list_roj = roj.split("-")
            roj = list_roj[0].strip()
            ats = roj[9:]
            ecli = list_roj[1].strip()
        else:
            ecli = "couldn't find"
            ats = "Couldn't find"
        print(ats)

        ##cendoj id
        m = re.search('\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d', text)
        if m:
            cendoj_id = m.group(0)  ## string
            cendoj_id = int(cendoj_id)  ## int
        else:
            cendoj_id = 0
        print(cendoj_id)

        ##organo
        m = re.search('[Ó][r][g][a][n][o].*', text)
        if m:
            organo = m.group(0)  ## string
            organo_total = organo.strip("Órgano:")
            list_1 = organo_total.split(".")
            tribunal = list_1[0]
            print(tribunal)
            sala = list_1[1].strip()
            print(sala)
        else:
            tribunal = np.nan
            sala = np.nan

        ## sede
        m = re.search('[S][e][d][e]\W.*', text)
        if m:
            sede = m.group(0)  ## string
            sede = sede[6:]  ## int
        else:
            sede = "Couldn't find"
        print(sede)

        # seccion
        m = re.search('[S][e][c][c][i][ó][n]\W.*', text)
        if m:
            seccion = m.group(0)
            seccion = int(seccion[9:])
        else:
            seccion = "Couldn't find"
        print(seccion)

        # fecha
        m = re.search('[F][e][c][h][a ]\W\d.*', text)
        if m:
            fecha = m.group(0)
            fecha = fecha[6:]
            fecha = fecha[0:7] + fecha[7 + 2::]
            fecha = datetime.strptime(fecha, '%d/%m/%y')  # datetime object
            print(fecha)
        else:
            fecha = np.nan
        # no recurso
        m = re.search('[N][º] [d][e] [R][e][c].*', text)
        if m:
            recurso_n = m.group(0)
            recurso_n = recurso_n[15:]
        else:
            recurso_n = "Couldn't find"
        print(recurso_n)

        # juez:
        m = re.search('[P][o][n][e][n][t][e]\W.*', text)
        if m:
            juez = m.group(0)
            juez = juez[8:]
        else:
            juez = "Couldn't find"
        print(juez)

        # letrado
        m = re.search('[L][e][t][r][a][d][o]\W.*', text)
        if m:
            letrado = m.group(0)
            letrado = letrado.removeprefix('Letrado de la Administración de Justicia: Ilmo. Sr. D. ')
        else:
            letrado = "Couldn't find"

        # REMOVES FILE, PUT IT WHEN EVERYTHING ELSE WORKS.

        myfile = "./pdf/" + i
        if os.path.isfile(newstr):
            os.remove(newstr)
        else:  ## Show an error ##
            print("Error: %s file not found" % myfile)

        data_sentence = (ats, ecli, cendoj_id, tribunal, sala, sede, seccion, fecha, recurso_n, juez, letrado, text)

        print(data_sentence)
        return data_sentence

    # PODEM FICAR EL LINK DE LA SENTENCIA, i altres coses pero crec que ja esta be.


def uploading_sql(data_sentence):
    conn = mysql.connector.connect(
        user='root', password='password', host='127.0.0.1', database='sentencias_españa')
    cursor = conn.cursor()
    insert_stmt = (
        "INSERT INTO sentencias(ATS, ECLI, Cendoj_id, Tribunal, Sala, Sede, Seccion, Fecha, Numero_recurso, Juez, Letrado, Full_text)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    cursor.execute(insert_stmt, data_sentence)

    # Commit your changes in the database
    conn.commit()

    # Rolling back in case of error
    conn.rollback()



def downloading_sentence(url):
    """
    This function takes an url of a CENDOJ sentence, downloads it, and save it.
    :param url: string, url of the CENDOJ sentence
    :return: it doesn't return anything.
    """
    # Url of the cendoj sentence page. It finds the href link of the direct download
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    href = soup.find("object", {"id": "objtcontentpdf"})
    href = href.find("a", href=True)
    href = "https://www.poderjudicial.es" + href["href"]

    # BEAUTIFUL SOUP ALTERNATIVE:
    location = r"C:\Users\lenovo\PycharmProjects\pythonProject\pdf"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'address': location}

    # sending get request and saving the response as response object
    i = requests.get(url=href, params=PARAMS)

    # Write content in pdf file
    with open(r"C:\Users\lenovo\PycharmProjects\pythonProject\pdf\sentence.pdf", 'wb') as f:
        f.write(i.content)

    # SELENIUM ALTERNATIVE:

    # where to download selenium
    # path_loc = r"C:\Users\lenovo\PycharmProjects\pythonProject\pdf"
    # options = Options()
    # options.add_argument(r"[C:\Users\lenovo\PycharmProjects\pythonProject\chromedriver.exe]")
    # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    # general download pdf options
    chrome_prefs = {
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "download.open_pdf_in_system_reader": False,
        "profile.default_content_settings.popups": 0,
        # add location preference...
        # "download.default_directory": path_loc
    }

    # apply them
    # options.add_experimental_option("prefs", chrome_prefs)
    # driver = webdriver.Chrome(options=options)

    # downloads the pdf
    # driver.get(href)

    # wait 6 seconds
    # time.sleep(6)

    # Location + name of the pdf
    m = re.search('\d\d\d\d\d\d\d\d', href)
    if m:
        name_file = m.group(0)
    name_file = str(name_file) + ".pdf"
    mypath = r"C:\Users\lenovo\PycharmProjects\pythonProject\pdf"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    file = onlyfiles[0]

    # We put it a new name because I CAN
    old_file = os.path.join(mypath, file)
    new_file = os.path.join(mypath, name_file)
    os.rename(old_file, new_file)


from Config.sql_config import engine


def get_all_from_sql():
    query = (
        f"SELECT ATS, ECLI, Cendoj_id, Tribunal, Sala, Sede, Seccion, Fecha, Numero_recurso, Juez, Letrado FROM \n"
        f"        sentencias_españa.sentencias;")
    df = pd.read_sql_query(query, con=engine)
    return df.to_dict(orient='records')


def get_count_with_variable(variable):
    query = f"""SELECT {variable}, count({variable}) as 'Sentencias_Totales' FROM sentencias_españa.sentencias Group by {variable} Order by Sentencias_Totales DESC;"""
    df = pd.read_sql_query(query, con=engine)
    return df.to_dict(orient='records')


def get_all_with_variable(variable, name):
    query = f"""SELECT * FROM sentencias_españa.sentencias Where {variable} = '{name}' Order by Fecha DESC;"""
    df = pd.read_sql_query(query, con=engine)
    return df.to_dict(orient='records')

def return_last_sql():
    query = f"""select * from sentencias_españa.sentencias Order by DESC Limit 1;"""
    df = pd.read_sql_query(query, con=engine)
    return df.to_dict(orient='records')
