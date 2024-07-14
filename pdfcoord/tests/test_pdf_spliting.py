import unittest
from unittest.mock import mock_open, patch, MagicMock
import json
import sys, os
# Add the directory containing excel_management.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from pdf_splitting import load_search_results, split_pdf_by_values, create_zip_file, clean_up_files

class TestPDFSplitting(unittest.TestCase):

    def setUp(self):
        self.pdf_path = "tests/test_media/sparrows.pdf"
        self.json_path = "tests/test_media/certNo_results.json"
        self.output_dir = "tests/output"
        self.search_results = {
            "1": {"1": ["Value1", "Value2"]},
            "2": {"2": ["Value3"]}
        }
        self.filenames = [
            os.path.join(self.output_dir, 'Value1_Page_1.pdf'),
            os.path.join(self.output_dir, 'Value2_Page_1.pdf'),
            os.path.join(self.output_dir, 'Value3_Page_2.pdf')
        ]

    @patch("builtins.open", new_callable=mock_open, read_data='{"1": {"1": ["Value1", "Value2"]}, "2": {"2": ["Value3"]}}')
    def test_load_search_results(self, mock_file):
        results = load_search_results(self.json_path)
        self.assertEqual(results, self.search_results)
        mock_file.assert_called_once_with(self.json_path, 'r', encoding='utf-8')

    @patch("os.path.isfile", return_value=True)
    @patch("os.makedirs")
    @patch("PyPDF2.PdfReader")
    @patch("PyPDF2.PdfWriter")
    def test_split_pdf_by_values(self, mock_writer, mock_reader, mock_makedirs, mock_isfile):
        mock_pdf_reader_instance = MagicMock()
        mock_pdf_reader_instance.pages = [MagicMock(), MagicMock()]
        mock_reader.return_value = mock_pdf_reader_instance
        mock_pdf_writer_instance = mock_writer.return_value

        filenames = split_pdf_by_values(self.pdf_path, self.search_results, self.output_dir)
        self.assertEqual(filenames, self.filenames)
        mock_isfile.assert_called_once_with(self.pdf_path)
        # mock_makedirs.assert_called_once_with(self.output_dir, exist_ok=True)

    @patch("os.path.isfile", return_value=False)
    def test_split_pdf_by_values_file_not_found(self, mock_isfile):
        with self.assertRaises(FileNotFoundError):
            split_pdf_by_values(self.pdf_path, self.search_results, self.output_dir)

    @patch("zipfile.ZipFile.write")
    @patch("zipfile.ZipFile.close")
    @patch("zipfile.ZipFile.__init__", return_value=None)
    def test_create_zip_file(self, mock_zip_init, mock_zip_close, mock_zip_write):
        zip_filename = create_zip_file(self.output_dir, self.filenames)
        self.assertTrue(zip_filename.endswith("split_pdfs.zip"))
        mock_zip_write.assert_any_call(self.filenames[0], os.path.basename(self.filenames[0]))

    @patch("os.remove")
    def test_clean_up_files(self, mock_remove):
        clean_up_files(self.filenames)
        mock_remove.assert_any_call(self.filenames[0])
        mock_remove.assert_any_call(self.filenames[1])
        mock_remove.assert_any_call(self.filenames[2])

if __name__ == "__main__":
    unittest.main()