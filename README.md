# TeamEcho2024

# Data extraction from PDF documents
## Overview
This project aims to build on the foundation laid by Team Charlie, by enhancing and expanding the capabilities of the existing system. to extract text data from PDF documents and store it in an Excel format for further analysis and processing, spliting the pdf doc into single pages and save same with the certificate report number. The extraction process involves identifying relevant information such as equipment details, descriptions, and manufacturers from PDF files and structuring it into an Excel spreadsheet.
These improvements aim to create a more robust, scalable, and user-friendly system that meets Interbloc’s evolving needs and sets the stage for future advancements.

## Features of Our Project:

PDF Processing: Our application leverages the Pdfplumber library to meticulously extract text from PDF documents, tailored specifically for efficient data retrieval and management within our Django-based UI. This integration allows for a seamless extraction process directly from the user interface.

Excel File Creation: As part of our data processing workflow, we generate Excel files to organize and store extracted data. This functionality remains integral to our system, providing users with easy access to analyzed and structured data for further manipulation and review.

PDF Splitting and Certificate Handling: A key feature of our system is its ability to split PDF documents based on specific certificate numbers identified during the extraction process. Each page associated with a certificate number is saved individually, ensuring that all related information is grouped appropriately and can be accessed conveniently.

AWS Integration: Unlike typical implementations that may rely on serverless functions like AWS Lambda, our architecture utilizes AWS EC2 instances for robust processing capabilities along with AWS S3 buckets for secure and scalable storage. This setup ensures that our application can handle extensive processing loads while providing reliable and accessible storage solutions.

Security and Scalability: Our application is designed with security at the forefront, implementing robust encryption for data at rest and comprehensive access controls to safeguard data integrity and confidentiality. The use of AWS EC2 and S3 also enhances the scalability of our system, allowing it to efficiently handle growing data volumes and user demands without compromising performance.

These features collectively contribute to a powerful platform capable of handling complex PDF processing tasks while ensuring data security and system scalability.

## Vision

Our primary goal was to radically enhance the existing system by creating a more versatile and generic solution capable of handling all types of PDF certificates efficiently. This initiative was driven by the need to overcome the limitations observed in the previous team’s design and to align more closely with our clients' evolving requirements.

Once fully implemented, our application is set to transform the PDF processing landscape. It features advanced text extraction capabilities using the Pdfplumber library, seamlessly integrated with Amazon S3 for robust data handling, and maintains our standard practice of generating detailed Excel files. This combination not only meets but exceeds the functional needs of our users by providing a comprehensive solution for extracting and managing data from PDF documents.

For Intebloc clients, the enhanced system has significantly reduced onboarding times—by up to 90%. This improvement streamlines the process of integrating new clients, allowing for quicker access to vital information and a smoother transition into the system. Our build ultimately achieves the client's goals by rectifying deficiencies in the previous design and setting a new standard for efficiency and utility in PDF management.


## Requirements
All the packages and libraries required for this application to run can be found in requirements.txt file.

### Installation Steps
   1. Clone or download the repository as follows:
      ``` bash
      git clone https://github.com/SiyuR2023/TeamEcho2024.git
      ```
      or extract the folder with the codebase if you have the zipped folder.
   2. Use these commands to set things up:
      Ensures you have python installed and properly configured in your IDE.
      Set up and activate the virtual environment at the same level as the 'manage.py file'. Navigate to the project folder (pdfcoord)- cd TeamEcho2024/pdfcoord and execute the following commands in the terminal:
      ``` bash
      python -m venv env
      source env/bin/activate # This activates the virtual environment for mac os
      source env/Scripts/activate # For window os

      ```

   3. Install the requirements by executing the following command in the terminal:
         ```
         pip install -r requirements.txt
         ```
   4. start the server by running the command and also run migration:
         ```bash
         python manage.py migrate
         python manage.py runserver # on local machine
         ```
   5. Launch the application to your browser at this IP http://127.0.0.1:8000/    

## Testing the build
To test the build deactivate the server (ctrl + C) and run the following commands.
```bash
pytest
```
## Running the Application

To utilize our application, begin by uploading a PDF certificate along with a keyword that corresponds to the desired template. This can be done through the user interface which allows for intuitive interaction with the PDF document.

Once the PDF is uploaded, you can select specific data to extract by drawing rectangles around desired sections directly on the displayed PDF image. These coordinates can be saved for each section on the page or across a range of pages, ensuring that all necessary data is captured according to user-defined parameters.

After specifying all the desired extraction areas, submit these coordinates for processing. The system then extracts the data and generates outputs in two forms: Excel files and split PDF pages. The split PDF pages are particularly useful as they are saved with the certificate number for easy reference and organization.

The application provides a streamlined process from the initial upload to the final retrieval of organized data, enhancing efficiency and user experience. Access your processed Excel outputs and corresponding PDF pages directly through the application’s interface.

## Deployment
This application supports AWS deployment by leveraging AWS EC2 service's serverless architecture, and currently deployed at http://54.225.210.49/. Please refer to the deployment.md file in the production dir to know more about AWS deployment.

## Team Members
- SAMUEL AMAO

- SIYU REN
  
- EDWARD NKANSAH
  
- PAIVANIEMI ROOPE EEMELI
  
- ZHISHUO FANG

- LUO CHUANWANG
