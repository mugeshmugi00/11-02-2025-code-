from django import forms
from .models import *
from django.db import models
from django.db.models import Max
 
 
class AssetCategory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
 
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
 
    class Meta:
        db_table = 'AssetCategory'
   
    def save(self, *args, **kwargs):
        # Using the default 'id' field for the primary key
        if not self.id:
            max_id = AssetCategory.objects.aggregate(
                max_id=Max('id')
            )['max_id']
            self.id = (max_id or 0) + 1  
        super().save(*args, **kwargs)
 
# ------------------------------------------------AssetSubCategory----------------------------------------------
class AssetSubCategory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    name = models.CharField(max_length=255)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='subcategories')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
 
    class Meta:
        db_table = 'AssetSubCategory'
        unique_together = ('name', 'category')
       
    def save(self, *args, **kwargs):
    # Using the default 'id' field for the primary key
        if not self.id:
            max_id = AssetSubCategory.objects.aggregate(
                max_id=Max('id')
            )['max_id']
            self.id = (max_id or 0) + 1  
        super().save(*args, **kwargs)
        
#------------------------------------------Supplier-----------------------------------------------------
class Supplier(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    email = models.EmailField(unique=True)
    asset_category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='suppliers')
    subcategories = models.ManyToManyField(AssetSubCategory, related_name='suppliers')  # Add this line
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    ranking = models.IntegerField(default=1)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Supplier'

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = Supplier.objects.aggregate(max_id=Max('id'))['max_id']
            self.id = (max_id or 0) + 1
        super().save(*args, **kwargs)
        
#  -------------------------------------ServiceProviderManagement----------------------------------

class Asset_ServiceProviderManagement(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    SERVICE_QUALITY_CHOICES = [
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ]
    
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    asset_categories = models.ManyToManyField(AssetCategory,blank=True)
    subcategories = models.ManyToManyField(AssetSubCategory, blank=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    cost_effective = models.BooleanField(default=True)
    service_quality = models.CharField(max_length=10, choices=SERVICE_QUALITY_CHOICES, default='fair')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average_response_time = models.CharField(max_length=50, default='1 day')
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    ranking = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'Asset_ServiceProviderManagement'
        
    def save(self, *args, **kwargs):
        if not self.id:
            max_id = Asset_ServiceProviderManagement.objects.aggregate(max_id=Max('id'))['max_id']
            self.id = (max_id or 0) + 1
        super().save(*args, **kwargs)
        
# --------------------------------------ChecklistMasterEntry---------------------------------------

class ChecklistMasterEntry(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
     
    item_name  = models.CharField(max_length=255)
    asset_category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='ChecklistMasterEntry')
    subcategories = models.ManyToManyField(AssetSubCategory, related_name='ChecklistMasterEntry')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    class Meta:
        db_table = 'ChecklistMasterEntry'

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = ChecklistMasterEntry.objects.aggregate(max_id=Max('id'))['max_id']
            self.id = (max_id or 0) + 1
        super().save(*args, **kwargs)
        
# -------------------------------------Asset Reg--------------------------------------
class AssetReg_Data(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=250)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='asset_registrations')
    asset_subcategory = models.ManyToManyField(AssetSubCategory, related_name='asset_registrations')
    supplier = models.ManyToManyField(Supplier, blank=True)
    Company_Brand= models.CharField(max_length=500)
    # department = models.ManyToManyField(Department, related_name='asset_registrations', blank=True)
    current_location = models.CharField(max_length=500)
    room_no = models.CharField(max_length=50)
    condition = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    market_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_working_life = models.IntegerField(null=True, blank=True)
    expected_working_life = models.IntegerField(null=True, blank=True)
    valuation_method = models.CharField(max_length=250, null=True, blank=True)
    is_new_asset = models.BooleanField(default=True)
    depreciation_method = models.CharField(max_length=250, null=True, blank=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    salvage_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    appreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'AssetReg_Data'

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = AssetReg_Data.objects.aggregate(max_id=Max('id'))['max_id']
            self.id = (max_id or 0) + 1
        super().save(*args, **kwargs)
        
    # ----------------------------------------------------------------------------------------------------

class AssetList(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('bad', 'Bad'),
    ]

    VALUATION_CHOICES = [
        ('none', 'None'),
        ('depreciated', 'Depreciated'),
        ('appreciation','Appreciation'),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey('AssetCategory', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('AssetSubCategory', on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    valuation_method = models.CharField(max_length=50, choices=VALUATION_CHOICES)

    class Meta:
        db_table = 'AssetList'

    def save(self, *args, **kwargs):
        if not self.pk: 
            max_id = AssetList.objects.aggregate(max_id=Max('id'))['max_id']
            self.id = (max_id or 0) + 1
        super().save(*args, **kwargs)
