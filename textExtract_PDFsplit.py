# import os
# import json
# import pdfplumber

# def extract_text_from_coordinates(pdf_path, coordinates_dict):
#     """
#     Extracts text from specified areas on specific pages in a PDF.

#     Args:
#     pdf_path (str): Path to the PDF file.
#     coordinates_dict (dict): Dictionary with page numbers as keys and list of coordinates as values.

#     Returns:
#     dict: Extracted text from each specified area on each page.
#     """
#     extracted_texts = {}
#     with pdfplumber.open(pdf_path) as pdf:
#         for page_number, coordinates_list in coordinates_dict.items():
#             for coordinates in coordinates_list:
#                 if page_number < len(pdf.pages):
#                     page = pdf.pages[page_number]
#                     x0, y0, x1, y1 = coordinates
#                     # Check if coordinates are within the page bounds
#                     if (0 <= x0 < page.width and 0 <= y0 < page.height and
#                         0 <= x1 <= page.width and 0 <= y1 <= page.height):
#                         text = page.within_bbox((x0, y0, x1, y1)).extract_text()
#                         if text:
#                             extracted_texts.setdefault(f'{page_number + 1}', []).append(text.strip())
#                     else:
#                         extracted_texts.setdefault(f'{page_number + 1}', []).append("Bounding box is outside the page bounds.")
#                 else:
#                     extracted_texts.setdefault(f'{page_number + 1}', []).append("Page number out of range.")
#     return extracted_texts

# def save_results_to_file(results, output_file):
#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(results, file, indent=4)

# if __name__ == "__main__":
#     pdf_path = input("Enter the PDF path: ")
#     num_ranges = int(input("Enter the number of page ranges to extract text from: "))
#     coordinates_dict = {}

#     total_pages = pdfplumber.open(pdf_path).pages

#     for _ in range(num_ranges):
#         start_page = int(input("Enter the starting page number (0-indexed): "))
#         end_page = int(input("Enter the ending page number (0-indexed, inclusive): "))
#         num_areas = int(input(f"Enter the number of areas to extract text from on pages {start_page + 1} to {end_page + 1}: "))
        
#         coordinates_list = []
#         for _ in range(num_areas):
#             x0 = float(input("Enter x0 (left coordinate): "))
#             y0 = float(input("Enter y0 (top coordinate): "))
#             x1 = float(input("Enter x1 (right coordinate): "))
#             y1 = float(input("Enter y1 (bottom coordinate): "))
#             coordinates_list.append((x0, y0, x1, y1))
        
#         for page_number in range(start_page, end_page + 1):
#             coordinates_dict[page_number] = coordinates_list

#     remaining_pages = [i for i in range(len(total_pages)) if i not in coordinates_dict]

#     for page_number in remaining_pages:
#         num_areas = int(input(f"Enter the number of areas to extract text from on page {page_number + 1}: "))
#         coordinates_list = []
#         for _ in range(num_areas):
#             x0 = float(input("Enter x0 (left coordinate): "))
#             y0 = float(input("Enter y0 (top coordinate): "))
#             x1 = float(input("Enter x1 (right coordinate): "))
#             y1 = float(input("Enter y1 (bottom coordinate): "))
#             coordinates_list.append((x0, y0, x1, y1))
#         coordinates_dict[page_number] = coordinates_list

#     extracted_texts = extract_text_from_coordinates(pdf_path, coordinates_dict)
    
#     # for page, texts in extracted_texts.items():
#     #     print(f"Extracted Text from Page {page}:")
#     #     for text in texts:
#     #         print(text)
#     #         print("\n" + "="*40 + "\n")
    
#     save_results_to_file(extracted_texts, 'search_results.json')
#     print("Extracted texts saved to 'search_results.json'")

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
            keyword = item.get("keyword", "unknown")

            pages_to_process = range(len(pdf.pages)) if page_number is None else [page_number]

            for page_num in pages_to_process:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    # Check if coordinates are within the page bounds
                    if (0 <= x0 < page.width and 0 <= y0 < page.height and
                        0 <= x1 <= page.width and 0 <= y1 <= page.height):
                        text = page.within_bbox((x0, y0, x1, y1)).extract_text()
                        if text:
                            extracted_texts.setdefault(keyword, {}).setdefault(page_num + 1, []).append(text.strip())
                        else:
                            extracted_texts.setdefault(keyword, {}).setdefault(page_num + 1, []).append(None)  # No text extracted
                    else:
                        extracted_texts.setdefault(keyword, {}).setdefault(page_num + 1, []).append("Bounding box is outside the page bounds.")
                else:
                    extracted_texts.setdefault(keyword, {}).setdefault(page_num + 1, []).append("Page number out of range.")
    
    # Adding completed field for each keyword
    for keyword in extracted_texts:
        extracted_texts[keyword]['completed'] = True
    
    return extracted_texts

def save_results_to_file(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    pdf_path = input("Enter the PDF path: ")
    json_path = input("Enter the JSON file path with coordinates: ")
    output_file = 'search_results.json'

    # Load coordinates and keywords from JSON file
    with open(json_path, 'r', encoding='utf-8') as file:
        coordinates_list = json.load(file)

    # Extract text based on coordinates
    extracted_texts = extract_text_from_coordinates(pdf_path, coordinates_list)
    
    # Save the results to a JSON file
    save_results_to_file(extracted_texts, output_file)
    print(f"Extracted texts saved to '{output_file}'")

