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