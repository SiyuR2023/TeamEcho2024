## 1. Introduction
### 1.1 Purpose
#### This document provides installation, configuration, usage, and maintenance guidelines for the Python script excel_management.py. This script is used to process JSON data, export it to an Excel file, and log error information.
### 1.2 Scope
#### Applicable to the excel_management.py script, covering data processing, Excel file generation, and error logging
## 2. File Overview
### 2.1 File excel_management.py
#### Functionality
•	Data Processing: Extract data from a JSON file.  
•	Excel Generation: Write and format data into an Excel file.  
•	Error Logging: Log errors encountered during the data processing to a separate worksheet.  
#### Key Modules and Functions
•	preProcess: Process Excel header and formatting.  
•	insertData: Insert extracted data into the Excel sheet.  
•	insertError: Insert error information into the error worksheet.  
•	create_excel: Create and save the Excel file.  
•	modelProcess: Process and parse model data.  
•	manuProcess: Process and parse manufacturer data.  
•	dateProcess: Process date data.  
•	swlProcess: Process SWL (Safe Working Load) data.  
•	jsonProcess: Read data from a JSON file.  
## 3. Installation and Configuration
### 3.1 Environment Setup
#### Ensure the following environment settings and dependencies are installed:
•	Python Version: 3.x  
•	Required Libraries: Install the openpyxl library using the following command:     
                  ``` pip install openpyxl```  
### 3.2 File Preparation
#### 1.	Download Script: Download and save excel_management.py to your local directory.  
#### 2.	Database File:  
•	Ensure the file database/Full_list_of_Manufacturers_and_Models.xlsx exists and contains the necessary manufacturer and model data.  
•	Ensure the path and filename are correct, as the script loads data from this file.  
### 3.3 Configuration Files
•	JSON Data File: Contains the data to be processed. Example path: input.json.  
•	Error Log File: Records errors encountered during processing. Example path: errors.json.  
## 4. Usage Instructions
### The file will run automatically when using the web application, below instructions are for using individually.
### 4.1 Running the Script
#### Run the script using the following command line format:
```python excel_management.py <input JSON file> <output Excel file> <Client Name> <Error JSON file>```  
•	<input JSON file>: Path to the input JSON file.  
•	<output Excel file>: Path for the output Excel file.  
•	<Client Name>: The client name to be included in the Excel file.  
•	<Error JSON file>: Path to the error log file.  
### 4.2 File Handling
•	data.json: JSON-formatted input data. Ensure the data format meets expectations, for example:  
```json
{
  "Id Number": ["1234", "5678"],
  "RFID": ["ABCD1234", "EFGH5678"],
  "Item Category": ["Category1", "Category2"],
  "Item Description": ["Description1", "Description2"],
  "Model": ["Model1", "Model2"],
  "SWL": ["1000kg Note1", "2000kg Note2"],
  "Manufacturer": ["Manufacturer1", "Manufacturer2"],
  "Certificate No": ["Cert1", "Cert2"],
  "Location": ["Location1", "Location2"],
  "Detailed Location ": ["Detail1", "Detail2"],
  "Previous Inspection": ["2023-01-01", "2023-06-01"],
  "Next Inspection Due Date": ["2023-12-01", "2024-06-01"],
  "Fit For Purpose Y/N": ["Y", "N"],
  "Status": ["Active", "Inactive"],
  "Provider Identification": ["Provider1", "Provider2"],
  "Errors": ["Error1", "Error2"]
}
```
•	output.xlsx: Generated Excel file with processed and formatted data.  
•	errors.json: JSON file for recording errors encountered during processing. Error information will be written to this file for subsequent analysis and correction.   
## 5.1 File Updates
### •	Updating excel_management.py:
 o	Ensure the script logic and functionality meet the latest data processing requirements.  
 o	Test thoroughly after any script modifications to validate functionality.  
### •	Updating Database File:
 o	Update the Full_list_of_Manufacturers_and_Models.xlsx file as needed to ensure it contains the latest manufacturer and model data.  
 o	Verify the path and filename to ensure the script can successfully load the data.  
## 5.2 Error Handling and Logging
### •	Error Handling:
 o	Errors will be logged in the errors.json file. Check this file to locate and address processing issues.  
 o	Common errors might include file reading errors, data format issues, or data processing errors.  
### •	Log File:
 o	Error information is recorded in errors.json. Check this file to understand the issues encountered during processing and take corrective actions.  




