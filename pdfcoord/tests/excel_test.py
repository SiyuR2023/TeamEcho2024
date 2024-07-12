import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys, os
import json
from openpyxl import Workbook

# Add the directory containing excel_management.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))


from excel_management import (
    preProcess, insertData, insertError, create_excel,
    modelProcess, manuProcess, dateProcess, swlProcess, jsonProcess
)

class TestExcelManagement(unittest.TestCase):

    def setUp(self):
        # This runs before each test
        self.workbook = Workbook()
        self.sheet_data = self.workbook.active

    def test_preProcess(self):
        column_mapping = {
            "Id Number": "A",
            "RFID": "B",
            "Item Category": "C"
        }
        preProcess(self.sheet_data, column_mapping)
        for header, column in column_mapping.items():
            cell = self.sheet_data[column + '2']
            self.assertEqual(cell.value, header)
            self.assertTrue(cell.font.bold)
            self.assertEqual(cell.alignment.horizontal, 'center')
            self.assertEqual(cell.alignment.vertical, 'center')

    def test_dateProcess(self):
        date_str = "12-12-2022"
        processed_date = dateProcess(date_str)
        self.assertEqual(processed_date, "12-12-2022")

        date_str = "12/Dec/2022"
        processed_date = dateProcess(date_str)
        self.assertEqual(processed_date, "12/Dec/2022")

        date_str = "Invalid Date"
        processed_date = dateProcess(date_str)
        self.assertEqual(processed_date, "Invalid Date")

    

    def test_jsonProcess(self):
        # Mock a JSON file
        test_json_data = {"key": "value"}
        with patch('builtins.open', mock_open(read_data=json.dumps(test_json_data))):
            with patch('os.path.isfile', return_value=True):
                result = jsonProcess("fake_path.json")
                self.assertEqual(result, test_json_data)

        # Test non-existent file
        with patch('os.path.isfile', return_value=False):
            result = jsonProcess("non_existent_file.json")
            self.assertEqual(result, "non_existent_file.json")

    
if __name__ == '__main__':
    unittest.main()