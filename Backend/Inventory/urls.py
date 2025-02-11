from django.urls import path
from .PurchaseOrder import *
from .ProductMaster import *
from .SupplierMaster import *
from .NewSupplierMaster import *
from .NurseStationStock import *
from .views import *
from .ProductCategory import Product_Category_Product_Details_link
from .GoodsReceiptNote import (Goods_Reciept_Note_Details_link,Goods_Reciept_Note_Details_Approve_link,
                               PO_Goods_Reciept_Note_Details_link,PO_Goods_Reciept_Note_GET_Details_link,
                               Old_Goods_Reciept_Note_stock_supplier_link,get_overall_stock_list_details,
                               get_overall_stock_list_table_column_details,get_overall_stock_list_By_batchwise_details)
from .Indent import (get_ward_store_detials_by_loc,get_item_detials_for_indent,post_indent_raise_details,
                     Indent_Raise_Details_Approve_link,get_item_detials_for_batch_indent_issue,
                     get_serialno_detials_for_batch_indent_issue,post_indent_issue_details,
                     Indent_Issue_Details_Approve_link,Post_Indent_Receive_Details_link,Indent_Receive_Details_Approve_link)

from .SupplierPay import get_supplier_payment_detials,get_supplier_payment_by_invoice_detials,supplier_payment_day_by_date

from .SerialNoForProduct import (GET_SerialNo_Quelist,SerialNumber_Create_Link,
GET_Last_SerialNumber_ItemDetails,GET_SerialNumber_Prodect_From_Master,Get_SerialNumber,Get_BatchNo,
Get_SerialNumber_Report)

from .ItemMinimumMaximum import (Product_Get_For_MinimumMaximum,
Single_Item_All_Location_Minimum_Maximum_Qty,
Post_Change_Minimum_Maximum_Qty)


urlpatterns = [

    path('get_Drug_segments',get_Drug_segments,name='get_Drug_segments'),
    path('get_unit_of_measurements',get_unit_of_measurements,name='get_unit_of_measurements'),
    path('Product_Category_Product_Details_link',Product_Category_Product_Details_link,name='Product_Category_Product_Details_link'),
    path('get_Product_fields_for_productcategory',get_Product_fields_for_productcategory,name='get_Product_fields_for_productcategory'),
    path('product_master_Detials_link',product_master_Detials_link,name='product_master_Detials_link'),
    path('Update_product_master_status',Update_product_master_status,name='Update_product_master_status'),
    path('Supplier_Master_Link',Supplier_Master_Link,name='Supplier_Master_Link'),
    path('Supplier_product_Mapping_link',Supplier_product_Mapping_link,name='Supplier_product_Mapping_link'),
    path('Product_wise_supplier_getdata',Product_wise_supplier_getdata,name='Product_wise_supplier_getdata'),
    path('Supplier_Data_Get',Supplier_Data_Get,name='Supplier_Data_Get'),
    # path('Supplier_Product_Category_link',Supplier_Product_Category_link,name='Supplier_Product_Category_link'),
    path('PurchaseOrder_Link',PurchaseOrder_Link,name='PurchaseOrder_Link'),
    path('PurchaseOrder_Report_Details',PurchaseOrder_Report_Details,name='PurchaseOrder_Report_Details'),
    path('PurchaseOrder_Itemwise_Link',PurchaseOrder_Itemwise_Link,name='PurchaseOrder_Itemwise_Link'),

    path('GET_Product_Detials_For_Tray_link',GET_Product_Detials_For_Tray_link,name='GET_Product_Detials_For_Tray_link'),
        
    path('PO_SupplierWise_product_Get',PO_SupplierWise_product_Get,name='PO_SupplierWise_product_Get'),
    path('PO_Supplier_Data_Get',PO_Supplier_Data_Get,name='PO_Supplier_Data_Get'),
    path('Goods_Reciept_Note_Details_link',Goods_Reciept_Note_Details_link,name='Goods_Reciept_Note_Details_link'),
    path('Goods_Reciept_Note_Details_Approve_link',Goods_Reciept_Note_Details_Approve_link,name='Goods_Reciept_Note_Details_Approve_link'),
    path('Old_Goods_Reciept_Note_stock_supplier_link',Old_Goods_Reciept_Note_stock_supplier_link,name='Old_Goods_Reciept_Note_stock_supplier_link'),
    path('get_overall_stock_list_table_column_details',get_overall_stock_list_table_column_details,name='get_overall_stock_list_table_column_details'),
    path('get_overall_stock_list_By_batchwise_details',get_overall_stock_list_By_batchwise_details,name='get_overall_stock_list_By_batchwise_details'),
    path('get_overall_stock_list_details',get_overall_stock_list_details,name='get_overall_stock_list_details'),
    
    
    # get store and ward store loc
    path('get_ward_store_detials_by_loc',get_ward_store_detials_by_loc,name='get_ward_store_detials_by_loc'),
    path('get_item_detials_for_indent',get_item_detials_for_indent,name='get_item_detials_for_indent'),
    path('get_item_detials_for_batch_indent_issue',get_item_detials_for_batch_indent_issue,name='get_item_detials_for_batch_indent_issue'),
    path('get_serialno_detials_for_batch_indent_issue',get_serialno_detials_for_batch_indent_issue,name='get_serialno_detials_for_batch_indent_issue'),
   
    # indent
    path('post_indent_raise_details',post_indent_raise_details,name='post_indent_raise_details'),
    path('Indent_Raise_Details_Approve_link',Indent_Raise_Details_Approve_link,name='Indent_Raise_Details_Approve_link'),
    path('post_indent_issue_details',post_indent_issue_details,name='post_indent_issue_details'),
    path('Indent_Issue_Details_Approve_link',Indent_Issue_Details_Approve_link,name='Indent_Issue_Details_Approve_link'),
    path('Post_Indent_Receive_Details_link',Post_Indent_Receive_Details_link,name='Post_Indent_Receive_Details_link'),
    path('Indent_Receive_Details_Approve_link',Indent_Receive_Details_Approve_link,name='Indent_Receive_Details_Approve_link'),
    
   path('PO_Goods_Reciept_Note_Details_link',PO_Goods_Reciept_Note_Details_link,name='PO_Goods_Reciept_Note_Details_link'),
    path('PO_Goods_Reciept_Note_GET_Details_link',PO_Goods_Reciept_Note_GET_Details_link,name='PO_Goods_Reciept_Note_GET_Details_link'),

    # supplier pay
    path('get_supplier_payment_detials',get_supplier_payment_detials,name='get_supplier_payment_detials'),
    path('get_supplier_payment_by_invoice_detials',get_supplier_payment_by_invoice_detials,name='get_supplier_payment_by_invoice_detials'),
    path('supplier_payment_day_by_date',supplier_payment_day_by_date,name='supplier_payment_day_by_date'),
    
     path('GET_SerialNo_Quelist',GET_SerialNo_Quelist,name='GET_SerialNo_Quelist'),
    path('SerialNumber_Create_Link',SerialNumber_Create_Link,name='SerialNumber_Create_Link'),
    path('GET_Last_SerialNumber_ItemDetails',GET_Last_SerialNumber_ItemDetails,name='GET_Last_SerialNumber_ItemDetails'),
     path('GET_SerialNumber_Prodect_From_Master',GET_SerialNumber_Prodect_From_Master,name='GET_SerialNumber_Prodect_From_Master'),
    path('Get_SerialNumber',Get_SerialNumber,name='Get_SerialNumber'),
    path('Get_BatchNo',Get_BatchNo,name='Get_BatchNo'),
    path('Get_SerialNumber_Report',Get_SerialNumber_Report,name='Get_SerialNumber_Report'),

    path('Product_Get_For_MinimumMaximum',Product_Get_For_MinimumMaximum,name='Product_Get_For_MinimumMaximum'),
    path('Single_Item_All_Location_Minimum_Maximum_Qty',Single_Item_All_Location_Minimum_Maximum_Qty,name='Single_Item_All_Location_Minimum_Maximum_Qty'),
    path('Post_Change_Minimum_Maximum_Qty',Post_Change_Minimum_Maximum_Qty,name='Post_Change_Minimum_Maximum_Qty'),
    
    path('GRN_Details_GET_For_PurchseReturn',GRN_Details_GET_For_PurchseReturn,name='GRN_Details_GET_For_PurchseReturn'),
    path('PurcchaseReturn_Link',PurcchaseReturn_Link,name='PurcchaseReturn_Link'),
    path('PurchaseReturn_Report_Link',PurchaseReturn_Report_Link,name='PurchaseReturn_Report_Link'),
    path('PurchaseReturn_StatusUpdate',PurchaseReturn_StatusUpdate,name='PurchaseReturn_StatusUpdate'),


    # views
    path('Sub_Product_Category_Details_by_Product', Sub_Product_Category_Details_by_Product, name='Sub_Product_Category_Details_by_Product'),
    path('Items_by_ProductCategory_Details', Items_by_ProductCategory_Details, name='Items_by_ProductCategory_Details'),
    path('Item_wise_supplier_getdata', Item_wise_supplier_getdata, name='Item_wise_supplier_getdata'),
    path('SupplierId_Supplier_Data_Get', SupplierId_Supplier_Data_Get, name='SupplierId_Supplier_Data_Get'),
    path('PO_SupplierWise_Item_Get', PO_SupplierWise_Item_Get, name='PO_SupplierWise_Item_Get'),

    # nursestationlink
    path("get_NurseStation_Details_list", get_NurseStation_Details_list, name='get_NurseStation_Details_list'),
    path('get_Product_Category_byNurseStation', get_Product_Category_byNurseStation, name='get_Product_Category_byNurseStation'),
    path('get_SubProductCategory_byProductCategory', get_SubProductCategory_byProductCategory, name='get_SubProductCategory_byProductCategory'),
    path('get_Item_Details_byNurseStation', get_Item_Details_byNurseStation,name='get_Item_Details_byNurseStation'),
    path('get_NurseStationall_Details_list', get_NurseStationall_Details_list, name='get_NurseStationall_Details_list'),
    
    path('StrengthName_Master_Link', StrengthName_Master_Link, name='StrengthName_Master_Link'),

]


