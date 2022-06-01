from tokenize import group
from rest_framework import serializers
from betogether.models import User, GroupProject,WishList, LearnerProject
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    # learnerProject = serializers.PrimamaryKeyRelatedField(many=False, queryset=LearnerProject.objects.all())
    class Meta:
        model = User
        fields = '__all__'
    
    def save(self):
        user = User(
            email =         self.validated_data["email"],
            username =      self.validated_data["username"],
            first_name =    self.validated_data["first_name"],
            last_name =      self.validated_data["last_name"],
        )

        password =  self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user
    # validate_password = make_password

class GroupProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProject
        fields = '__all__'

class LearnerProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    groupProject = GroupProjectSerializer(many=False, read_only=True)
    class Meta:
        model = LearnerProject
        fields = '__all__'

class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    groupProject = GroupProjectSerializer(many=False, read_only=True)
    class Meta:
        model = WishList
        fields = '__all__'