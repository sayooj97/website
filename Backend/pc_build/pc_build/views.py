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