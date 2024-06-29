import os
import django
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'pdfcoord.pdfcoord.settings'
django.setup()

# test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pdfcoord.coordselector.models import PDFDocument
import json

class PDFCoordTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure the media directory exists
        os.makedirs('media', exist_ok=True)
        os.makedirs('media/transferred', exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Clean up the media directory
        for root, dirs, files in os.walk('media', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload_pdf')

        # Use the absolute path to the PDF file
        pdf_path = 'D:\\Download\\TeamEcho2024\\pdf_uploadedFiles\\sparrows.pdf'
        with open(pdf_path, 'rb') as pdf_file:
            self.pdf_file = SimpleUploadedFile("test.pdf", pdf_file.read(), content_type="application/pdf")

        # Create a sample PDFDocument instance
        self.document = PDFDocument.objects.create(file=self.pdf_file)

        # Now we can create URLs that use self.document.id
        self.select_coords_url = reverse('select_coords', kwargs={'pdf_id': self.document.id})
        self.submit_coords_url = reverse('submit_coordinates', kwargs={'pdf_id': self.document.id})

        # Sample session data
        self.client.session['selected_keyword'] = 'test_keyword'
        self.client.session.save()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coordselector/home.html')

    def test_upload_pdf_view_get(self):
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coordselector/upload_pdf.html')

    def test_upload_pdf_view_post(self):
        # Test uploading a new PDF file
        pdf_path = 'D:\\Download\\TeamEcho2024\\pdf_uploadedFiles\\sparrows.pdf'
        with open(pdf_path, 'rb') as pdf_file:
            response = self.client.post(self.upload_url, {
                'pdf_file': pdf_file,
                'new_keyword': 'test_keyword',
                'action': 'upload',
            })
            self.assertEqual(response.status_code, 302)  # Should redirect
            self.assertTrue(PDFDocument.objects.filter(file='test.pdf').exists())

    def test_select_coords_view_get(self):
        response = self.client.get(self.select_coords_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coordselector/select_coords.html')

    def test_select_coords_view_post(self):
        coords = {
            'coordinates': [{'x0': 10, 'y0': 10, 'x1': 50, 'y1': 50}],
            'start_page': 0,
            'end_page': 0,
            'keyword': 'test_keyword'
        }
        response = self.client.post(self.select_coords_url, json.dumps(coords), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_submit_coordinates_view_post(self):
        # Prepare coordinates JSON file for testing
        coords_per_page = {
            '0': [{'keyword': 'test_keyword', 'coordinates': [{'x0': 10, 'y0': 10, 'x1': 50, 'y1': 50}]}]
        }
        json_file_path = os.path.join('media', f'pdf_coords_{self.document.id}.json')
        with open(json_file_path, 'w') as f:
            json.dump(coords_per_page, f, indent=4)

        response = self.client.post(self.submit_coords_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

        # Check if final_coords.json exists in the transferred directory
        transfer_path = os.path.join('media', 'transferred', 'final_coords.json')
        self.assertTrue(os.path.exists(transfer_path))

        # Cleanup test files
        os.remove(json_file_path)
        os.remove(transfer_path)
