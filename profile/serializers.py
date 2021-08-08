from rest_framework import serializers
# from users.models import User
from users.serializers import UserSerializer
from profile.models import Achievement
from profile.models import Developer

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = (
            "id",
            "user_id",
            "title",
            "origin",
            "description",
            "start_date",
            "finish_date",
            "feats_type",
            "is_verified",
            "verification",
        )


class DeveloperSerializer(serializers.ModelSerializer):

    #Campo que hace referencia a lo que devuelve el str del modelo
    email = UserSerializer(many=False, read_only=True)
    achievements = AchievementsSerializer(many=True, read_only=True)

    class Meta:
        model = Developer
        fields = (
            "id",
            "email",
            "profile_image",
            "first_name",
            "last_name",
            "birth_date",
            "location",
            "bio",
            "education",
            "dev_area",
            "main_language",
            "experience",
            "website",
            "updated_at",
            "achievements",
        )


class DeveloperAchievementsSerializer(serializers.ModelSerializer):

    achievements = AchievementsSerializer(many=True, read_only=True)

    class Meta:
        model = Developer
        fields = (
            "id",
            "email",
            "profile_image",
            "first_name",
            "last_name",
            "birth_date",
            "location",
            "bio",
            "education",
            "dev_area",
            "main_language",
            "experience",
            "website",
            "updated_at",
            "achievements",
        )
