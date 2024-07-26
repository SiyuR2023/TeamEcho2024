## 1. Introduction
### 1.1 Purpose
#### This document outlines the functionality, usage, and maintenance of the pdf_splitting.py script. This script is designed to split PDF files based on specified page numbers and keywords, save individual pages as new PDF files, and then compress these files into a zip archive for easy distribution and storage.
### 1.2 Scope
#### This documentation covers the entire lifecycle of the script from installation, configuration, and usage, to maintenance. The script is applicable in scenarios where selective extraction of PDF pages is needed, followed by archiving.
## 2. File Overview
### 2.1 File pdf_splitting.py
#### Functionality
•	Data Processing: Splits a single PDF into multiple files based on JSON-configured keywords and page numbers.  
•	File Output: Generates individual PDF files and a zip archive of these files.  
•	Clean-up Operation: Removes all intermediary PDF files post-archiving.  
#### Key Modules and Functions
•	load_search_results: Loads the JSON configuration file containing the keywords and target pages. 
•	split_pdf_by_values: Processes the PDF according to the loaded configuration and saves new PDFs. 
•	create_zip_file: Archives all generated PDF files into a single zip file. 
•	clean_up_files: Deletes all temporary files created during the splitting process. 
## 3. Installation and Configuration
### 3.1 Environment Setup
#### Ensure the following environment settings and dependencies are installed:
•	Python Version: 3.x  PyPDF2: For handling PDF reading and writing operations.
json: For parsing JSON files.
os, sys, re: Standard Python libraries for file and system operations.

•	Required Libraries: Install the PyPDF2 library using the following command:     
                  ``` pip install PyPDF2```  
### 3.2 File Preparation
Script File: Ensure that pdf_splitting.py is saved in your project directory.
JSON Configuration File: Prepare a JSON file specifying the pages and keywords for splitting.

## 4. Usage Instructions
### The file will run automatically when using the web application, below instructions are for using individually.
### 4.1 Running the Script
#### Run the script using the following command line format:
```python pdf_splitting.py <PDF path> <JSON path> <output directory>```  
•	<PDF path>: Path to the input PDF file. 
•	<JSON path>: Path to the JSON configuration file. 
•	<output directory>: Directory where the output files will be saved. 
### 4.2 Post-Execution
After running the script, check the specified output directory for the split_pdfs.zip file containing all the split PDF files.  
## 5.1 Maintenance Manual
### •	Updating the Script
 Review and test the script periodically to ensure compatibility with new versions of dependencies and Python.
Update the JSON configuration as needed to reflect changes in the document structure or processing requirements.  
## 5.2 Error Handling and Logging
### •	Error Handling:
The script includes basic error logging to assist with troubleshooting issues related to file access, JSON parsing, and PDF processing.  
Regularly check console outputs for any error messages that may indicate problems during execution.
## 5.3 Best Practices
Maintain a backup of the original PDF files and the JSON configuration to prevent data loss.
Keep the Python environment and libraries updated to the latest stable versions to ensure optimal performance and security





