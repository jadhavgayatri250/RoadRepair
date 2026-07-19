from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from bson.objectid import ObjectId
from datetime import datetime

from .serializers import ReportSerializer
from .forms import ReportForm
from .mongo import reports_collection
from .classes import Report, Ward
from .thread import start_notification


def home(request):
    return render(request, "home.html")


def report(request):

    form = ReportForm()

    if request.method == "POST":

        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():

            try:

                name = form.cleaned_data["name"].strip()
                location = form.cleaned_data["location"].strip()
                pincode = form.cleaned_data["pincode"].strip()
                description = form.cleaned_data["description"].strip()
                photo = form.cleaned_data["photo"]

                duplicate = reports_collection.find_one({
                    "location": location,
                    "pincode": pincode,
                    "status": "Pending"
                })

                if duplicate:
                    messages.warning(
                        request,
                        "Duplicate complaint already exists."
                    )
                    return redirect("report")

                photo_name = ""

                if photo:
                    fs = FileSystemStorage()
                    photo_name = fs.save(photo.name, photo)

                report_obj = Report(
                    name=name,
                    location=location,
                    pincode=pincode,
                    description=description
                )

                ward = Ward.get_ward(pincode)

                reports_collection.insert_one({

                    "name": report_obj.name,
                    "location": report_obj.location,
                    "pincode": report_obj.pincode,
                    "description": report_obj.description,
                    "photo": photo_name,
                    "ward": ward,
                    "status": "Pending",
                    "report_date": datetime.now()

                })

                start_notification(name)

                messages.success(
                    request,
                    "Complaint submitted successfully."
                )

                return redirect("dashboard")

            except Exception as e:

                messages.error(
                    request,
                    str(e)
                )

    return render(
        request,
        "report.html",
        {
            "form": form
        }
    )
   

def dashboard(request):

    reports = list(
        reports_collection.find().sort("report_date", -1)
    )

    total_reports = len(reports)
    pending_reports = 0
    completed_reports = 0

    # Convert MongoDB ObjectId to String
    for report in reports:

        report["id"] = str(report["_id"])

        if report.get("status") == "Completed":
            completed_reports += 1
        else:
            pending_reports += 1

    aggregate_result = reports_collection.aggregate([
        {
            "$group": {
                "_id": "$ward",
                "count": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ])

    ward_counts = {}

    for item in aggregate_result:

        ward = item["_id"]

        if ward is None:
            ward = "Unknown Ward"

        ward_counts[ward] = item["count"]

    return render(
        request,
        "dashboard.html",
        {
            "reports": reports,
            "total_reports": total_reports,
            "pending_reports": pending_reports,
            "completed_reports": completed_reports,
            "ward_counts": ward_counts,
        }
    )


def update_status(request, report_id):

    try:

        reports_collection.update_one(
            {
                "_id": ObjectId(report_id)
            },
            {
                "$set": {
                    "status": "Completed"
                }
            }
        )

        messages.success(
            request,
            "Complaint marked as Completed."
        )

    except Exception as e:

        messages.error(
            request,
            str(e)
        )

    return redirect("dashboard")

def delete_report(request, report_id):

    try:

        reports_collection.delete_one(
            {
                "_id": ObjectId(report_id)
            }
        )

        messages.success(
            request,
            "Complaint deleted successfully."
        )

    except Exception as e:

        messages.error(
            request,
            str(e)
        )

    return redirect("dashboard")

@api_view(["GET"])
def report_api(request):

    reports = []

    for report in reports_collection.find():

        report["id"] = str(report["_id"])
        del report["_id"]

        reports.append(report)

    serializer = ReportSerializer(reports, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def report_detail(request, report_id):

    try:

        report = reports_collection.find_one(
            {
                "_id": ObjectId(report_id)
            }
        )

        if report:

            report["id"] = str(report["_id"])
            del report["_id"]

            serializer = ReportSerializer(report)

            return Response(serializer.data)

        return Response(
            {
                "error": "Report Not Found"
            },
            status=404
        )

    except Exception as e:

        return Response(
            {
                "error": str(e)
            },
            status=400
        )

@api_view(["POST"])
def add_report_api(request):

    serializer = ReportSerializer(data=request.data)

    if serializer.is_valid():

        data = serializer.validated_data

        # Duplicate Complaint Check
        duplicate = reports_collection.find_one({
            "location": data["location"],
            "pincode": data["pincode"],
            "status": "Pending"
        })

        if duplicate:

            return Response(
                {
                    "message": "Duplicate complaint already exists."
                },
                status=409
            )

        data["ward"] = Ward.get_ward(data["pincode"])

        data["status"] = "Pending"

        data["report_date"] = datetime.now()

        reports_collection.insert_one(data)

        return Response(
            {
                "message": "Report Added Successfully"
            },
            status=201
        )

    return Response(serializer.errors, status=400)