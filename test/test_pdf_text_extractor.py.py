import unittest
from unittest.mock import patch, Mock
import json
import pdfplumber
from io import BytesIO

class TestExtractTextFromCoordinates(unittest.TestCase):
    @patch('pdfplumber.open')
    def test_extract_text_from_coordinates(self, mock_pdfplumber_open):
        # 示例PDF和坐标数据
        pdf_path = 'sample.pdf'
        coordinates_dict = {
            "0": [
                {
                    "keyword": "example_keyword",
                    "coordinates": [{"x0": 10, "y0": 10, "x1": 50, "y1": 50}]
                }
            ]
        }

        # 模拟pdfplumber的页面对象及其方法
        mock_page = Mock()
        mock_page.width = 100
        mock_page.height = 100
        mock_page.within_bbox.return_value.extract_text.return_value = "示例文本"
        
        # 模拟pdfplumber的pdf对象
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page]
        
        # 设置pdfplumber.open的返回值
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf
        
        # 运行函数
        from genericPDF_extract import extract_text_from_coordinates  # 将 'genericPDF_extract' 替换为实际模块名
        extracted_texts = extract_text_from_coordinates(pdf_path, coordinates_dict)
        
        # 预期结果
        expected_result = {
            "example_keyword": ["示例文本", {"completed": True}]
        }
        
        # 断言
        self.assertEqual(extracted_texts, expected_result)
        mock_page.within_bbox.assert_called_with((10, 10, 50, 50))

    @patch('pdfplumber.open')
    def test_page_out_of_range(self, mock_pdfplumber_open):
        pdf_path = 'sample.pdf'
        coordinates_dict = {
            "2": [
                {
                    "keyword": "out_of_range",
                    "coordinates": [{"x0": 10, "y0": 10, "x1": 50, "y1": 50}]
                }
            ]
        }

        # 模拟只有一页的pdfplumber的pdf对象
        mock_pdf = Mock()
        mock_pdf.pages = [Mock()]

        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

        from genericPDF_extract import extract_text_from_coordinates  # 将 'genericPDF_extract' 替换为实际模块名
        extracted_texts = extract_text_from_coordinates(pdf_path, coordinates_dict)

        expected_result = {
            "out_of_range": ["Page number out of range.", {"completed": True}]
        }

        self.assertEqual(extracted_texts, expected_result)

    @patch('pdfplumber.open')
    def test_bounding_box_out_of_bounds(self, mock_pdfplumber_open):
        pdf_path = 'sample.pdf'
        coordinates_dict = {
            "0": [
                {
                    "keyword": "out_of_bounds",
                    "coordinates": [{"x0": 10, "y0": 10, "x1": 200, "y1": 200}]
                }
            ]
        }

        mock_page = Mock()
        mock_page.width = 100
        mock_page.height = 100
        
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page]

        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

        from genericPDF_extract import extract_text_from_coordinates  # 将 'genericPDF_extract' 替换为实际模块名
        extracted_texts = extract_text_from_coordinates(pdf_path, coordinates_dict)

        expected_result = {
            "out_of_bounds": ["Bounding box is outside the page bounds.", {"completed": True}]
        }

        self.assertEqual(extracted_texts, expected_result)

if __name__ == '__main__':
    unittest.main()
