from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from Inventory.models import (Product_Category_Product_Details)
from django.db import transaction


@receiver(post_save, sender=Finance_LedgerMasters_Detailes)
def insert_financeledger_mapping_tableinsert(sender, instance, created, **kwargs):
    # print('Signal for ledger finance:', instance)
    if created:
        try:
            with transaction.atomic():
                AllLedgers_Mapping_Detailes.objects.create(
                    TableName=Finance_LedgerMasters_Detailes,
                    TableId=instance.pk,
                    created_by=instance.created_by,
                    Updated_by=instance.Updated_by
                )
                print(f"Mapping entry created for Finance Ledger: {instance.LedgerName}")
        except Exception as e:
            print(f"Error inserting mapping entry: {e}")


@receiver(post_save, sender=Product_Category_Product_Details)
def insert_financeledger_mapping_tableinsert(sender, instance, created, **kwargs):
    # print('Signal for ledger finance:', instance)
    if created:
        try:
            with transaction.atomic():
                AllLedgers_Mapping_Detailes.objects.create(
                    TableName=Product_Category_Product_Details,
                    TableId=instance.pk,
                    created_by=instance.Created_by,
                    Updated_by=instance.Updated_by
                )
                print(f"Mapping entry created for Finance Ledger: {instance.LedgerName}")
        except Exception as e:
            print(f"Error inserting mapping entry: {e}")
