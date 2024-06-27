# import unittest

# class TestPdfSplitting(unittest.TestCase):

#     def test_split_pdf(self):
#         # Your test code here
#         pass

# if __name__ == '__main__':
#     unittest.main()


# import unittest
# from unittest.mock import patch, mock_open, MagicMock
# import sys
# import os

# # Add the directory containing pdf_spliting.py to the path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import pdf_spliting  # Assuming the script is named pdf_spliting.py

# class TestPdfSplitting(unittest.TestCase):

#     @patch('pdf_spliting.open', new_callable=mock_open)
#     @patch('pdf_spliting.PyPDF2.PdfReader')
#     @patch('pdf_spliting.PyPDF2.PdfWriter')
#     def test_split_pdf(self, MockPdfWriter, MockPdfReader, mock_open):
#         # Setup mocks
#         mock_pdf_reader = MagicMock()
#         mock_pdf_reader.pages = [MagicMock(), MagicMock(), MagicMock()]
#         MockPdfReader.return_value = mock_pdf_reader
        
#         mock_pdf_writer = MagicMock()
#         MockPdfWriter.return_value = mock_pdf_writer
        
#         # Call the function
#         input_pdf_path = '/path/to/input.pdf'
#         output_dir = '/path/to/output/dir'
#         num_pages = pdf_spliting.split_pdf(input_pdf_path, output_dir)
        
#         # Assert the results
#         self.assertEqual(num_pages, 3)
#         self.assertEqual(mock_open.call_count, 7)  # 1 for input and 3 for output, 3 for reader context

#         # Check if PdfWriter was called three times
#         self.assertEqual(MockPdfWriter.call_count, 3)
#         # Ensure each page was written to a separate file
#         for i in range(3):
#             mock_pdf_writer.add_page.assert_any_call(mock_pdf_reader.pages[i])
#             mock_pdf_writer.write.assert_any_call(mock_open())

# if __name__ == '__main__':
#     unittest.main()


import unittest
from unittest.mock import mock_open, patch
import json
import pdf_spliting


# Assuming the load_search_results function is defined in a module named search_module
# from search_module import load_search_results

def load_search_results(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

class TestLoadSearchResults(unittest.TestCase):
    def test_load_search_results(self):
        # Sample JSON data
        sample_data = {"key": "value"}
        sample_json = json.dumps(sample_data)
        
        # Mock open to simulate file reading
        with patch('builtins.open', mock_open(read_data=sample_json)) as mocked_file:
            # Mock json.load to return the sample data
            with patch('json.load', return_value=sample_data):
                # Call the function
                result = load_search_results('dummy_path.json')
                
                # Assertions
                mocked_file.assert_called_once_with('dummy_path.json', 'r', encoding='utf-8')
                self.assertEqual(result, sample_data)

    def test_split_pdf_by_values(self):
        

if __name__ == '__main__':
    unittest.main()

