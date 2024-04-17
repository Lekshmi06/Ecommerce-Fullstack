from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import CustomUser,Otp, Product, Category, CartItem,Review
from .serializers import  UserSerializer, UserLoginSerializer,Otpserializer,ProductSerializer, CategorySerializer, ReviewSerializer, Cartserializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib import messages
from rest_framework.views import APIView
from django.db.models import Q
from .utils import generate_and_save_otp, send_otp_email
# Create your views here.

class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'error': 'Username or Emial already exists'}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()

            otp_instance = generate_and_save_otp(user)
            send_otp_email(user.email, otp_instance)

            return Response({'message':'Otp sent to your email, Please verify.', 'user_id':user.id})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyOtp(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = Otpserializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp_value = serializer.validated_data['otp']

            try:
                otp_instance = Otp.objects.get(user=user)

                if otp_value == otp_instance.otp:
                    user.is_active = True
                    user.is_verified = True
                    user.save(update_fields=['is_active', 'is_verified'])
                    otp_instance.delete()

                    token = RefreshToken.for_user(user)
                    token.payload = {"id": user.id,
                                     "username": user.username, 
                                     "active": user.is_active, 
                                     "verified": user.is_verified}

                    
                    return Response({'token':str(token), 'message':'User is verified and activated.'}, status=status.HTTP_200_OK)
                else:
                      return Response({'message':'Invalid OTP.'},status=status.HTTP_400_BAD_REQUEST)
            except Otp.DoesNotExist:
                return Response({'message':'Otp not found for the user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    permission_class = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = RefreshToken.for_user(user)
                token.payload = {"id": user.id,
                                 "username": user.username, 
                                 "active": user.is_active, 
                                 "verified": user.is_verified,
                                 "is_superuser": user.is_superuser}
                
                return Response({'token': str(token), 'message': 'Login sucessfull.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message':"invalid credential"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #listing product based on category
class Category_wise(APIView):
    def get(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'category_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(category__id = category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class product_view(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
         products = Product.objects.all()
         serializer = ProductSerializer(products, many=True)
         return Response(serializer.data)
    def post(self, request):
         serializer = ProductSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EditProduct(APIView):
    permission_classes = [AllowAny]
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class single_product(APIView):
    permission_classes = [AllowAny]    
    def get(self, request, product_id):
        try:
         
          book = get_object_or_404(Product, pk=product_id)
          serializer = ProductSerializer(book)
          return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesnotExist:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class category_thing(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    def post(self, request): 
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)   
    
class DeleteCategory(APIView):
    def post(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            category.delete()
            return Response("Successfully deleted", status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response("Category not found", status=status.HTTP_404_NOT_FOUND)
        
class DeleteProduct(APIView):
    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return Response("Successfully deleted", status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)




class EditCategory(APIView):
    def post(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)

            # Use a serializer for validation and data handling
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Successfully updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        
class set_review(APIView):
    def get(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'product_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        reviews = Review.objects.filter(product__id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request): 
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 


class DeleteReview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id, user=request.user)
            review.delete()
            return Response({'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found or you do not have permission to delete it'}, status=status.HTTP_404_NOT_FOUND)              
    

class cart(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        reviews = CartItem.objects.filter(user__id=user_id)
        serializer = Cartserializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request): 
        serializer = Cartserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)   

