from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("report/", views.report, name="report"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("update/<str:report_id>/",
         views.update_status,
         name="update_status"),

    path("delete/<str:report_id>/",
         views.delete_report,
         name="delete_report"),

    path("api/reports/",
         views.report_api,
         name="report_api"),

    path("api/report/<str:report_id>/",
         views.report_detail,
         name="report_detail"),

    path("api/add-report/",
         views.add_report_api,
         name="add_report_api"),
]