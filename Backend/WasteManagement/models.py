from django.db import models
from django.utils import timezone

class wasteManagement(models.Model):
    wasteManagement_Id = models.AutoField(primary_key=True)
    date=models.DateField()
    wasteCategory=models.CharField(max_length=20,blank=True,null=True)
    wasteColor=models.CharField(max_length=20,blank=True,null=True)
    bagCount=models.IntegerField()
    weight=models.IntegerField()
    description=models.TextField()

    
    class Meta:
        db_table = 'wasteManagement'

class WasteCount(models.Model):
    WasteCount_Id = models.AutoField(primary_key=True)
    date=models.DateField(default=timezone.now)
    wasteCategory=models.CharField(max_length=20)
    wasteColor=models.CharField(max_length=20)
    weight=models.IntegerField()
    totalWst=models.IntegerField()
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'WasteCount'
    
class handOver(models.Model):
    handOver_Id = models.AutoField(primary_key=True)
    date=models.DateField(default=timezone.now)
    wasteCategory=models.CharField(max_length=20)
    wasteColor=models.CharField(max_length=20)
    weight=models.IntegerField()
    collecter=models.CharField(max_length=50)
    collecterCnt=models.BigIntegerField()
    incharge=models.CharField(max_length=50)

    class Meta:
        db_table = 'handOver'







# class bioWaste(models.Model):
#     wst_type=models.CharField(max_length=50)
#     wst_color=models.CharField(max_length=30)
#     bag_count=models.IntegerField()
#     weight=models.IntegerField()
#     date=models.DateField()

#     def __str__(self):
#         return self.wst_type


# class GenrelWaste(models.Model):
#     wst_type=models.CharField(max_length=50)
#     bag_count=models.IntegerField()
#     weight=models.IntegerField()
#     date=models.DateField()

#     def __str__(self):
#         return self.wst_type
    

# class eWaste(models.Model):
#     wst_type=models.CharField(max_length=50)
#     bag_count=models.IntegerField()
#     weight=models.IntegerField()
#     date=models.DateField()

#     def __str__(self):
#         return self.wst_type
    

    