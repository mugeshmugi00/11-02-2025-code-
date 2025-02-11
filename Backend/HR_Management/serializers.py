from rest_framework import serializers
from .models import DutyRousterMaster
from datetime import datetime
from .models import *


class DutyRousterMasterDetailsSerializer(serializers.ModelSerializer):
    Status = serializers.BooleanField(required=False)
    display_starttime = serializers.SerializerMethodField()
    display_endtime = serializers.SerializerMethodField()

    class Meta:
        model = DutyRousterMaster
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            self.fields["Display_Location"] = serializers.CharField(
                source="Location.Location_Name", read_only=True
            )
            self.fields["DepartmentName"] = serializers.CharField(
                source="Department.Department_Name", read_only=True
            )

    def get_display_starttime(self, obj):
        return self.convert_to_12hr_format(obj.StartTime)

    def get_display_endtime(self, obj):
        return self.convert_to_12hr_format(obj.EndTime)

    @staticmethod
    def convert_to_12hr_format(time_obj):
        return time_obj.strftime("%I:%M %p") if time_obj else None

    def get_Status_Name(self, obj):
        return "Active" if obj.Status else "Inactive"

    def update(self, instance, validated_data):
        statusedit = self.initial_data.get("Statusedit", None)
        if statusedit is not None:
            Status = validated_data.get("Status")
            Status1 = False if Status is True else True
            validated_data["Status"] = Status1
            instance.Status = Status1
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Add the Statusedit field with a value of True to the serialized output.
        """
        representation = super().to_representation(instance)
        representation["is_edit"] = True
        return representation


from rest_framework import serializers
from .models import ShiftDetails_Master


class ShiftDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftDetails_Master
        fields = "__all__"
    def create(self, validated_data):
        return super().create(validated_data)