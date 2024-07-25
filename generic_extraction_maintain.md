## Maintenance Manual for PDF Text Extraction Script
### 1. Overview
This script extracts text from specific areas on PDF pages based on predefined coordinates and keywords. It is designed to handle various text formats and special cases, including processing identification numbers and correcting errors.
### 2. Setup and Installation
#### 2.1. Prerequisites
•	Python Version: 3.x  
•	Required Libraries:  
- 	pdfplumber: For extracting text from PDF files.  
- 	json: For handling JSON data.  
- 	re: For regular expressions.  
- 	sys: For command-line argument handling.  
#### 2.2. Installation
##### 1.	Install Python: Ensure Python 3.x is installed on your system. You can download it from Python's official website.
##### 2.	Install Required Libraries: Use pip to install the required libraries. Open a terminal or command prompt and run:
```
pip install pdfplumber
```
## 3. Script Usage
#### The file will run automatically when using web application. The instructions below is for using the file individually.
### 3.1. Command-Line Arguments
The script requires three command-line arguments:
- 1.	PDF Path: The path to the PDF file from which text will be extracted.
- 2.	Coordinates JSON Path: The path to the JSON file containing the coordinates and keywords.
- 3.	Output JSON File: The path to the JSON file where the extracted text will be saved.
#### Usage:
```
python genericPDF_extract.py <PDF path> <coordinates JSON path> <output JSON file>
```
### 3.2. JSON Coordinates Format
The coordinates JSON file should be structured as follows:
```
{
    "page_number": [
        {
            "keyword": "Keyword1",
            "coordinates": [
                {"x0": 0, "y0": 0, "x1": 100, "y1": 50},
                {"x0": 100, "y0": 50, "x1": 200, "y1": 100}
            ]
        },
        {
            "keyword": "Keyword2",
            "coordinates": [
                {"x0": 200, "y0": 100, "x1": 300, "y1": 150}
            ]
        }
    ]
}
```
## 4. Script Maintenance
### 4.1. Code Structure
#### 1.	extract_text_from_coordinates(pdf_path, coordinates_dict):
- Extracts text from specified coordinates on each page and processes it based on keywords.
#### 2.	parse_page_number(page_num_str):
-	Converts page number strings to integers and handles invalid numbers.
#### 3.	is_valid_bbox(page, bbox):
-	Validates if the bounding box is within page dimensions.
#### 4.	process_text(extracted_texts, keyword, text):
-	Processes and stores extracted text.
#### 5.	process_id_number(extracted_texts, keyword, text):
-	Handles special processing for identification numbers.
#### 6.	extract_id_numbers(text):
-	Extracts and formats ID numbers from the text.
#### 7.	finalize_extracted_texts(extracted_texts):
-	Finalizes the text processing (not implemented in the provided code).
### 4.2. Adding New Features
#### To add new features or modify existing ones:
- 1.	Identify the Target Function: Determine which function needs modification or expansion.
- 2.	Update Logic: Modify the logic within the function or add new helper functions as needed.
- 3.	Test Changes: Thoroughly test the script with various PDF files and coordinate configurations.
- 4.	Update Documentation: Ensure that all changes are reflected in the comments and documentation.
- 5. Troubleshooting
### 5.1. Common Issues
#### 1.	Invalid Page Number:
-	Error Message: Invalid page number: <page_num_str>
-	Solution: Ensure that the page number provided in the JSON file is within the range of pages in the PDF.
#### 2.	Bounding Box Out of Range:
-	Error Message: Bounding box is outside the page bounds.
-	Solution: Verify that the coordinates in the JSON file are within the dimensions of the page.
#### 3.	No Text Extracted:
-	Error Message: No text extracted
-	Solution: Check the coordinates and ensure that they are correct and contain text.
#### 4.	Malformed JSON:
-	Error Message: JSON parsing error
-	Solution: Validate the JSON file for proper formatting using a JSON validator.
### 5.2. Debugging Tips
•	Print Statements: Use print statements to output variable values and track the flow of execution.  
•	Logging: Implement logging to capture detailed runtime information and errors.  
•	Unit Tests: Write unit tests to check individual functions and their correctness.  
## 6. Best Practices
- 1.	Code Consistency: Follow consistent coding standards and naming conventions.
- 2.	Version Control: Use version control (e.g., Git) to manage changes and collaborate with others.
- 3.	Documentation: Maintain up-to-date documentation for functions and usage instructions.
- 4.	Error Handling: Implement comprehensive error handling to manage unexpected situations gracefully.
## 7. References
•	pdfplumber Documentation  
•	Python Regular Expressions  
•	JSON Specification  
