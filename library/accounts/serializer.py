
from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id", "username","user_type"]


#Serializer to Register User
class LibRegisterSerializer(serializers.ModelSerializer):
  username = serializers.CharField(
    required=True,
    validators=[UniqueValidator(queryset=CustomUser.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = CustomUser
    fields = ('username', 'password', 'password2')
    
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = CustomUser.objects.create(
      username=validated_data['username'],
      user_type = 1
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class MemRegisterSerializer(serializers.ModelSerializer):
  username = serializers.CharField(
    required=True,
    validators=[UniqueValidator(queryset=CustomUser.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = CustomUser
    fields = ('username', 'password', 'password2')
    
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = CustomUser.objects.create(
      username=validated_data['username'],
      user_type = 2
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class MemViewSerializer(serializers.ModelSerializer):
  class Meta:
        model = CustomUser
        fields = '__all__'



