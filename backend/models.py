from django.db import models

class BudgetPCBuild(models.Model):
    """Budget PC Builds Table"""
    name = models.CharField(max_length=200)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    psu = models.CharField(max_length=100)
    cabinet = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class GamingPCBuild(models.Model):
    """Gaming PC Builds Table"""
    name = models.CharField(max_length=200)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    psu = models.CharField(max_length=100)
    cabinet = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class WorkstationPCBuild(models.Model):
    """Workstation PC Builds Table"""
    name = models.CharField(max_length=200)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    psu = models.CharField(max_length=100)
    cabinet = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class ProfessionalPCBuild(models.Model):
    """Professional & Enterprise PC Builds Table"""
    name = models.CharField(max_length=200)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    psu = models.CharField(max_length=100)
    cabinet = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class EnthusiastPCBuild(models.Model):
    """Enthusiast & Niche PC Builds Table"""
    name = models.CharField(max_length=200)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    psu = models.CharField(max_length=100)
    cabinet = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
