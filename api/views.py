from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status,viewsets,permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCustomer
from accounts.permissions import IsProvider

from .serializers import *
from core.models import *
from cart.models import *
from orders.models import *

# class ProductListAPI(APIView):
#     def get(self , resquest):
#         product = Product.objects.all()
#         serializers = ProductSerializer(product, many=True)
#         return Response(serializers.data, status = status.HTTP_200_OK)
#         # return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)
    
#     def post(self, request):
#         serializers = ProductSerializer(data=request.data)
        
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_200_OK)
        
#         return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

# class ProductDetailAPI(APIView):
#     def get(self, request, pk):
#         product = Product.objects.get(id=pk)
#         serializers = ProductSerializer(product)
#         return Response(serializers.data, status= status.HTTP_302_FOUND)
    
#     def put(self, request, pk):
#         product = Product.objects.get(id=pk)
        
#         serializers = ProductSerializer(product, data=request.data)
        
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

        
#     def delete(self, request,pk):
#         product = Product.objects.get(id = pk)
#         product.delete()
#         return Response({"message": "Deleted"})

class NavbarCategoryViewSet(viewsets.ModelViewSet):
    queryset = NavbarCategory.objects.all()
    serializer_class = NavbarCategorySerializer
    
class BusinessHourViewSet(viewsets.ModelViewSet):
    queryset = BusinessHour.objects.all()
    serializer_class = BusinessHourSerializer
    
class SocialMediaViewSet(viewsets.ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CategoryWithProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductsSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsProvider()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        product = serializer.validated_data['product']

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += serializer.validated_data['quantity']
            cart_item.save()
        else:
            serializer.save(cart=cart)
            
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total = 0
        order = Order.objects.create(
            user=request.user,
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            email=request.data.get('email'),
            address=request.data.get('address'),
            address2=request.data.get('address2'),
            country=request.data.get('country'),
            state=request.data.get('state'),
            zip_code=request.data.get('zip_code'),
            payment_method=request.data.get('payment_method'),
            total_price=0
        )

        for item in cart.items.all():
            price = item.product.price
            total += price * item.quantity

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=price
            )

        order.total_price = total
        order.save()

        cart.items.all().delete()  # 🔥 clear cart

        return Response({"message": "Order placed successfully"})
    
