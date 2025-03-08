# models.py
from django.db import models

class PCBuildCategory(models.Model):
    """Model representing the main PC build categories"""
    name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class PCBuildSubCategory(models.Model):
    """Model representing sub-categories within each main category"""
    category = models.ForeignKey(PCBuildCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class PCPart(models.Model):
    """Model representing individual PC parts"""
    TYPE_CHOICES = (
        ('CPU', 'CPU'),
        ('GPU', 'GPU'),
        ('RAM', 'RAM'),
        ('Storage', 'Storage'),
        ('Motherboard', 'Motherboard'),
        ('PSU', 'Power Supply'),
        ('Case', 'Case'),
        ('Cooling', 'Cooling'),
        ('Other', 'Other'),
    )
    
    subcategory = models.ForeignKey(PCBuildSubCategory, on_delete=models.CASCADE, related_name='parts')
    part_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    specifications = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.part_type} - {self.name}"

# utils.py
import csv
import os
from django.conf import settings
from .models import PCBuildCategory, PCBuildSubCategory, PCPart

def initialize_categories():
    """Initialize the database with the main categories and subcategories"""
    categories = [
        {
            'name': 'Budget PC Builds',
            'file_name': 'buget_pc_build.csv',
            'subcategories': [
                {'name': 'Student PC', 'description': 'Affordable build for online classes, coding, and research.'},
                {'name': 'Office Workstation', 'description': 'Optimized for productivity apps like MS Office, Zoom, and web browsing.'},
                {'name': 'Casual Home PC', 'description': 'General-purpose PC for browsing, media streaming, and light tasks.'},
                {'name': 'Low-Cost Gaming PC', 'description': 'Entry-level gaming rig with budget-friendly GPU and CPU.'},
            ]
        },
        {
            'name': 'Gaming PC Builds',
            'file_name': 'gamming_pc_build.csv',
            'subcategories': [
                {'name': 'Entry-Level Gaming PC', 'description': '1080p gaming on medium settings, targeting esports titles.'},
                {'name': 'Mid-Range Gaming PC', 'description': 'Balanced performance for 1080p/1440p gaming.'},
                {'name': 'High-End Gaming PC', 'description': '1440p/4K gaming with high FPS.'},
                {'name': 'Competitive eSports PC', 'description': 'High refresh rate gaming (240Hz+) for games like CS2, Valorant, and Apex.'},
                {'name': 'VR-Ready Gaming PC', 'description': 'Optimized for VR gaming performance.'},
                {'name': 'Streaming & Gaming Hybrid PC', 'description': 'Designed for gaming and live streaming simultaneously.'},
            ]
        },
        {
            'name': 'Workstation PC Builds',
            'file_name': 'workstation_pc_buils.csv',
            'subcategories': [
                {'name': 'Video Editing Workstation', 'description': 'Optimized for Adobe Premiere Pro, DaVinci Resolve.'},
                {'name': '3D Rendering & Animation PC', 'description': 'High-end GPUs and CPUs for Blender, Maya, Cinema 4D.'},
                {'name': 'CAD & Engineering Workstation', 'description': 'Best for AutoCAD, SolidWorks, and simulations.'},
                {'name': 'Music Production Workstation', 'description': 'Low-latency setup for DAWs like FL Studio, Ableton, Logic Pro.'},
                {'name': 'AI & Machine Learning PC', 'description': 'High-core CPU and powerful GPU for TensorFlow, PyTorch.'},
                {'name': 'Software Development PC', 'description': 'Ideal for coding, virtualization, and compiling large projects.'},
            ]
        },
        {
            'name': 'Professional & Enterprise Use',
            'file_name': 'professional_and_enterprise_use.csv',
            'subcategories': [
                {'name': 'Business Workstation', 'description': 'Secure and reliable for enterprise applications.'},
                {'name': 'Financial Trading PC', 'description': 'Multi-monitor setup for stock trading and financial analysis.'},
                {'name': 'Server & Home Lab PC', 'description': 'Custom NAS, virtualization, or hosting solutions.'},
                {'name': 'Medical & Scientific Computing PC', 'description': 'For simulations, medical imaging, and data analysis.'},
            ]
        },
        {
            'name': 'Enthusiast & Niche Builds',
            'file_name': 'enthusiast_and_niche_builds.csv',
            'subcategories': [
                {'name': 'Overclocking Enthusiast PC', 'description': 'Designed for extreme CPU and GPU overclocking.'},
                {'name': 'Silent PC Build', 'description': 'Noise-optimized setup with fanless or low-noise components.'},
                {'name': 'Mini ITX Compact PC', 'description': 'Small form factor build with high performance.'},
                {'name': 'Modding & Custom Water Cooling Build', 'description': 'High-end aesthetics with custom cooling loops.'},
                {'name': 'Energy-Efficient PC', 'description': 'Low-power consumption for eco-conscious users.'},
            ]
        },
    ]
    
    for category_data in categories:
        category, created = PCBuildCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={'file_name': category_data['file_name']}
        )
        
        for subcategory_data in category_data['subcategories']:
            PCBuildSubCategory.objects.get_or_create(
                category=category,
                name=subcategory_data['name'],
                defaults={'description': subcategory_data['description']}
            )

def parse_csv_file(file_path, subcategory):
    """Parse a CSV file and extract PC parts for the given subcategory"""
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            parts_data = []
            
            for row in reader:
                # Check if this row belongs to the selected subcategory
                if row.get('name') == subcategory.name:
                    # Parse the components from the CSV
                    part = {
                        'subcategory': subcategory,
                        'part_type': row.get('part_type', 'Other'),
                        'name': row.get('part_name', ''),
                        'brand': row.get('brand', ''),
                        'model': row.get('model', ''),
                        'price': float(row.get('price', 0)),
                        'specifications': {
                            key: value for key, value in row.items()
                            if key not in ['name', 'part_type', 'part_name', 'brand', 'model', 'price']
                        }
                    }
                    parts_data.append(part)
            
            return parts_data
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
        return []

def get_pc_build_recommendations(category_name, subcategory_name):
    """Get PC build recommendations based on category and subcategory"""
    try:
        category = PCBuildCategory.objects.get(name=category_name)
        subcategory = PCBuildSubCategory.objects.get(category=category, name=subcategory_name)
        
        # Check if we already have parts for this subcategory in the database
        if PCPart.objects.filter(subcategory=subcategory).exists():
            return PCPart.objects.filter(subcategory=subcategory)
        
        # If not, parse the CSV file and save the parts
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', category.file_name)
        parts_data = parse_csv_file(csv_file_path, subcategory)
        
        # Save the parts to the database
        for part_data in parts_data:
            PCPart.objects.create(**part_data)
        
        return PCPart.objects.filter(subcategory=subcategory)
    except (PCBuildCategory.DoesNotExist, PCBuildSubCategory.DoesNotExist):
        return []
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return []

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PCBuildCategory, PCBuildSubCategory, PCPart
from .utils import get_pc_build_recommendations

@api_view(['GET'])
def get_categories(request):
    """API endpoint to get all main categories"""
    categories = PCBuildCategory.objects.all()
    data = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return Response(data)

@api_view(['GET'])
def get_subcategories(request, category_id):
    """API endpoint to get subcategories for a specific category"""
    try:
        category = PCBuildCategory.objects.get(id=category_id)
        subcategories = category.subcategories.all()
        data = [{'id': subcat.id, 'name': subcat.name, 'description': subcat.description} 
                for subcat in subcategories]
        return Response(data)
    except PCBuildCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

@api_view(['GET'])
def get_recommendations(request):
    """API endpoint to get PC part recommendations based on category and subcategory"""
    category_name = request.GET.get('category')
    subcategory_name = request.GET.get('subcategory')
    
    if not category_name or not subcategory_name:
        return Response({'error': 'Category and subcategory are required'}, status=400)
    
    parts = get_pc_build_recommendations(category_name, subcategory_name)
    
    # Group parts by type
    parts_by_type = {}
    for part in parts:
        if part.part_type not in parts_by_type:
            parts_by_type[part.part_type] = []
        
        parts_by_type[part.part_type].append({
            'id': part.id,
            'name': part.name,
            'brand': part.brand,
            'model': part.model,
            'price': float(part.price),
            'specifications': part.specifications
        })
    
    return Response({
        'category': category_name,
        'subcategory': subcategory_name,
        'parts': parts_by_type
    })

@csrf_exempt
@api_view(['POST'])
def upload_csv(request):
    """API endpoint to upload and process a new CSV file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    category_name = request.POST.get('category')
    
    if not category_name:
        return Response({'error': 'Category name is required'}, status=400)
    
    try:
        # Save the uploaded file
        file_path = os.path.join(settings.MEDIA_ROOT, 'csv', file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Update or create the category
        category, created = PCBuildCategory.objects.get_or_create(
            name=category_name,
            defaults={'file_name': file.name}
        )
        
        return Response({
            'success': True,
            'message': f"CSV file uploaded for category '{category_name}'",
            'category_id': category.id
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/categories/<int:category_id>/subcategories/', views.get_subcategories, name='get_subcategories'),
    path('api/recommendations/', views.get_recommendations, name='get_recommendations'),
    path('api/upload-csv/', views.upload_csv, name='upload_csv'),
]

# settings.py additions
# Add these to your Django settings.py file

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Create a folder for storing CSV files
CSV_DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(CSV_DATA_DIR, exist_ok=True)

# management/commands/initialize_data.py
from django.core.management.base import BaseCommand
from ....utils import initialize_categories

class Command(BaseCommand):
    help = 'Initialize the database with PC build categories and subcategories'

    def handle(self, *args, **options):
        initialize_categories()
        self.stdout.write(self.style.SUCCESS('Successfully initialized PC build categories and subcategories'))
