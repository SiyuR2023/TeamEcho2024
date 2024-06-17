import fitz  # PyMuPDF
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json

def get_coords(pdf_path, output_json_path):
    doc = fitz.open(pdf_path)
    coordinates_dict = []

    def onclick(event, coords, ax, fig):
        coords.append((event.xdata, event.ydata))
        if len(coords) % 2 == 0:
            x0, y0 = coords[-2]
            x1, y1 = coords[-1]
            ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], color='red')
            fig.canvas.draw()

    def select_page():
        while True:
            try:
                page_number = int(input(f"Enter the page number (0 to {len(doc)-1}): "))
                if 0 <= page_number < len(doc):
                    return page_number
                else:
                    print(f"Error: Page number out of range. Please enter a valid page number (0 to {len(doc)-1}).")
            except ValueError:
                print("Error: Please enter a valid integer for the page number.")

    def select_coordinates_for_page(page_number):
        page = doc.load_page(page_number)
        coords = []

        fig, ax = plt.subplots()
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = np.array(img)
        ax.imshow(img)

        cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, coords, ax, fig))
        
        plt.show()
        plt.close(fig)

        return coords

    while True:
        page_number = select_page()
        coords = select_coordinates_for_page(page_number)

        while len(coords) % 2 != 0 or len(coords) == 0:
            print("You need to select pairs of coordinates.")
            coords = select_coordinates_for_page(page_number)
        
        for i in range(0, len(coords), 2):
            x0, y0 = coords[i]
            x1, y1 = coords[i+1]
            keyword = input("Enter the keyword for these coordinates: ")
            apply_all_pages = input("Apply these coordinates to all pages? (yes/no): ").strip().lower()
            if apply_all_pages == 'yes':
                coordinates_dict.append({"page": None, "coordinates": [x0, y0, x1, y1], "keyword": keyword})
            else:
                coordinates_dict.append({"page": page_number, "coordinates": [x0, y0, x1, y1], "keyword": keyword})

        cont = input("Do you want to select another page? (yes/no): ").strip().lower()
        if cont != 'yes':
            break

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(coordinates_dict, json_file, indent=4)
    
    print(f"Coordinates saved to {output_json_path}")

if __name__ == "__main__":
    pdf_path = input("Enter the PDF path: ")
    output_json_path = input("Enter the output JSON file path: ")
    get_coords(pdf_path, output_json_path)
