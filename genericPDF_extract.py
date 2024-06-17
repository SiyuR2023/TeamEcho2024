import os
import json
import pdfplumber

def extract_text_from_coordinates(pdf_path, coordinates_list):
    """
    Extracts text from specified areas on specific pages in a PDF.

    Args:
    pdf_path (str): Path to the PDF file.
    coordinates_list (list): List of dictionaries containing page number, coordinates, and keyword.

    Returns:
    dict: Extracted text from each specified area on each page.
    """
    extracted_texts = {}
    with pdfplumber.open(pdf_path) as pdf:
        for item in coordinates_list:
            page_number = item.get("page", None)
            x0, y0, x1, y1 = item["coordinates"]
            keyword = item["keyword"]

            pages_to_process = range(len(pdf.pages)) if page_number is None else [page_number]

            for page_num in pages_to_process:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    # Check if coordinates are within the page bounds
                    if (0 <= x0 < page.width and 0 <= y0 < page.height and
                        0 <= x1 <= page.width and 0 <= y1 <= page.height):
                        text = page.within_bbox((x0, y0, x1, y1)).extract_text()
                        if text:
                            extracted_texts.setdefault(keyword, []).append(text.strip())
                        else:
                            extracted_texts.setdefault(keyword, []).append(None)  # No text extracted
                    else:
                        extracted_texts.setdefault(keyword, []).append("Bounding box is outside the page bounds.")
                else:
                    extracted_texts.setdefault(keyword, []).append("Page number out of range.")
    
    # Adding completed field for each keyword
    for keyword in extracted_texts:
        extracted_texts[keyword].append({'completed': True})
    
    return extracted_texts

def save_results_to_file(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    pdf_path = input("Enter the PDF path: ")
    coordinates_json_path = input("Enter the JSON file path with coordinates: ")

    # Load coordinates from JSON file
    with open(coordinates_json_path, 'r', encoding='utf-8') as f:
        coordinates_list = json.load(f)

    extracted_texts = extract_text_from_coordinates(pdf_path, coordinates_list)
    
    save_results_to_file(extracted_texts, 'genericSearch_results.json')
    print("Extracted texts saved to 'genericSearch_results.json'")
