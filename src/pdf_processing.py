import sparrow_extraction
import pdfplumber
import centurion_extraction
import first_integrated


def pdf_to_text(pdf_path):
    
    doc = pdfplumber.open(pdf_path)
    
    text = ""
    page = doc.pages[0]
    print(page)
    text += page.extract_text()
    
    return text


def search_keyword(text, keywords):
    for elem in text:
        for keyword in keywords:
            if keyword.lower() in elem[0].lower():
                return keyword
    return None  # Return None if no keyword is found


def is_empty(text):
    return not bool(text.strip())

def main():
    try: 
        pdf_path = "../resources/test.pdf"
        
        pdf = pdfplumber.open(pdf_path) #get the pdf file by path
        extraction_info = dict()
        page_errors = dict()
        text_content = pdf_to_text(pdf_path) #convert the pdf to string
       
        keywords = ["Sparrows", "Centurion", "First Integrated"] #set up a list for keywords
        
        for i, page in enumerate(pdf.pages): #loop the pdf files
            # text = page.extract_text() #extract each page's string 
            # page = pdf.pages[i]        #set up the page number
            # print("in the for loop")
            #search for keyword and choose the correct functions to process
            page_tables = page.extract_tables()
            first = page_tables[0]
            
            
            found_keyword = search_keyword(first, keywords) 
            
            print(f"keyword found: {found_keyword}", page)
            if found_keyword and found_keyword == "Sparrows":
                sparrow_extraction.extract_sparrow_pdf(pdf_path, i)
            elif found_keyword and found_keyword == "Centurion":
                
                centurion_extraction.extraction_centurion_pdf(pdf_path, i, page)
            # elif found_keyword and found_keyword == "First Integrated":
            #     first_integrated.extract_first_integrated_pdf(pdf_path)
            else:
                print(f"No matching keywords found")
    except Exception as e:
            print("Error in processing the PDF")

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