________________________________________________
</br>

# Project IV - Cendoj scrapping / API 

<img src="https://miro.medium.com/max/1200/1*kfOsUxggG5wDbDcxgC0Uwg.png" width="600" align="center">

### 1) Scrapping the Data from the Cendoj webpage.
### 2) Data managment from the Cendoj webpage to a SQL database.
### 3) Creating an API to interact with the data
#### Main technical tools: SQL, Regex, Flask, Python.
________________________________________________
</br>

#### By: Gaspar Masdeu Sans
#### Date: August 13st 2022

</br>
________________________________________________

### Cendoj - API query

<img src="https://www.davincigroup.es/wp-content/uploads/2020/02/Davinci-Group-clientes_CENDOJ.png" width="400" align="center">

The Judicial Documentation Center (Cendoj) is the technical body of the General Council of the Judiciary that is responsible for the official publication of case law, as well as other competencies in the field of documentation and knowledge management services.


# Part One: Data Scrapping and Data Pipeline.

## Scrapping CENDOJ:

To find the judicial data I need as a starting point the link of the court sentence we want to store, as data.

        https://www.poderjudicial.es/search/AN/openDocument/ced204cfbea1fe77/20220429

I have 3 main functions that help me throughout this process.  The three functions are defined in the Sql_tools.py file, in the Tools folder.

1)
        downloading_sentence(link)

This functions downloads the pdf attached to the main CENDOJ page and stores it in the pdf folder of the project. This function needs as argument the link of the sentence from the CENDOJ web page. Does not return anything.

2) 
        regex_court_sentence_file()

This function uses regex to find the data that I think is relevant, such as the Court, the Chamber, the CENDOJ id, the Judge, and of course, all the text of the sentence. It doesn't need any arguments as it simply iterates the "pdf" folder and picks up the text of the only pdf there. Once finished, it deletes all the files in the folder.

3) 
        uploading_sql(data_sentencia)

Function I use to upload the data collected by regex to my SQL database. Previously I have already created my database and set up the SQL data types needed to assimilate the data correctly.


<img src="https://i.gyazo.com/a50fce384f938423af0d2a105d9eb870.png" width="1200" align="center">



# Part 2: API 

Flask is a widely used micro web framework for creating APIs in Python. I have created an API so that any user can interact with the database, take information from there, and also upload new sentences, which will be assimilated homogeneously through the scraping functions.

<img src="https://raw.githubusercontent.com/ProgramoErgoSum/Tutoriales/master/v1/servidor-web-con-flask-en-raspberry-pi/img/flask.jpg" width="1200" align="center">

### 1 - Endpoint route for generating a Random Number:
As a special feature we created a special feature that generates a number between 0 and 1000</br>
this special feature is just to test the access to the endpoint route</br>

        http://127.0.0.1:5000/random-number 

### 2 - Endpoint route for a dictionary of all court sentences from the Database:
Getting query on all the court sentences that are uploaded to my SQL database.</br>
From oldest to newest, it returns all the data I have.

        http://127.0.0.1:5000/all

### 3 - Endpoint route for a dictionary of the number of court sentences grouped by a specific variable:
Get the query of all the diferent court sentences in my SQL Database./br>
It returns a dictionary with a count of all the same values into summary rows, like "find the number of court sentences made by all the Judges".</br>

      http://127.0.0.1:5000/count/<column>

A good example you can use:

      http://127.0.0.1:5000/count/Sala


### 4 - Endpoint route for Character sentimient in a given episode:
I return a dictionary with all the information we have, based on a specific variable requested by the user. For example, the user can ask for all the sentences of a particular judge. </br>

      http://127.0.0.1:5000/all/<variable>/<name>

A good example: 

      http://127.0.0.1:5000/all/Juez/MARIA DE LOS ANGELES PARRA LUCAN


            

### 5 - Endpoint route for posting a new entry through API:
You can post a new entry into the SQL Database for future query in the API. The software only needs the link of the cendoj court sentence, and it will assimilate all available information.

      http://127.0.0.1:5000/post

For this, I have built a small user interface to make it easy to insert the link to the required web page. 

<img src="https://i.gyazo.com/136a291e1117b20dddcf6e993e05783e.png" width="400" align="center">


The possible endpoint paths are infinite, but the most interesting part of the project is the scraping from the CENDOJ website, and how I manage all the data into the SQL database.

### Thanks for reading!
