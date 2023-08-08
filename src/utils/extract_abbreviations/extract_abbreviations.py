import os
from os.path import join, abspath

import docx
from csv import writer
import PyPDF2
import pandas as pd
import docx2txt

import zipfile
import xml.etree.ElementTree as ET

root_directory = r'C:\Users\Asus\Desktop\preklad\doc\small_ver\docx'

class DuplicateAbbraviationsInTable(Exception):
    pass


def extract_table_content(file_path, first_abbreviation_definition):
    # Open the DOCX file as a zip archive
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Extract the content of the "document.xml" file (where the text is stored)
        with zip_ref.open('word/document.xml') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Find all table elements
            table_elements = root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl')
            
            #iterate over every table
            for table in table_elements:
                rows = table.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr')
                table_content = []
                for x, row in enumerate(rows):
                    cell_texts = []
                    for cell in row.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc'):
                        cell_text = ''
                        for p in cell.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                            for t in p.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                                if t.text:
                                    cell_text += t.text
                        cell_texts.append(cell_text)

                    # If the selected table doesn't have first row, second columns skip table
                    try:
                        cell_texts[1]
                    except IndexError:
                        break

                    #Skip the table, in case it doesn't match abbrevition definition in its first row, second column
                    if x == 1 and cell_texts[1].strip().lower().replace('\xa0', ' ') != first_abbreviation_definition:
                        break
                    else:
                        table_content.append(cell_texts)
                        
                    if x == len(rows)-1:
                        return table_content


def get_abbreviations_from_docx(root_directory , abbreviation_notations):
    data = [] 
    for root, dir, files in os.walk(root_directory):
        for i, file in enumerate(files):
            file_path = abspath(join(root, file))

            #python docx library is unable to process tables as text, therefore it removes them from returned paragraph.
            #To overcome this issue, we've used docx2txt library to find the definition of first abbreviation and than
            #iterate over table to find a cell that matches the definition. If more than one table contains the defintion, an exception is raised. 

            # Get entire document as raw text 
            text_docx = docx2txt.process(file_path).lower().replace('\xa0', ' ')

            # Check whether given document contains at least one notation signalling abbreviation; should the file not contain such a notation, skip it.
            if not any(abbreviation_notation in text_docx for abbreviation_notation in abbreviation_notations):
                continue

            print(file_path)
            
            # Convert string int olist, delimitting by new line. 
            # We've found that definition of first abbreviation is on position n+4; where n=position of paragraph with abbreviation notation
            docx_list = text_docx.split('\n')
            docx_list = [item.strip() for item in docx_list]
            for abbreviation_notation in abbreviation_notations:
                try:
                    abbreviation_notation_index = docx_list.index(abbreviation_notation)        
                except ValueError:
                    continue
                except Exception as err:
                    print(f'Unexpected exception occured.{err}')
            first_abbreviation_definition = docx_list[abbreviation_notation_index+8].strip()


            abbreviation_table = extract_table_content(file_path, first_abbreviation_definition)
            data.append(abbreviation_table)

    return data

# xyz = get_abbreviations_from_docx(root_directory, ['applied designation and terminology'])

x = get_abbreviations_from_docx(root_directory, ['stosowane oznakowanie i nomenklatura','použité značenie a názvoslovie', 'applied designation and terminology', 'angewendete bezeichnungen und terminologie', 'alkalmazott jelölés és szakszókincs'])
df = pd.DataFrame(x)

df = df.dropna()
df = df.drop_duplicates()
df.to_csv(r'C:\Users\Asus\Desktop\preklad\slovak_abr.csv', encoding='ansi')
print(1)