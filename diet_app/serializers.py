

from rest_framework import serializers

from diet_app.models import User,UserProfile,FoodLog


# FoodLog

class UserSerializer(serializers.ModelSerializer):

    profile=serializers.SerializerMethodField(read_only=True)


    class Meta:

        model = User

        fields=["id","username","email","phone","password","profile"]

        # read_only_fields=["id","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def get_profile(self,object):

        profile_instance = UserProfile.objects.get(owner=object)

        serializer_instance = UserProfileSerializer(profile_instance)

        return serializer_instance.data


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserProfile

        fields  = "__all__"

        read_only_fields=["id","owner","bmr"]



class FoodLogSerializer(serializers.ModelSerializer):


    class Meta:

        model = FoodLog

        fields="__all__"

        read_only_fields = ["id","owner","created_at"]

