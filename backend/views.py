# views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import PCBuild
import random

@api_view(['GET'])
def get_filtered_pc_builds(request):
    """Retrieve a single random PC build filtered by price, CPU type, or storage type."""
    price = request.GET.get('price')
    cpu = request.GET.get('cpu')
    storage = request.GET.get('storage')
    
    builds = PCBuild.objects.all()
    
    if price:
        builds = builds.filter(price__lte=price)  # Less than or equal to given price
    
    if cpu:
        builds = builds.filter(cpu__icontains=cpu)  # Matches CPU type (case-insensitive)
    
    if storage:
        builds = builds.filter(storage__icontains=storage)  # Matches storage type (case-insensitive)
    
    builds_list = list(builds.values())
    
    if builds_list:
        random_build = random.choice(builds_list)  # Select a random build if multiple exist
        return JsonResponse({'build': random_build})
    else:
        return JsonResponse({'message': 'No builds found matching criteria'}, status=404)