import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import json
import re

column_mapping = {
    "Id Number": "A",
    "RFID": "B",
    "Item Category": "C",
    "Item Description": "D",
    "Model": "E",
    "SWL Value": "F",
    "SWL Unit": "G",
    "SWL Note": "H",
    "Manufacturer": "I",
    "Certificate No": "J",
    "Location": "K",
    "Detailed Location ": "L",
    "Previous Inspection": "M",
    "Next Inspection Due Date": "N",
    "Fit For Purpose Y/N": "O",
    "Status" : "P",
    "Provider Identification": "Q",
    "Errors": "R"
}


def create_excel(extracted_data: dict, filename: str, client: str, page_errors: dict):
        
    # try:
        print("<--------------Creating new excel------------------>")
        workbook = openpyxl.Workbook()  # Create a new Workbook

        # Create a sheet for extracted data
        sheet_data = workbook.active
        sheet_data.title = "Extraction Data"  # Set sheet name

        sheet_data['A1'] = "Rig-Ware import v2"
        sheet_data['B1'] = client
        sheet_data['C1'] = "CreateLocations=No"

        # Write column headers for extracted data sheet
        for header, column in column_mapping.items():
            cell = sheet_data[column + '2']
            cell.value = header
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')  # Center align the text
            cell.border = Border(bottom=Side(border_style='thin'))  # Add a thin border at the bottom

            # Adjust column width to fit the header text
            column_width = max(len(header), 10)  # Set a minimum width of 10 characters
            sheet_data.column_dimensions[column].width = column_width
        
        
        nameList = list(extracted_data.keys())  
        print(nameList)
       
        row_idx = 3

        for name in nameList:
            if name == "SWL":
                    swlVlaue = extracted_data.get(name)
                    
                    swlProcess(sheet_data, swlVlaue)
            else:
                column_name = column_mapping.get(name)  
                if column_name:
                    row_idx = 3
                    
                    for val in extracted_data.get(name, []):
                        if isinstance(val, str):  
                            sheet_data.cell(row=row_idx, column=ord(column_name) - 64, value=val)
                            row_idx += 1  

       

        # Create a sheet for errors
        sheet_errors = workbook.create_sheet(title="Errors")  # Create a new worksheet
        sheet_errors.append(["Page No", "Error"])  # Write column headers

        # Write errors to the worksheet
        for key, value in page_errors.items():
            sheet_errors.append([key, value])  # Write key-value pairs as rows

        workbook.save(filename)  # Save the workbook with the provided filename
        workbook.close()
        print("<-------------- Excel created successfully ------------------>")
    # except Exception as e:
    #     print(f"An error occurred in excel creation: {e}")

def swlProcess(sheet_data, swlValue):
    
    valPattern = r'\d+(?:\.\d+)?'
    unitPattern = r'[a-zA-Z]+'
    notePattern = r'[\s\n]+(\S.*)'
    idx = 3
    for val in swlValue:
        if isinstance(val, str):
            swlVal = re.findall(valPattern, val)[0]
            print(swlVal)
            sheet_data.cell(row=idx, column=ord("F") - 64, value=swlVal)
            
            swlUnit = re.findall(unitPattern, val)[0]
            print(swlUnit)
            sheet_data.cell(row=idx, column=ord("G") - 64, value=swlUnit)
            
            swlNote = re.findall(notePattern, val)
            if(len(swlNote) > 0):
                swlNote = swlNote[0]
                sheet_data.cell(row=idx, column=ord("H") - 64, value=swlNote)
            print(swlNote)
            
            idx += 1

        


def jsonProcess():
   
    with open('coords.json', 'r') as file:
        data = json.load(file)
    
    return data


if __name__ == "__main__":
    data = jsonProcess()
    create_excel(data, "output.xlsx", "Client Name", {"Page1": "Error1", "Page2": "Error2"})
