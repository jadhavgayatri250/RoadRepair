# RoadRepair
RoadRepair is a Citizen Pothole Reporting and Municipal Tracking Portal developed using Python, Django, MongoDB and Django REST Framework.

## Features
- User Registration and Login
- Secure Login Authentication
- Report Potholes
- Upload Road Damage Images
- View Submitted Reports
- Duplicate Complaint Detection
- Ward Mapping using Pincode
- Complaint Status Tracking
- Admin Dashboard
- Update Complaint Status
- Delete Reports
- REST API for Reports

## Technologies Used
- Python
- Django
- Django REST Framework
- MongoDB
- HTML
- CSS
- Bootstrap

## Project Description
RoadRepair helps citizens report potholes by submitting the location, pincode, description and road image. 
The system validates the pincode, detects duplicate complaints, assigns the appropriate ward, stores reports in MongoDB and 
allows municipal authorities to update the complaint status through an admin dashboard.

## How to Run
### Step 1: Clone the Repository
bash
git clone https://github.com/jadhavgayatri250/RoadRepair.git

### Step 2: Open the Project Folder
bash
cd RoadRepair
### Step 3: Install Required Packages
bash
pip install django djangorestframework pymongo pillow
### Step 4: Start MongoDB
Make sure MongoDB Server is running before starting the project.
### Step 5: Run Database Migration
bash
python manage.py migrate
### Step 6: Start the Django Server
bash
python manage.py runserver
### Step 7: Open the Project
Open your browser and visit:
http://127.0.0.1:8000/
## Output
- Home Page
- User Registration
- User Login
- Report Pothole Page
- Upload Image
- Dashboard
- Complaint Status Tracking
- Admin Dashboard
- REST API
