from rest_framework import serializers

class ReportSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    location = serializers.CharField()
    pincode = serializers.CharField()
    description = serializers.CharField()
    ward = serializers.CharField()
    status = serializers.CharField()
    photo = serializers.CharField(required=False)
    report_date = serializers.DateTimeField(required=False)