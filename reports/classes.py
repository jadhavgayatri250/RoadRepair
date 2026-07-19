from datetime import datetime


class Report:

    def __init__(self, name, location, pincode, description):
        self.name = name
        self.location = location
        self.pincode = pincode
        self.description = description
        self.status = "Pending"
        self.report_date = datetime.now()


class Ward:

    ward_pincode = {
        "4232203": "Ward A",
        "4222001": "Ward B",
        "423301": "Ward C",
        "423108": "Ward D"
    }

    @classmethod
    def get_ward(cls, pincode):
        return cls.ward_pincode.get(pincode, "Unknown Ward")


class StatusTracker:

    def __init__(self):
        self.status = "Pending"

    def update_status(self, new_status):
        self.status = new_status