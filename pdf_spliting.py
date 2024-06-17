import os
import json
import re
from PyPDF2 import PdfReader, PdfWriter

def load_search_results(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def split_pdf_by_values(pdf_path, search_results, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.isfile(pdf_path):
        print(f"Error: The file {pdf_path} does not exist.")
        return
    
    pdf_reader = PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)

    for page_num_str, values in search_results.items():
        page_num = int(page_num_str) - 1  # Convert to zero-based index
        if 0 <= page_num < total_pages:
            for value in values:
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num])
                
                sanitized_value = re.sub(r'[^\w\-_\. ]', '_', value)  # Sanitize the value for file name
                output_filename = os.path.join(output_dir, f'{sanitized_value}_Page_{page_num + 1}.pdf')
                
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                
                print(f'Created: {output_filename}')
        else:
            print(f"Warning: Page number {page_num + 1} out of range.")

if __name__ == "__main__":
    json_path = 'search_results.json'  # Path to the search results JSON file
    pdf_path = input("Enter the PDF path: ")  # Prompt user for PDF path
    output_dir = 'pdf_outputFiles'  # Directory to save the split pages

    search_results = load_search_results(json_path)
    split_pdf_by_values(pdf_path, search_results, output_dir)
