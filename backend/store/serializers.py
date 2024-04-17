from rest_framework import serializers
from .models import  CustomUser,Otp,Product, CartItem, Category, Review
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser        
        fields = ['username', 'password', 'email', 'is_active', 'is_verified', 'last_name', 'first_name', 'profile_picture']
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)  

class Otpserializer(serializers.ModelSerializer) :    
    class  Meta:
        model = Otp
        fields = '__all__' 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category']      


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"     

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Review
        fields = "__all__"

class Cartserializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_image = serializers.ReadOnlyField(source='product.image.url')  # Assuming 'image' is a FileField in your Product model
    product_description = serializers.ReadOnlyField(source='product.description')
    class Meta:
        model = CartItem
        fields = "__all__"        
    