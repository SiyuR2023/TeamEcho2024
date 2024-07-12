import unittest
import json
import sys, os
# Add the directory containing excel_management.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from extract_certNo import extract_certificate_no, save_results_to_file

class TestExtractCertificateNo(unittest.TestCase):

    def setUp(self):
        # Set the initial data required for the test
        self.test_data = {
            "Certificate No": [
                "SB343913",
                "SB343931",
                123,  # This is an integer, and should be filtered out
                "SB343944"
            ],
            "Other Key": [
                "Some other value"
            ]
        }
        self.expected_output = {
            "certificate no": {
                "1": ["SB343913"],
                "2": ["SB343931"],
                "3": ["SB343944"]
            }
        }

    def test_extract_certificate_no(self):
        # Test that the extract_certificate_no function works as expected
        result = extract_certificate_no(self.test_data)
        self.assertEqual(result, self.expected_output)

    def test_save_results_to_file(self):
        # Test that the save_results_to_file function works as expected
        output_file = 'test_output.json'
        save_results_to_file(self.expected_output, output_file)
        
        with open(output_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        self.assertEqual(data, self.expected_output)

if __name__ == "__main__":
    unittest.main()