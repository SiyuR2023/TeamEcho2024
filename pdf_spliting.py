import os
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
    
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])
        
        output_filename = os.path.join(output_dir, f'page_{page_num + 1}.pdf')
        
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        
        print(f'Created: {output_filename}')

if __name__ == "__main__":
    # Path to the PDF file to split
    pdf_file_path = 'pdf_uploadedFiles/centurion.pdf'  
    
    # Directory to save the single page PDFs
    output_directory = 'pdf_outputFiles'
    
    split_pdf(pdf_file_path, output_directory)
