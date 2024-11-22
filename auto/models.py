from django.db import models
from django.db.models import Sum, Avg, Count, Min, Max
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime, timedelta

class User(AbstractUser):
    pass

class Omnicell(models.Model):
    """ Class for storing Omnicells """

    #Fields
    id = models.BigAutoField(primary_key=True)
    Omni_Id = models.CharField(max_length=50, blank=True, null=True)
    Omni_Description = models.CharField(max_length=50, blank=True, null=True)
    Serial_Number = models.CharField(max_length=7, blank=True, null=True)
    Model = models.ForeignKey("OmnicellModel", on_delete=models.SET_NULL, blank=True, null=True)
    CT_Version = models.CharField(max_length=10, blank=True, null=True)
    PC_Name = models.CharField(max_length=20, blank=True, null=True)
    Ivanti = models.BooleanField(default=False)
    
    Site = models.ForeignKey("Site", on_delete=models.SET_NULL, blank=True, null=True)
    Building = models.ForeignKey("Building", on_delete=models.SET_NULL, blank=True, null=True)
    Area = models.CharField(max_length=10, blank=True, null=True)
    Room = models.CharField(max_length=10, blank=True, null=True)
    Door_Code = models.CharField(max_length=10, blank=True, null=True)
    Emergency = models.BooleanField(default=False)
    Note = models.TextField(max_length=500, blank=True, null=True)
    
    Port_Name = models.CharField(max_length=10, blank=True, null=True)
    

    # Metadata
    class Meta:
        ordering = ['Omni_Id', 'Site', 'Building', 'Area']
    
    # Methods
    def __str__(self):
        return str(self.Omni_Id)

class Aux(models.Model):
    """ Class for storing Aux Towers """

    #Fields
    id = models.BigAutoField(primary_key=True)
    Omnicell = models.ForeignKey("Omnicell", on_delete=models.SET_NULL, blank=True, null=True)
    Serial_Number = models.CharField(max_length=7, blank=True, null=True)
    Model = models.ForeignKey("OmnicellModel", on_delete=models.SET_NULL, blank=True, null=True)   
    

    # Metadata
    class Meta:
        ordering = ['Omnicell', 'Model', 'Serial_Number']
    
    # Methods
    def __str__(self):
        return str(self.Model)

class Refrigerator(models.Model):
    """ Class for storing Refrigerators """

    #Fields
    id = models.BigAutoField(primary_key=True)
    Facilities_Id = models.CharField(max_length=50, blank=True, null=True)
    Omnicell = models.ForeignKey("Omnicell", on_delete=models.SET_NULL, blank=True, null=True)
    Type = models.CharField(max_length=50, blank=True, null=True)
    Model = models.ForeignKey("RefrigeratorModel", on_delete=models.SET_NULL, blank=True, null=True)
    Wheels = models.BooleanField(default=False)
    Broken = models.BooleanField(default=False)

    # Metadata
    class Meta:
        ordering = ['Omnicell', 'Type', 'Facilities_Id']
    
    # Methods
    def __str__(self):
        return str(self.Omnicell) + " | " + str(self.Facilities_Id)

class OmnicellModel(models.Model):
    """Class for storing Omnicell Models """

    #Fields
    id = models.BigAutoField(primary_key=True)
    Generation = models.CharField(max_length=5, blank=True, null=True)
    Model = models.CharField(max_length=50, blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ['Generation', 'Model']
    
    # Methods
    def __str__(self):
        return str(self.Generation+" "+self.Model)
    
class Site(models.Model):
    """ Class for storing Sites """

    #Fields
    id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=50, blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ['Name']
    
    # Methods
    def __str__(self):
        return self.Name
    
class Building(models.Model):
    """Class Description"""

    #Fields
    id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=50, blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ['Name']
    
    # Methods
    def __str__(self):
        return self.Name

class Lockbox(models.Model):
    """Class for storing lockboxes"""

    #Fields
    id = models.BigAutoField(primary_key=True)
    Refrigerator = models.ForeignKey("Refrigerator", on_delete=models.SET_NULL, blank=True, null=True)
    Key = models.CharField(max_length=10, blank=True, null=True)
    Medication = models.CharField(max_length=50, blank=True, null=True)
    Description = models.CharField(max_length=50, blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ['Refrigerator']
    
    # Methods
    def __str__(self):
        return str(self.Refrigerator) + " | " + str(self.Medication)

class RefrigeratorModel(models.Model):
    """Class Description"""

    #Fields
    id = models.BigAutoField(primary_key=True)
    Category = models.CharField(max_length=50, blank=True, null=True)
    ModelName = models.CharField(max_length=50, blank=True, null=True)
    Screen = models.BooleanField(default=False)
    Window = models.BooleanField(default=False)
    InteriorVolume = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    Height = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    Width = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    Depth = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)

    # Metadata
    class Meta:
        ordering = ['ModelName']
    
    # Methods
    def __str__(self):
        return self.ModelName


class portLocation(models.Model):
    """Class Description"""

    #Fields
    id = models.BigAutoField(primary_key=True)
    Description = models.CharField(max_length=50, blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ['id']
    
    # Methods
    def __str__(self):
        return self.Description

# class theclass(models.Model):
#     """Class Description"""

#     #Fields
#     id = models.BigAutoField(primary_key=True)

#     # Metadata
#     class Meta:
#         ordering = ['id']
    
#     # Methods
#     def __str__(self):
#         return self.id