# settings.py additions
# Add these to your Django settings.py file

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Create a folder for storing CSV files
CSV_DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(CSV_DATA_DIR, exist_ok=True)

# management/commands/initialize_data.py
from django.core.management.base import BaseCommand
from .utils import initialize_categories

class Command(BaseCommand):
    help = 'Initialize the database with PC build categories and subcategories'

    def handle(self, *args, **options):
        initialize_categories()
        self.stdout.write(self.style.SUCCESS('Successfully initialized PC build categories and subcategories'))
