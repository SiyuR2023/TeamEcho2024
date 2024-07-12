import unittest
from unittest.mock import mock_open, patch
import json
import sys, os
# Add the directory containing excel_management.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from pdf_splitting import load_search_results, split_pdf_by_values

# Assuming the load_search_results function is defined in a module named search_module
# from search_module import load_search_results

# def load_search_results(json_path):
#     with open(json_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

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
        pass
        

if __name__ == "__main__":
    unittest.main()