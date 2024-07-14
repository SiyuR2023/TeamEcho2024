import unittest
import os
import sys
from unittest.mock import patch, mock_open
import pdfplumber

# Add the directory containing excel_management.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from genericPDF_extract import extract_text_from_coordinates, save_results_to_file

class TestExtractTextFromCoordinates(unittest.TestCase):

    def setUp(self):
        self.pdf_path = 'test.pdf'
        self.coordinates_dict = {
            "0": [
                {
                    "keyword": "Id Number",
                    "coordinates": [
                        {"x0": 10, "y0": 10, "x1": 50, "y1": 50}
                    ]
                }
            ]
        }
        self.invalid_coordinates_dict = {
            "0": [
                {
                    "keyword": "Id Number",
                    "coordinates": [
                        {"x0": -10, "y0": 10, "x1": 50, "y1": 50}
                    ]
                }
            ]
        }

    @patch('pdfplumber.open')
    def test_extract_text_from_valid_coordinates(self, mock_pdf_open):
        mock_pdf = unittest.mock.MagicMock()
        mock_page = unittest.mock.MagicMock()
        mock_page.width = 100
        mock_page.height = 100
        mock_page.within_bbox.return_value.extract_text.return_value = "Sample text"
        mock_pdf.pages = [mock_page]
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf

        result = extract_text_from_coordinates(self.pdf_path, self.coordinates_dict)
        expected_result = {
            "Id Number": ["Sample text"]
        }
        self.assertEqual(result, expected_result)

    @patch('pdfplumber.open')
    def test_extract_text_from_invalid_coordinates(self, mock_pdf_open):
        mock_pdf = unittest.mock.MagicMock()
        mock_page = unittest.mock.MagicMock()
        mock_page.width = 100
        mock_page.height = 100
        mock_page.within_bbox.return_value.extract_text.return_value = "Sample text"
        mock_pdf.pages = [mock_page]
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf

        result = extract_text_from_coordinates(self.pdf_path, self.invalid_coordinates_dict)
        expected_result = {
            "Id Number": ["Bounding box is outside the page bounds."]
        }
        self.assertEqual(result, expected_result)

    @patch('pdfplumber.open')
    def test_extract_text_from_non_existent_page(self, mock_pdf_open):
        mock_pdf = unittest.mock.MagicMock()
        mock_pdf.pages = []
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf

        result = extract_text_from_coordinates(self.pdf_path, self.coordinates_dict)
        expected_result = {
            "Id Number": ["Page number out of range."]
        }
        self.assertEqual(result, expected_result)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_results_to_file(self, mock_file_open):
        results = {
            "Id Number": ["Sample text"]
        }
        with patch('json.dump') as mock_json_dump:
            save_results_to_file(results, 'output.json')
            mock_json_dump.assert_called_once_with(results, mock_file_open(), indent=4)

if __name__ == '__main__':
    unittest.main()