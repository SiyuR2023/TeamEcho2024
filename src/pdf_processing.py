import sparrow_extraction
import pdfplumber
import centurion_extraction
import first_integrated
import EnerMech
import controlUnion
import re

def pdf_to_text(pdf_path):
    
    doc = pdfplumber.open(pdf_path)
    
    text = ""
    page = doc.pages[0]
    
    text += page.extract_text()
    
    return text


def search_keyword(text, keywords):
    text = text.replace("\n", " ")
    text = text.split(',')
    
    for elem in text:
        # print(elem)
        # print("---------")
        for keyword in keywords:
            # print(keyword)
            # print("<<<<<<<<<<<")
            if keyword.lower() in elem.lower():
                return keyword
    return None  # Return None if no keyword is found


def is_empty(text):
    return not bool(text.strip())

def main():
    # try: 
    # pdf_path = "../resources/First_Integrated.pdf"
    # pdf_path = "../resources/test.pdf"
    # pdf_path = "../resources/EnerMech Example 1.pdf"
    pdf_path = "../resources/Control Union Example 1.pdf"
    
    pdf = pdfplumber.open(pdf_path) #get the pdf file by path
    extraction_info = dict()
    page_errors = dict()
    text_content = pdf_to_text(pdf_path) #convert the pdf to string
    
    keywords = ["Sparrows", "Centurion", "First Integrated", "Report Ref No", "EnerMech", "Control Union"] #set up a list for keywords
    
    for i, page in enumerate(pdf.pages): #loop the pdf files
        # text = page.extract_text() #extract each page's string 
        # page = pdf.pages[i]        #set up the page number
        # print("in the for loop")
        #search for keyword and choose the correct functions to process
        if i >= 2:
            break
        page_tables = page.extract_text()
        # print(page_tables)
        first = None
        found_keyword = None
        print(len(page_tables))
        if(len(page_tables) != 0):
            first = page_tables
            # print(first)
            found_keyword = search_keyword(first, keywords) 
        
        
        
        # print(f"keyword found: {found_keyword}", page)
        
        if len(page_tables) == 0:
            print("No data in this page")
            continue
        elif found_keyword and found_keyword == "Sparrows":
            sparrow_extraction.extract_sparrow_pdf(pdf_path, i)
        elif found_keyword and found_keyword == "Centurion":
            centurion_extraction.extraction_centurion_pdf(pdf_path, i, page)
        elif found_keyword == "EnerMech":
            EnerMech.extractEner(pdf_path, i)
        elif found_keyword == "First Integrated":
            first_integrated.extract_first_integrated_pdf(pdf_path, i)
        elif found_keyword == "Control Union":
            controlUnion.extractConUn(pdf_path, i)
        #     first_integrated.process_table_type1(page_tables, extraction_info)
        # elif found_keyword == "Date of Thorough Examination":
        #     first_integrated.process_table_type2(page_tables[0], extraction_info)
        # elif found_keyword == "Name &AddressofManufacturer" or found_keyword == "Name & Address of Manufacturer":
        #     first_integrated.process_table_type3(page_tables[0], extraction_info)
        # else:
        #     page_errors[i+1] = f"No recognized table found on page {i+1}"
        # elif found_keyword and found_keyword == "First Integrated":
        #     first_integrated.extract_first_integrated_pdf(pdf_path)
        else:
            print(f"No matching keywords found")
    # except Exception as e:
    #         print("Error in processing the PDF")

    # return 

""" def main():
        try:
            pdf_path = "../resources/sparrows.pdf"
            images_path = "../resources/images"
            text_content = pdf_to_text(pdf_path)
            keywords = ["Sparrows", "Centurion", "First Integrated"]

            if is_empty(text_content):
                print(f"No text found")

            else:
                found_keyword = search_keyword(text_content, keywords)
                print(f"keyword found: {found_keyword}")
                if found_keyword and found_keyword == "Sparrows":
                    sparrow_extraction.extract_sparrow_pdf(pdf_path)
                elif found_keyword and found_keyword == "Centurion":
                    centurion_extraction.extraction_centurion_pdf(pdf_path)
                elif found_keyword and found_keyword == "First Integrated":
                    first_integrated.extract_first_integrated_pdf(pdf_path)
                else:
                    print(f"No matching keywords found")
        except Exception as e:
            print("Error in processing the PDF")
"""


if __name__ == "__main__":
    main()