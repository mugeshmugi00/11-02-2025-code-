from django.urls import path
from .AssetCategories import *
from .AssetSubCategorieManagement import *
from .Suppliers import *
from .ServiceProviderMangement import *
from .ChecklistManagement import *
from .ChecklistMasterEntry import *
from .AssetManagement import *
 
urlpatterns = [
    path('asset_categories/', asset_categories, name='asset_categories'),  # Added trailing slash
    path('update_asset_category/<int:category_id>/', update_asset_category, name='update_asset_category'),
    path('get_asset_category/<int:category_id>/', get_asset_category, name='get_asset_category'),
    path('asset_categories_list/', asset_categories_list, name='asset_categories_list'),  # Added trailing slash
   
    # -----------------------------sub Categories-------------------------------
    path('asset_subcategories/',asset_subcategories,name='asset_subcategories'),
    path('get_asset_subcategories/',get_asset_subcategories,name='get_asset_subcategories'),
    path('update_asset_subcategory/<int:subcategory_id>/',update_asset_subcategory,name='update_asset_subcategory'),
 
    # -----------------------------suppliers Data-------------------------------
    path('suppliers_Data/',suppliers_Data,name='suppliers_Data'),
    path('suppliers_Data_Get/',suppliers_Data_Get,name='suppliers_Data_Get'),
    path('suppliers_Data_Put/<int:supplier_id>/',suppliers_Data_Put,name='suppliers_Data_Put'),
    
    # --------------------------ServiceProviderManagement_POST--------------------------------
    path('ServiceProviderManagement_POST/',ServiceProviderManagement_POST,name='ServiceProviderManagement_POST'),
    path('ServiceProviderManagement_GET/',ServiceProviderManagement_GET,name='ServiceProviderManagement_GET'),
    path('ServiceProviderManagement_PUT/<int:ServiceProviderManagement_id>/',ServiceProviderManagement_PUT,name='ServiceProviderManagement_PUT'),
    
    # --------------------------------------ChecklistManagement-------------------------------------
    path('ChecklistManagement_post/',ChecklistManagement_post,name='ChecklistManagement_post'),
    path('ChecklistManagement_get/',ChecklistManagement_get,name='ChecklistManagement_get'),
    path('ChecklistManagement_Put/',ChecklistManagement_Put,name='ChecklistManagement_Put'),
    
    # ---------------------------------ChecklistMasterEntry--------------------------------------
    path('ChecklistMasterEntry_post/',ChecklistMasterEntry_post,name='ChecklistMasterEntry_post'),
    path('ChecklistMasterEntry_get/',ChecklistMasterEntry_get,name='ChecklistMasterEntry_get'),
    path('ChecklistMasterEntry_Put/<int:entry_id>/',ChecklistMasterEntry_Put,name='ChecklistMasterEntry_Put'),
    # ------------------------------------AssetReg------------------------------------------------
    path('Asset_Reg_post/',Asset_Reg_post,name='Asset_Reg_post'),
    path('Asset_Reg_Get/',Asset_Reg_Get,name='Asset_Reg_Get'),
    path('Asset_Reg_put/<int:asset_id>/', Asset_Reg_put, name='Asset_Reg_put'),
    
    # ---------------------------------------------assetList---------------------------------------------------
    path('assetList_Get/',assetList_Get,name='assetList_Get'),
    # path('assetList_POST/',assetList_POST,name='assetList_POST'),
    path('assetList_PUT/',assetList_PUT,name='assetList_PUT'),
    
]