from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .serializers import *

class ProductListAPI(APIView):
    def get(self , resquest):
        product = Product.objects.all()
        serializers = ProductSerializer(product, many=True)
        return Response(serializers.data, status = status.HTTP_200_OK)
        # return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializers = ProductSerializer(data=request.data)
        
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPI(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializers = ProductSerializer(product)
        return Response(serializers.data, status= status.HTTP_302_FOUND)
    
    def put(self, request, pk):
        product = Product.objects.get(id=pk)
        
        serializers = ProductSerializer(product, data=request.data)
        
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self, request,pk):
        product = Product.objects.get(id = pk)
        product.delete()
        return Response({"message": "Deleted"})