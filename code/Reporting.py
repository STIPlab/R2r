# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:54:17 2020

@author: Barreneche_A
"""

import pandas as pd

from jinja2 import FileSystemLoader, Environment
from jinja2.utils import urlize

from datetime import datetime

def csv_to_Qhtml(parea):
    """
    Open a .csv file and return it in HTML format.
    :param filepath: Filepath to a .csv file to be read.
    :return: String of HTML to be published.
    """
    filepath = "INPUT/pdq.csv"
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv(filepath, index_col=0, engine='python')
    df = df[parea].to_frame()
    qtext = str(df[parea].iloc[0])
    df.drop(df.index[0], inplace=True)
    df.rename(columns={parea : 'Response'}, inplace=True)
    
    #df['Response'] = df['Response'].str.encode('utf-8', 'ignore').str.decode('utf-8')
    df['Response'] = df['Response'].apply(lambda x: urlize(x, 40, target='_blank'))
    
    html = df.to_html(index_names=False, classes=['table-striped', 'table-bordered'], escape=False, table_id="Qtable").replace("\\n","<br>").replace("\\t"," ").replace("\\r","")
    Qhtml = [qtext,html]
    return Qhtml

def csv_to_html_text(parea):
    """
    Open a .csv file and return it in HTML format.
    :param filepath: Filepath to a .csv file to be read.
    :return: String of HTML to be published.
    """
    filepath = "INPUT/secTexts.csv"
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv(filepath, index_col=0, engine='python')
    df = df.T
        
    #df = df[parea].apply(lambda x: urlize(x, 40, target='_blank'))
    
    html_text = df[parea].tolist()
    return html_text

# Allow for very wide columns - otherwise columns are spaced and ellipse'd
pd.set_option("display.max_colwidth", 200)

# Configure Jinja and ready the loader
env = Environment(
    loader=FileSystemLoader(searchpath="templates")
)

main_template = env.get_template("main.html")
section_template = env.get_template("section.html")

def main(PAREA):

    now = datetime.now()
    dt_stamp = now.strftime("%d %B, %Y")
    
    with open("OUTPUT/main.html", "w", encoding="utf-8") as f:
        output = main_template.render(PAREA=PAREA, today=dt_stamp) 
        f.write(output)
    
    for i, item in enumerate(PAREA):
        PDQdata =   csv_to_Qhtml(PAREA[i])
        q = PDQdata[0]
        rtable = PDQdata[1]
        
        textdata = csv_to_html_text(PAREA[i])
        
        secFile = "OUTPUT/" + str(PAREA[i]) + ".html"
        
        with open(secFile, "w", encoding="utf-8") as f:
            output = section_template.render(parea = PAREA[i], texts=textdata, table = rtable, table_id="Qtable", PDQtext = q) 
            f.write(output)

        
if __name__ == "__main__":
    main(PAREA)