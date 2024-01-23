from django.db import models
from django.db.models import Sum, Avg, Count, Min, Max
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime, timedelta


class Omnicell(models.Model):
    """ Class for storing Omnicells """

    #Fields
    id = models.BigAutoField(primary_key=True)
    Omni_Id = models.CharField(max_length=50, blank=True, null=True)
    Omni_Description = models.CharField(max_length=50, blank=True, null=True)
    # Site = ?
    # Type = ?

    # Metadata
    class Meta:
        ordering = ['id']
    
    # Methods
    def __str__(self):
        return str(self.Omni_Id)

class Refrigerator(models.Model):
    """ Class for storing Refrigerators """

    #Fields
    id = models.BigAutoField(primary_key=True)
    Facilities_Id = models.CharField(max_length=50, blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ['id']
    
    # Methods
    def __str__(self):
        return self.id

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