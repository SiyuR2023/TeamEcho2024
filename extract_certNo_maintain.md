## 1. Introduction
### 1.1 Purpose
#### This document provides guidelines on installing, configuring, and using the script extract_certNo.py. This Python script is designed to extract unique certificate numbers from JSON-formatted data and save them into an output file.
### 1.2 Scope
#### This documentation applies to extract_certNo.py, focusing on unique certificate number extraction from JSON data and outputting to a file.
## 2. File Overview
### 2.1 File extract_certNo.py
#### Functionality
•	Data Processing: Reads JSON data and extracts unique certificate numbers.  
•	Output Generation: Writes the extracted certificate numbers to an output file in JSON format.   
#### Key Functions
•	extract_certificate_no: Extracts unique certificate numbers.
•	save_results_to_file: Saves the results to an output file.
## 3. Installation and Configuration
### 3.1 Environment Setup
#### Ensure the following environment settings and dependencies are installed:
•	Python Version: 3.x  

•	Required Libraries: json  
### 3.2 Installation:
Download extract_certNo.py and place it in your desired directory.
### 3.3 Configuration Files:
Prepare your input JSON file with the expected data structure. Ensure the path to this file is accessible to the script.
### 3.4 JSON Coordinates Format
The coordinates JSON file should be structured as follows:
```
{
    "Certificate No": [
        "CERT123456",
        "CERT123456",  
        "CERT789101",
        "CERT112131",
        "CERT141516",
        "CERT141516",  
        "CERT171819"
    ]
}
```
## 4. Usage Instructions
### The file will run automatically when using the web application, below instructions are for using individually.
### 4.1 Running the Script
#### Run the script using the following command line format:
```python extract_certNo.py <input JSON file> <output JSON file>```  
•	<input JSON file>: Path to the JSON file containing certificate data. 
•	<output JSON file>: Desired path for the JSON file to save extracted certificates. 
## 5.1 Maintenance Manual
### •	Updating the Script
 Regularly check and update the script for compatibility with new Python versions or JSON data formats.  
## 5.2 Error Handling and Logging
### •	Error Handling:
Monitor for errors related to file access or JSON format. Update exception handling in the script to provide more descriptive error messages and solutions.
## 6 Troubleshooting
### Common Issues:
JSON Parsing Error: Ensure the input JSON file is properly formatted.
File Not Found: Verify that the paths provided are correct and accessible.
## 7 Best Practices
Code Review: Periodically review the code for optimisation and better error handling.





