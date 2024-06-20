import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import PDFDocument
import fitz  # PyMuPDF
import json
import os
from PIL import Image
from django.conf import settings
from django.core.cache import cache
import shutil

def home(request):
    return render(request, 'coordselector/home.html')

def upload_pdf(request):
    if request.method == "POST":
        pdf_file = request.FILES['pdf_file']
        document = PDFDocument(file=pdf_file)
        document.save()
        return redirect('select_coords', pdf_id=document.id)
    return render(request, 'coordselector/upload_pdf.html')

def render_pdf_to_images(pdf_path):
    cache_key = f'pdf_images_{os.path.basename(pdf_path)}'
    doc = fitz.open(pdf_path)
    img_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_images')

    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
    os.makedirs(img_dir, exist_ok=True)

    img_paths = []

    try:
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            img_path = os.path.join(img_dir, f'page_{page_number}.png')
            img.save(img_path)
            img_rel_path = os.path.relpath(img_path, settings.MEDIA_ROOT)
            img_url = os.path.join(settings.MEDIA_URL, img_rel_path)
            img_paths.append(img_url)
    except Exception as e:
        print(f"Error rendering PDF: {e}")

    cache.set(cache_key, img_paths, timeout=3600)
    
    return img_paths

def select_coords(request, pdf_id, page_number=0):
    document = get_object_or_404(PDFDocument, pk=pdf_id)
    pdf_path = document.file.path
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        coordinates = data.get('coordinates', [])
        start_page = data.get('start_page', 0)
        end_page = data.get('end_page', start_page)
        keyword = data.get('keyword', 'default_keyword')

        coords_per_page = {}

        json_file_path = os.path.join(settings.MEDIA_ROOT, f'pdf_coords_{pdf_id}.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                coords_per_page = json.load(f)

        coords_per_page = {str(k): v for k, v in coords_per_page.items()}

        for page in range(start_page, end_page + 1):
            page_key = str(page)
            if page_key in coords_per_page:
                coords_per_page[page_key].append({"keyword": keyword, "coordinates": coordinates})
            else:
                coords_per_page[page_key] = [{"keyword": keyword, "coordinates": coordinates}]

        with open(json_file_path, 'w') as f:
            json.dump(coords_per_page, f, indent=4)
        
        return JsonResponse({'status': 'success'})

    img_paths = render_pdf_to_images(pdf_path)
    img_path = os.path.relpath(img_paths[page_number], settings.MEDIA_ROOT)
    img_url = f"{settings.MEDIA_URL}{img_path}"

    previous_page = page_number - 1 if page_number > 0 else None
    next_page = page_number + 1 if page_number < total_pages - 1 else None

    context = {
        'img_url': img_url,
        'pdf_id': pdf_id,
        'current_page': page_number,
        'total_pages': total_pages,
        'previous_page': previous_page,
        'next_page': next_page,
        'csrf_token': request.META.get('CSRF_COOKIE')
    }
    return render(request, 'coordselector/select_coords.html', context)


def submit_coordinates(request, pdf_id):
    if request.method == "POST":
        json_file_path = os.path.join(settings.MEDIA_ROOT, f'pdf_coords_{pdf_id}.json')
        final_json_file_path = os.path.join(settings.MEDIA_ROOT, 'final_coords.json')

        if not os.path.exists(final_json_file_path):
            with open(final_json_file_path, 'w') as f:
                json.dump({}, f)  # Initialize with an empty dictionary

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                coords_per_page = json.load(f)
            
            with open(final_json_file_path, 'w') as f:
                json.dump(coords_per_page, f, indent=4)
            
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No coordinates found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
