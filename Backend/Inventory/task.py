from Inventory.models import Stock_Maintance_Table_Detials
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
import datetime

def check_and_update_expiry_status():
    stock_items = Stock_Maintance_Table_Detials.objects.all()
    for stock_item in stock_items:
        old_status = stock_item.Expiry_Status
        stock_item.check_and_update_expiry_status()
        new_status = stock_item.Expiry_Status
        # print(
        #     f"ItemCode: {stock_item.Product_Detials.pk}, BatchNo: {stock_item.Batch_No}, IsNurseStation: {stock_item.IsNurseStation} at {stock_item.NurseStation_location.NurseStationName if stock_item.IsNurseStation else stock_item.Store_location.str() }\n"
        #     f"Old Status: {old_status}, "
        #     f"New Status: {new_status}"
        # )
        
        
def check_and_update_expiry_status_stsrt_fun():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_and_update_expiry_status,
        'interval',
        days=1,  # Set to run every day
        start_date=timezone.now() + datetime.timedelta(seconds=10)  # Start after 10 seconds
    )
    try:
        scheduler.start()
        print("Scheduler started successfully , Inventory ")
    except Exception as e:
        print(f"Failed to start scheduler: {e}")


