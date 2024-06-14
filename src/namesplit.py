import os
import re
import sparrow_extraction
import pdfplumber
import centurion_extraction
import first_integrated
import namesplit
from openpyxl import load_workbook
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter




def split_pdf(file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Check if the PDF file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return
    
    # Open the PDF file
    pdf_reader = PdfReader(file_path)
    pdf_plumber = pdfplumber.open(file_path)

    
    
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])
        page = pdf_plumber.pages[page_num]
        text = page.extract_text()
        #rint(text)
        if "Centurion" in text and "Hendrik" not in text:
            if page.extract_tables():
                try:
                    page_tables = page.extract_tables()
                    first_table = page_tables[0]

                    table_data = first_table[0][13]
                    table_data1 = table_data[15:21]
                    table_data5 = first_table[5]
                    table_data6 = table_data5[0]
                    table_data7 = table_data6[15:]
                    output_filename = os.path.join(output_dir, f'page_{page_num + 1}_{table_data1}_{table_data7}.pdf')
                    print(f'Created: {output_filename}')
                except Exception as e:
                    print("Error extracting format from page:", e)
                
        else:
            print("No verified company found")

        #output_filename = os.path.join(output_dir, f'page_{page_num}_{table_data1}_{table_data7}.pdf')
        
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        

        




if __name__ == "__main__":
    # Path to the PDF file to split
    pdf_file_path = 'pdf_uploadedFiles/centurion.pdf'  
    
    # Directory to save the single page PDFs
    output_directory = 'pdf_outputFiles'
    
    split_pdf(pdf_file_path, output_directory)