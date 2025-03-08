# views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import BudgetPCBuild, GamingPCBuild, WorkstationPCBuild, ProfessionalPCBuild, EnthusiastPCBuild
import random

CATEGORY_MAP = {
    'budget': BudgetPCBuild,
    'gaming': GamingPCBuild,
    'workstation': WorkstationPCBuild,
    'professional': ProfessionalPCBuild,
    'enthusiast': EnthusiastPCBuild
}

@api_view(['GET'])
def get_filtered_pc_builds(request):
    """Retrieve a single random PC build filtered by category (table name), subcategory (PC build name), and price."""
    category = request.GET.get('category')  # Table name
    subcategory = request.GET.get('subcategory')  # Name inside the table
    price = request.GET.get('price')  # Budget constraint
    
    if not category or category not in CATEGORY_MAP:
        return JsonResponse({'error': 'Invalid or missing category'}, status=400)
    
    builds = CATEGORY_MAP[category].objects.all()
    
    if subcategory:
        builds = builds.filter(name__icontains=subcategory)  # Matches subcategory (PC build name)
    
    if price:
        builds = builds.filter(price__lte=price)  # Filters by price (budget constraint)
    
    builds_list = list(builds.values())
    
    if builds_list:
        random_build = random.choice(builds_list)  # Select a random build if multiple exist
        return JsonResponse({'build': random_build})
    else:
        return JsonResponse({'message': 'No builds found matching criteria'}, status=404)
