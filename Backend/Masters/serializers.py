from rest_framework import serializers
from .models import *


class MainDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab_Department_Detials
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SubLabDepartmentSerializer(serializers.ModelSerializer):
    # Use a primary key related field to handle the foreign key
    department = serializers.PrimaryKeyRelatedField(
        queryset=Lab_Department_Detials.objects.all()
    )

    MainDepartment_Name = serializers.SerializerMethodField()

    class Meta:
        model = SubLab_Department_Detials
        fields = "__all__"

    def get_MainDepartment_Name(self, obj):
        # Retrieve the main department name from the related department
        if obj.department:
            return obj.department.Department_Name
        return None

    def create(self, validated_data):
        return SubLab_Department_Detials.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ContainerMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container_Masters
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SpecimenMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specimen_Masters
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UnitMasterSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Unit_Masters
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MethodMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Methods_Masters
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AntibioticMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntibioticMaster
        fields = "__all__"

    def create(self, insert_data):
        return super().create(insert_data)

    def update(self, instance, inserted_data):
        for key, value in inserted_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class OrganismMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism_Masters
        fields = "__all__"

    def create(self, insert_data):
        return super().create(insert_data)

    def update(self, instance, inserted_data):
        for key, value in inserted_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RemarksMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks_master
        fields = "__all__"

    def create(self, insert_data):
        return super().create(insert_data)

    def update(self, instance, inserted_data):
        for key, value in inserted_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class NurseStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseStationMaster
        fields = "__all__"
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request", None)
        print("request :", request.method)
        if request and request.method == "GET":
            # Only add the source fields for GET request
            self.fields["Display_Location_Name"] = serializers.CharField(
                source="Location_Name.Location_Name", read_only=True
            )
            self.fields["Display_Building_Name"] = serializers.CharField(
                source="Building_Name.Building_Name", read_only=True
            )
            self.fields["Display_Block_Name"] = serializers.CharField(
                source="Block_Name.Block_Name", read_only=True
            )
            self.fields["Display_Floor_Name"] = serializers.CharField(
                source="Floor_Name.Floor_Name", read_only=True
            )
 
    def get_Status_Name(self, obj):
        return "Active" if obj.Status else "InActive"
 
    def create(self, insert_data):
        # Create method remains unchanged
        return super().create(insert_data)
 
 
class NurseStationDetailsSerializer(serializers.ModelSerializer):
 
    Ward_Name = serializers.CharField(source="Wardid.Ward_Name", read_only=True)
 
    class Meta:
        model = NurseStationMasterDetails
        fields = "__all__"
 
    def create(self, insert_data):
        return super().create(insert_data)


class ServiceCategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Category_Masters
        fields = '__all__'
 
    def create(self, validated_data):
        return super().create(validated_data)
   
    def update(self,instance,inserted_data):
        for key,value in inserted_data.items():
            setattr(instance,key,value)
        instance.save()
        return instance
 