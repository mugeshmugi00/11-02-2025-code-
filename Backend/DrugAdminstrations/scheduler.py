from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from Masters.models import *
from Inventory.models import *
from django.db.models import Q
from django.core.files.base import ContentFile
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, time
import pytz
from django.db import transaction


import json
from collections import defaultdict





def job_function():
    try:
        print('job function insert')
        # Fetch drug administration details
        administrations = Doctor_drug_prescription.objects.all()
        print('Query result:', administrations)
    
        for administration in administrations:
            if administration.FrequencyMethod == 'Regular':
                try:
                    # Ensure FrequencyTime attribute is present and correct
                    frequency_times = administration.Frequency.FrequencyTime.split(',')
                    print('frequency_times', frequency_times)
                except AttributeError:
                    print(f"Error: Frequency object does not have 'FrequencyTime' attribute. Found attributes: {dir(administration.Frequency)}")
                    continue  # Skip this record if FrequencyTime is missing or incorrect

                tablet_duration_days = int(administration.Duration)
                tablet_frequency_time = [(int(hour), 0) for hour in frequency_times]
                
                # Convert `start_date` to a datetime.date object
                start_date = administration.created_at.date()  # Ensure it's a date object
                start_time = administration.created_at.time()

                print('Start date and time:', start_date, start_time)
                for day_offset in range(tablet_duration_days):
                    print('dayyyyyssss',day_offset)
                    current_date = start_date + timedelta(days=day_offset)
                    tablet_times = []

                    for freq_time in tablet_frequency_time:
                        tablet_datetime = datetime.combine(current_date, time(freq_time[0], freq_time[1]))
                        print('tabbbbbb',tablet_datetime)
                        if tablet_datetime.time() < start_time:
                            tablet_datetime += timedelta(days=1)
                            print('bbbbbbbb',tablet_datetime)
                        tablet_times.append(tablet_datetime)
                        print(f"current_date: {current_date}, freq_time: {freq_time}, tablet_datetime: {tablet_datetime}, start_time: {start_time}")

                    print('tablet_times',tablet_times)

                    if tablet_times:
                        tablet_times.sort()
                        today_date = timezone.now().date()
                        
                        print('3333333333')

                        # Update pending requests
                        Ip_Nurse_Drug_Completed_Administration.objects.filter(
                            Status='Pending', Issued_Date__lt=today_date
                        ).update(Status='NotIssued')
                        for tablet_time in tablet_times:
                            print('aaaaaaaaa', today_date, tablet_time.date())
                            if today_date == tablet_time.date():
                                print('44444444',today_date, tablet_time.date())
                                print('5555555555')
                                tablet_issue = int(tablet_time.strftime("%H"))
                                tablet_date_issue = tablet_time.date()
                                print('Tablet issue date:', tablet_date_issue)

                                # Check pending status and handle accordingly
                                if administration.Status == 'Pending':
                                    if administration.OrderType == 'OutSource':
                                        print('gottttinnntoooOutsource')
                                        handle_outsourced_request(administration, tablet_issue, tablet_date_issue)
                                    elif administration.OrderType == 'IP_Pharmacy':
                                        print('gottttinnntoooIP_Pharmacy')
                                        handle_inhouse_request(administration, tablet_issue, tablet_date_issue)

    except Exception as e:
        print(f"Error in job_function: {e}")
        # Use Django's logging for better error tracking

# Define handle_outsourced_request and handle_inhouse_request functions here
# They should use Django ORM to update relevant models as needed


@transaction.atomic
def handle_outsourced_request(row, tablet_issue, tablet_date_issue):
    """Handles outsourced drug requests using Django ORM."""

    exists = Ip_Nurse_Drug_Completed_Administration.objects.filter(
        prescription_id=row.Prescription_Id, booking_id=row.Booking_Id,
        frequency_issued=tablet_issue, issued_date=tablet_date_issue
    ).exists()

    if not exists:
        Ip_Nurse_Drug_Completed_Administration.objects.create(
            Prescription_Id=row.prescription_id,
            Booking_Id=row.booking_id,
            Department=row.department,
            DoctorName=row.doctor_name,
            ProductCode=row.generic_name,
            Dosage=row.dosage,
            Route=row.route,
            FrequencyIssued=tablet_issue,
            FrequencyMethod=row.frequency_method,
            Quantity=1,  # Adjust as per actual requirement
            Issued_Date=tablet_date_issue,
            Complete_Date=None,
            Complete_Time=None,
            Completed_Remarks='',
            Status='Pending',
            Location=row.location,
            CapturedBy='',  # Define as needed
            AdminisDose=row.adminis_dose
        )


@transaction.atomic
def handle_inhouse_request(row, tablet_issue, tablet_date_issue):
    print('Gottttttiiinnnnnnhandle_inhouse_request')
    """Handles in-house drug requests using Django ORM."""

    # Handling 'Daily' frequency
    if row.RequestType == 'Daily':
        print('Daillyyyyyyyy')
        # Check if the request already exists for the given prescription and booking on this date
        existing_request = ip_drug_request_table.objects.filter(
            Prescription_Id=row.Prescription_Id,
            Booking_Id=row.Booking_Id,
            Date=tablet_date_issue
        ).first()

        if existing_request is None:
            prescription_ins = Doctor_drug_prescription.objects.get(Prescription_Id = row.Prescription_Id)
            remaining = int(row.Quantity) - int(row.RequestQuantity)
            ip_drug_request_table.objects.create(
                Booking_Id=row.Booking_Id,
                Prescription_Id=prescription_ins,
                Department=row.Department,
                DoctorName=row.DoctorName,
                ProductCode = row.ProductCode,
                Route=row.Route,
                Frequency = row.Frequency,
                FrequencyMethod = row.FrequencyMethod,
                OrderType=row.OrderType,
                Quantity=row.Quantity,
                RequestType = row.RequestType,
                RequestQuantity=row.RequestQuantity,
                RemainingQuantity=remaining,
                Instruction = row.Instruction,
                Location=row.Location,
                IssuedBy=row.IssuedBy,  # Adjust as per requirement
                CapturedBy=row.CapturedBy,  # Adjust as per requirement
                Status='Pending',
                Duration=row.Duration,
                DurationType=row.DurationType,
                Date=tablet_date_issue
            )
        elif existing_request.Status == "Received":
            # Ensure drug request entry for 'Daily' frequency
            existing_administration = Ip_Nurse_Drug_Completed_Administration.objects.filter(
                Prescription_Id=row.Prescription_Id,
                Booking_Id=row.Booking_Id,
                FrequencyIssued=tablet_issue,
                Issued_Date=tablet_date_issue
            ).first()

            if existing_administration is None:
                next_id1 = Ip_Nurse_Drug_Completed_Administration.objects.aggregate(
                    max_id=models.Max('Nurse_Prescription_Id')
                )['max_id']
                next_id1 = next_id1 + 1 if next_id1 is not None else 1

                Ip_Nurse_Drug_Completed_Administration.objects.create(
                    Nurse_Prescription_Id=next_id1,
                    Prescription_Id=row.Prescription_Id,
                    Booking_Id=row.Booking_Id,
                    Department=row.Department,
                    DoctorName=row.DoctorName,
                    GenericName=row.GenericName,
                    MedicineCode=row.MedicineCode,
                    MedicineName=row.MedicineName,
                    Dosage=row.Dosage,
                    Route=row.Route,
                    FrequencyIssued=tablet_issue,
                    FrequencyMethod=row.FrequencyMethod,
                    Quantity=1,  # Adjust this as needed
                    Issued_Date=tablet_date_issue,
                    Status='Pending',
                    Location=row.Location,
                    CapturedBy='',  # Define appropriately
                    AdminisDose=row.AdminisDose
                )

    # Handling 'Total' frequency
    elif row.RequestType == 'Total':
        print('77777777777')
        print('88888888')
        existing_request_total = ip_drug_request_table.objects.filter(
            Prescription_Id = row.Prescription_Id,
            Booking_Id=row.Booking_Id
        ).first()
        if existing_request_total is None:
            print('99999')
            prescription_ins = Doctor_drug_prescription.objects.get(Prescription_Id = row.Prescription_Id)
            remaining = int(row.Quantity) - int(row.RequestQuantity)
            ip_drug_request_table.objects.create(
                Booking_Id=row.Booking_Id,
                Prescription_Id=prescription_ins,
                Department=row.Department,
                DoctorName=row.DoctorName,
                ProductCode = row.ProductCode,
                Route=row.Route,
                Frequency = row.Frequency,
                FrequencyMethod = row.FrequencyMethod,
                OrderType=row.OrderType,
                Quantity=row.Quantity,
                RequestType = row.RequestType,
                RequestQuantity=row.RequestQuantity,
                RemainingQuantity=remaining,
                Instruction = row.Instruction,
                Location=row.Location,
                IssuedBy=row.IssuedBy,  # Adjust as per requirement
                CapturedBy=row.CapturedBy,  # Adjust as per requirement
                Status='Pending',
                Duration=row.Duration,
                DurationType=row.DurationType,
                Date=tablet_date_issue
            )
        elif existing_request_total.Status == "Recieved":
            print('CheckkkkkkkkTooootaalll')
            existing_administration_total = Ip_Nurse_Drug_Completed_Administration.objects.filter(
                Prescription_Id=row.Prescription_Id,
                Booking_Id=row.Booking_Id,
                FrequencyIssued=tablet_issue,
                Issued_Date=tablet_date_issue
            ).first()

            if existing_administration_total is None:
                prescription_ins = Doctor_drug_prescription.objects.get(Prescription_Id = row.Prescription_Id)
                Ip_Nurse_Drug_Completed_Administration.objects.create(
                    Prescription_Id=prescription_ins,
                    Booking_Id=row.Booking_Id,
                    Department=row.Department,
                    DoctorName=row.DoctorName,
                    ProductCode = row.ProductCode,
                    Route=row.Route,
                    FrequencyIssued=tablet_issue,
                    FrequencyMethod=row.FrequencyMethod,
                    Quantity=1,  # Adjust as necessary
                    Issued_Date=tablet_date_issue,
                    Status='Pending',
                    Location=row.Location,
                    CapturedBy=row.CapturedBy,  # Adjust as needed
                    AdminisDose=row.AdminisDose
                )
                print('Ip_Nurse_Drug_Completed_Administration created succesfuly')


def start_scheduler():
    sched = BackgroundScheduler()
    next_run_time = timezone.now() + timedelta(days=1)  # Adjust as needed for testing
    sched.add_job(job_function, "date", run_date=next_run_time)
    sched.start()
    print('Scheduler started successfully,DrugAdministration.')