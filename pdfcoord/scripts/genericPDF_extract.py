
import os
import json
import pdfplumber
import sys
import re
def extract_text_from_coordinates(pdf_path, coordinates_dict):
    """
    Extracts text from specified areas on specific pages in a PDF.

    Args:
    pdf_path (str): Path to the PDF file.
    coordinates_dict (dict): Dictionary containing page numbers as keys and lists of dictionaries with coordinates and keywords.

    Returns:
    dict: Extracted text from each specified area on each page.
    """
    extracted_texts = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_num_str, items in coordinates_dict.items():
            try:
                page_num = int(page_num_str)  # Convert page number to integer
            except ValueError:
                print(f"Invalid page number: {page_num_str}")
                continue
            
            for item in items:
                keyword = item["keyword"]
                
                for coord in item["coordinates"]:
                    x0, y0, x1, y1 = coord["x0"], coord["y0"], coord["x1"], coord["y1"]
                    
                    if 0 <= page_num < len(pdf.pages):
                        page = pdf.pages[page_num]
                        
                        if (0 <= x0 < page.width and 0 <= y0 < page.height and
                            0 <= x1 <= page.width and 0 <= y1 <= page.height):
                            text = page.within_bbox((x0, y0, x1, y1)).extract_text()
                            if text:
                                
                                # put extracted data and headers into a dictionary
                                extracted_texts.setdefault(keyword, []).append(text.strip())
                                temp = []
                                idNumList = []
                                # processing id number speical cases
                                if keyword == "Id Number":
                                    num = 0
                                
                                    if "," in text:
                                        num = commaProcess(text)
                                        
                                    elif "to" in text:
                                        num = toProcess(text)

                                    elif "-" in text:
                                        num = dashProcess(text)
                                    
                                    if num > 10000:  # Arbitrary large number to prevent excessive memory usage
                                        print(f"Warning: Skipping large quantity {num} for text: {text}")
                                        continue
                                    
                                    temp = get_identification_number_list(text, num)
                                                                        
                                    idNumList.extend(temp)
                                    
                                    # the id number on the page is multiple, need to be expanded
                                    if len(idNumList) != 0:
                                        hint = "Below: " + str(len(idNumList))
                                        extracted_texts.setdefault(keyword, []).append(hint)
                                        for idNum in idNumList:
                                            cleaned_idNum = idNum.replace('\n', '').strip()
                                            extracted_texts.setdefault(keyword, []).append(cleaned_idNum)
                                            continue
                                
                            else:
                                extracted_texts.setdefault(keyword, []).append(None)  # No text extracted
                        else:
                            extracted_texts.setdefault(keyword, []).append("Bounding box is outside the page bounds.")
                    else:
                        extracted_texts.setdefault(keyword, []).append("Page number out of range.")
    if "\n(" in extracted_texts["Id Number"][0]:
        firstInteProcess(extracted_texts)
    idProcess(extracted_texts)
    nextLineProcess(extracted_texts)
    
    return extracted_texts

def nextLineProcess(extracted_texts):
    
    for key, value in extracted_texts.items():
        if key != ["Certificate No"] or key != ["SWL"]:
            newList = []
            for ele in value:
                if ele != None:
                    if '\n' in ele:
                        ele = ele.replace('\n', ' ')
                        newList.append(ele)
                    else:
                        newList.append(ele)
            extracted_texts[key] = newList

# method of processing one of First Integrated format
def firstInteProcess(extracted_texts):
    cert = None
    total = len(extracted_texts["Certificate No"])
    certList = []
    idx = 0
    for key, value in extracted_texts.items():
        
        newList = []
        if key != "Certificate No":
            for idx in range(0, total):
                if len(extracted_texts["Certificate No"]) != 0:
                    cert = extracted_texts["Certificate No"][idx]
                if key == "Id Number":
                    temp = value[idx].split(")\n")
                    for ele in temp:
                        if "GIT03641" in ele:
                            special = ele.split("\n")
                            newList.append(special[0])
                            newList.append(special[1])
                        else:
                            ele = ele + ')'
                            ele = ele.replace('\n', ' ')
                            newList.append(ele)
                        certList.append(cert)
                else:
                    temp = value[idx].split("\n")
                    for elem in temp:
                        newList.append(elem)
                        
        extracted_texts[key] = newList
    extracted_texts["Certificate No"] = certList

# procees multiple id number in one page
def idProcess(extracted_texts):
    
    idNumList = extracted_texts["Id Number"]
    idxDict = {}
    
    deleted = 2
    i = 0
    start = 0
    # check for the flag "Below", if there is a "Below: 8", 
    # means this page has 8 items 
    # with differnt id Numbers but same content(SWL, item description, etc)
    while i < len(idNumList):
        start += 1
        idNum = idNumList[i]
        if idNum != None and  "Below:" in idNum:
            start -= deleted
            count = int(re.findall(r'\d+', idNum.split("Below:")[1])[0])
            # count = int(idNum.split("Below:")[1]) 
            idxDict.update({start : count})

        i += 1
    # insert the duplicate data into correct position
    insertData(idxDict, extracted_texts)
    # delete incorrect format of id Number
    processFormat(idNumList, extracted_texts)

# delete and rewrite id number with wrong format
def processFormat(idNumList, extracted_texts):
    new_idNumList = []
    for idNum in idNumList:
        if idNum != None:
            match = re.findall(r'x(\d+)', idNum)
            secMatch = re.match(r'([A-Za-z]+\d+/?\d*)/(\d+)-(\d+)', idNum)
            thirdMatch = re.findall(r'\d{2}[A-Z]{2}\d-\d', idNum)
            if match or secMatch or thirdMatch or specialCase(idNum):
                continue  # Skip this idNum if it matches the condition
        new_idNumList.append(idNum)
    extracted_texts["Id Number"] = new_idNumList

def specialCase(idNum):
    cases = [",", "Below:", "to", " - " ]
    for ele in cases:
        if ele in idNum:
            return True
    return False

# insert data based on index of id number
# ensure that each header's content is at correct postion after processing id number
def insertData(idxDict, extracted_texts):
    
    nameList = []
    for key, value in extracted_texts.items():
        if key != "Id Number":
            nameList.append(key)
    for name in nameList:
        newList = []
        tempList = extracted_texts[name]
        for elem in tempList:
            newList.append(elem)
        for idx, count in idxDict.items():
            for j in range(idx, idx + count - 1):
                content = newList[idx]
                newList.insert(j, content)
        extracted_texts[name] = newList


def commaProcess(text):
    textList = text.split(",")
    
    return len(textList)


def only_contains_number(string):
    
    pattern = re.compile(r'^\d+$')

    return bool(pattern.search(string))
# split multiple id numbers if they have "to" in it and return a quantity for further processing

def toProcess(text):

    firstPart = None
    start = None
    secondPart = None
    end = None   
    
    if len(text.split(" to ")) > 1:
        firstPart = text.split(" to ")[0].strip()
        secondPart = text.split(" to ")[1].strip()
    else:
        firstPart = text.split("to")[0].strip()
        secondPart = text.split("to")[1].strip()
    
    if only_contains_number(firstPart):
        if only_contains_number(secondPart):
            start = int(firstPart)
            end = int(secondPart)
            return end - start + 1
    else:
        pattern = re.compile(r'\d+')
        end = pattern.findall(secondPart)[0]
    
    fLen= len(firstPart)
    start = firstPart[fLen - 1]
    if "-" in firstPart:
        start = re.findall(r'-(\d+)', firstPart)[0]

    if end != None:
        num = int(end) - int(start) + 1
    else:
        return 1
    return num

# split multiple id numbers if they have "-" in it and return a quantity for further processing
def dashProcess(text):

    firstPart = text.split("-")[0].strip()
    secondPart = text.split("-")[1].strip()
    start = re.findall(r'\d+', firstPart)[0]
    end = re.findall(r'(\d+)', secondPart)[0]
    num = int(end) - int(start) + 1
    
    return num

def get_identification_parts_list(input_string: str, quantity: int):
    
    if quantity > 10000:  # Arbitrary large number to prevent excessive memory usage
        print(f"Warning: Skipping large quantity {quantity} for input string: {input_string}")
        return []
    
    numeric_part = ''.join(filter(str.isdigit, input_string))
    part_list = list()
    if input_string[0].isdigit():
        alpha_part = input_string[len(numeric_part):]
        for i in range(0, quantity):
            part_list.append(f"{int(numeric_part) + i}{alpha_part}")
            
    else:
        alpha_part = input_string[:len(input_string)-len(numeric_part)]
        for i in range(0, quantity):
            part_list.append(f"{alpha_part}{int(numeric_part) + i}")
    return part_list

def checkMulti(identification_numbers, newList):
    
    for num in identification_numbers.split(','):
        id_number = num.split('x')[0].strip()
        for i in range(len(id_number)-1, -1, -1):
            if id_number[i].isdigit():
                id_number= id_number[:i+1]
                break
        count = int(''.join(filter(str.isdigit, num.split('x')[1].strip())))
        for i in range(1,count+1):
            newList.append(f"{id_number}-{i}")
    return newList

# generating id numbers based on quantity and format
def get_identification_number_list(identification_numbers: str, quantity: int):
        
    identification_number_list = list()
    #Take this as example (D971-1 to 6) or (MGL1 to MGL36)
    if "," in identification_numbers:
        identification_number_list = identification_numbers.split(',')
        if re.search(r'x(\d+)', identification_numbers):
            newList = []
            identification_number_list = checkMulti(identification_numbers, newList)
    
    elif "to" in identification_numbers.lower():
        # identification_number_first_part = D971-1 or MGL1
        identification_number_first_part = identification_numbers.split("to")[0].strip()
    
        # example: D971-1
        if "-" in identification_number_first_part:
            # first_part = D971, second_part = 1
            first_part, second_part = identification_number_first_part.split('-')
            # print(quantity)
            second_part_list = get_identification_parts_list(second_part, quantity)
            
            for second_part in second_part_list:
                identification_number_list.append(f"{first_part}-{second_part}")
        else:
            # example: MGL1
            identification_number_list = get_identification_parts_list(identification_number_first_part, quantity)
    elif re.search(r'x(\d+)', identification_numbers):
    
        identification_number_list = list()
        for num in identification_numbers.split(','):
            id_number = num.split('x')[0].strip()
            for i in range(len(id_number)-1, -1, -1):
                if id_number[i].isdigit():
                    id_number= id_number[:i+1]
                    break
            count = int(''.join(filter(str.isdigit, num.split('x')[1].strip())))
            for i in range(1,count+1):
                identification_number_list.append(f"{id_number}-{i}")
    elif "-" in identification_numbers and not identification_numbers.replace('-', '').isdigit():
        match = re.match(r'([A-Za-z]+)(\d+)-(\d+)', identification_numbers)
        secMatch = re.match(r'([A-Za-z]+\d+/?\d*)/(\d+)-(\d+)', identification_numbers)
        if match:

            prefix_alpha = match.group(1)
            range_start = int(match.group(2))
            range_end = int(match.group(3))
            if range_end < range_start:
                identification_number_list.append(f"{prefix_alpha}{range_start}")
            else:
                for i in range(range_start, range_end + 1):
                    identification_number_list.append(f"{prefix_alpha}{i}")
        elif secMatch:
            prefix_alpha = match.group(1)
            prefix_numeric = match.group(2)
            range_start = int(prefix_numeric)
            range_end = int(match.group(3))
            if range_end < range_start:
                identification_number_list.append(f"{prefix_alpha}/{range_start:02}")
                
            else:
                # Generate new id numbers based on the matched pattern
                for i in range(range_start, range_end + 1):
                    identification_number_list.append(f"{prefix_alpha}/{i:02}")
        else:
            parts = identification_numbers.split("-")
            if len(parts) == 2:
                first_part = parts[0].strip()
                second_part = parts[1].strip()
                
                prefix_part = first_part[:-1]
                start_number = int(first_part[-1])
                end_number = int(second_part)
            
                identification_number_list = [
                    f"{prefix_part}{i}" for i in range(start_number, end_number + 1)]
    
    return identification_number_list


def save_results_to_file(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python genericPDF_extract.py <PDF path> <coordinates JSON path> <output JSON file>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    coordinates_json_path = sys.argv[2]
    output_json_file = sys.argv[3]

    # Load coordinates from JSON file
    with open(coordinates_json_path, 'r', encoding='utf-8') as f:
        coordinates_dict = json.load(f)

    extracted_texts = extract_text_from_coordinates(pdf_path, coordinates_dict)
    
    save_results_to_file(extracted_texts, output_json_file)
    print(f"Extracted texts saved to '{output_json_file}'")