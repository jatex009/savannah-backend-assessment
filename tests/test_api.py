from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Category, Product
from customers.models import Customer
from orders.models import Order

# Override REST_FRAMEWORK settings for tests
@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    }
)
class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.99,
            category=self.category,
            stock_quantity=100
        )
        # Create and authenticate a user for API tests
        self.user = Customer.objects.create_user(
            username="testuser", 
            email="test@test.com",
            phone_number="+254700000000"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_products(self):
        url = '/api/products/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Test Product")

    def test_get_categories(self):
        url = '/api/categories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Test Category")

    def test_average_price_endpoint(self):
        url = '/api/products/average_price_by_category/'
        response = self.client.get(url, {'category_id': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_price', response.data)
        self.assertEqual(response.data['average_price'], 10.99)

class ModelTestCase(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")
        
    def test_category_hierarchy(self):
        parent = Category.objects.create(name="Electronics")
        child = Category.objects.create(name="Phones", parent=parent)
        self.assertEqual(child.parent, parent)

    def test_product_creation(self):
        category = Category.objects.create(name="Books")
        product = Product.objects.create(
            name="Django Book",
            description="Learn Django",
            price=29.99,
            category=category,
            stock_quantity=50
        )
        self.assertEqual(product.name, "Django Book")
        self.assertTrue(product.is_in_stock)

    def test_order_creation(self):
        customer = Customer.objects.create_user(
            username="testuser", 
            email="test@test.com",
            phone_number="+254700000000"
        )
        order = Order.objects.create(
            customer=customer, 
            total_amount=25.00,
            notes="Test order"
        )
        self.assertEqual(order.customer, customer)
        self.assertEqual(float(order.total_amount), 25.0)
        self.assertEqual(order.status, 'pending')
