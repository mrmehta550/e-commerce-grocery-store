from rest_framework import serializers
from products.models import *
from accounts.models import *
from cart.models import *
from core.models import *
from orders.models import *

class NavbarCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_image = serializers.SerializerMethodField()
    
    class Meta:
        model = NavbarCategory
        fields = ['id', 'category', 'category_name', 'category_image', 'position']
    
    def get_category_image(self, obj):
        if obj.category.image:
            return obj.category.image.url
        return None

    def validate(self, data):
        if NavbarCategory.objects.count() >= 5 and not self.instance:
            raise serializers.ValidationError("Maximum 5 categories allowed")
        return data
    
class BusinessHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHour
        fields = '__all__'
        
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

    def validate(self, data):
        if SocialMedia.objects.count() >= 5 and not self.instance:
            raise serializers.ValidationError("Maximum 5 social links allowed")
        return data
    
class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategoryMiniSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',

            'category',
            'category_id',

            'tag',
            'is_sale',
            'is_new'
        ]

class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_id',
            'quantity',
            'price',
            'total_price'
        ]

    def get_total_price(self, obj):
        return obj.total_price()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'id', 'user',

            # Billing
            'first_name', 'last_name', 'email',
            'address', 'address2',
            'country', 'state', 'zip_code',

            # Payment
            'payment_method',

            # Pricing
            'total_price',

            # Status
            'status',
            'created_at',

            # Items
            'items'
        ]
        read_only_fields = ['status', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']
        
class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']
        
class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products = ProductMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products']