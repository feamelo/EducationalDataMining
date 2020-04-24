# Statistical Analysis - UnB
This is a final graduation project which aims to apply statistical methods to analyze UnB courses data. 

## Installation

Install python
```
sudo apt-get update
sudo apt-get install python3.6
```

Create a virtual environment called "venv" and activate it
```
python3 -m venv venv
source venv/bin/activate
```

Install the required packages
```
python3 -m pip install -r requirements.txt
```

## Usage 

Navigato to one of the folders containing the analysis (bi, grades, probability, cep). 
```
cd <folder>
```

For running the python files containing the scripts for extracting the data features from the tables.
```
python3 <filename>.py
```

Run the notebook with the analysis
```
jupyter notebook <filename>.ipynb
```

# Overview
The project is divided into four main sections:

## "BI" folder

Contains the analysis of the UnB BI platform for the students of Computer Engineering from 2009 to 2019.

The "/data" folder contains the tables (.csv and .xlsx) generated on the platform, whose features were extracted using the file __[extraction.py](bi/extraction.py)__ that feeds a SQL database.

The following images illustrate the outputs of the file __[notebook_bi.ipynb](bi/notebook_bi.ipynb)__ , containing the analysis of the extracted features. 

![Amount](bi/notebook_BI_files/notebook_BI_15_0.png?raw=true)
![Mean_ira](bi/notebook_BI_files/notebook_BI_6_0.png?raw=true)

## "Grades" folder

Contains the analysis of the grades of the students of Electrical and Computer Engineering from 2009 to 2018.

The file __[extraction.py](grades/extraction.py)__ reads the txt data inside "/data" folder and creates a structured database of grades for all courses of Electrical Engineering (ENE) and Computer Science (CIC) departments from 2009 to 2018.

The analysis is stored in the ipython notebook __[grades_notebook.ipynb](grades/grades_notebook.ipynb)__ and some outputs are shown bellow:

+ Courses with highest failure rate per department
![Failure_ene](grades/images/failure_ene.png?raw=true)
![Failure_cic](grades/images/failure_cic.png?raw=true)


+ Dynamical behaviour of any course over time.

![Time](grades/images/time.png?raw=true)

## "CEP" folder

Contains the analysis of the relation between the IRA (GPA equivalent ) and the CEP (brazilian ZIP code) from the students of Computer Engineering over time.

The notebooks __[CEP_IRA.ipynb](cep/CEP_IRA.ipynb)__ e __[CEP_aluno.ipynb](cep/CEP_aluno.ipynb)__ extracts the features of the files from the __[data](cep/data)__ folder and generates the pictures of the __[heatmap](cep/heatmap)__ folder.

The file __[convert2gif.py](cep/convert2gif.py)__ inserts a "semester/year" title on the top of each image and converts them to an animated gif.

![Heatmap_IRA](cep/heatmap_ira.gif)


## "Probability" folder

Contains the analysis of the dropout probability of the Computer Engineering students. 
The 3 notebooks contains the graphs relating the conditional probability of dropout and courses failure.

![Prob_1x1_sem1](probability/images/prob_1x1_sem1.png?raw=true)
![Prob_1x2_sem1](probability/images/prob_1x2_sem1.png?raw=true)
