import sys
import os
import json
import re
from PyPDF2 import PdfReader, PdfWriter
import zipfile  # Import the zipfile module

def load_search_results(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load search results from {json_path}: {e}")
        raise

def split_pdf_by_values(pdf_path, search_results, output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"The file {pdf_path} does not exist.")

        pdf_reader = PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)
        filenames = []  # List to store filenames to add to zip

        for key, page_dict in search_results.items():
            if key == "completed":
                continue
            for page_num_str, values in page_dict.items():
                try:
                    page_num = int(page_num_str) - 1  # Convert to zero-based index
                except ValueError:
                    print(f"Warning: Skipping invalid page number {page_num_str}.")
                    continue

                if 0 <= page_num < total_pages:
                    for value in values:
                        pdf_writer = PdfWriter()
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                        
                        sanitized_value = re.sub(r'[^\w\-_\. ]', '_', value)  # Sanitize the value for file name
                        output_filename = os.path.join(output_dir, f'{sanitized_value}_Page_{page_num + 1}.pdf')
                        filenames.append(output_filename)  # Add to list for zipping
                        with open(output_filename, 'wb') as out:
                            pdf_writer.write(out)
                else:
                    print(f"Warning: Page number {page_num + 1} out of range.")
        return filenames
    except Exception as e:
        print(f"Error during PDF splitting: {e}")
        raise

def create_zip_file(output_dir, filenames):
    zip_filename = os.path.join(output_dir, "split_pdfs.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in filenames:
            zipf.write(file, os.path.basename(file))
    print(f"All files zipped successfully into '{zip_filename}'")
    return zip_filename

def clean_up_files(filenames):
    for file in filenames:
        os.remove(file)
    print("Temporary files deleted.")

if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            print("Usage: python pdf_splitting.py <PDF path> <JSON path> <output directory>")
            sys.exit(1)

        pdf_path = sys.argv[1]
        json_path = sys.argv[2]
        output_dir = sys.argv[3]

        search_results = load_search_results(json_path)
        filenames = split_pdf_by_values(pdf_path, search_results, output_dir)
        zip_filename = create_zip_file(output_dir, filenames)  # Zip all files after splitting
        clean_up_files(filenames)  # Delete all files that were added to the zip archive
        print(f"PDF splitting completed, files zipped in '{output_dir}'")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
