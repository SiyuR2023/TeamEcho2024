import os
import re
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter


def split_pdf(pdf_path, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Check if the PDF file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: The file {file_path} does not exist.")
        return
    
    # Open the PDF file
    pdf_reader = PdfReader(pdf_path)
    
    for page_num in range(len(pdf_reader.pages)):
    
        doc = pdfplumber.open(pdf_path)
    
        text = ""
        page = doc.pages[page_num]
    
        text += page.extract_text()
        x = re.split("\n|,|:", text)
        e = [e.lower() for e in x]
        y = e.index('report number')
        z = x[y+1].replace(' ','')
        #print("Report number: ",x[1])
        #print("ID number: ",x[8])
        #print("Date number: ",x[18])
        #print("Order number: ",x[31])
        #print(x)
        #print(x[0])
        #return text

        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])
        
        output_filename = os.path.join(output_dir, f'Certificate_{z}.pdf')
        
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        
        print(f'Created: {output_filename}')


def main():
    pdf_path = "../src/pdf_uploadedFiles/centurion.pdf"
    output_directory = 'pdf_outputFiles'
    pdf = pdfplumber.open(pdf_path) #get the pdf file by path
    extraction_info = dict()
    page_errors = dict()
    #text_content = split_pdf(pdf_path) #convert the pdf to string
    split_pdf(pdf_path, output_directory)

if __name__ == "__main__":
    main()