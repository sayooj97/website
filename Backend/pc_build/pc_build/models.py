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
