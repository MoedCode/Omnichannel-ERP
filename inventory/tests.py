from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Category, Supplier, Product, StockMovement


class InventoryModelsTestCase(TestCase):
    """Test cases for Inventory models"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Electronics', description='Electronic items')
        self.supplier = Supplier.objects.create(
            name='Tech Supplier',
            contact_person='John Doe',
            email='john@supplier.com',
            phone='+1234567890',
            address='123 Tech Street'
        )

    def test_category_creation(self):
        """Test category creation"""
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(str(self.category), 'Electronics')

    def test_supplier_creation(self):
        """Test supplier creation"""
        self.assertEqual(self.supplier.name, 'Tech Supplier')
        self.assertEqual(str(self.supplier), 'Tech Supplier')

    def test_product_creation(self):
        """Test product creation"""
        product = Product.objects.create(
            name='Laptop',
            sku='LAP001',
            category=self.category,
            supplier=self.supplier,
            cost_price=800.00,
            selling_price=1200.00,
            quantity_in_stock=50,
            reorder_level=10
        )
        self.assertEqual(product.name, 'Laptop')
        self.assertEqual(str(product), 'Laptop (LAP001)')

    def test_low_stock_property(self):
        """Test low stock detection"""
        product = Product.objects.create(
            name='Mouse',
            sku='MOU001',
            category=self.category,
            supplier=self.supplier,
            cost_price=10.00,
            selling_price=20.00,
            quantity_in_stock=5,
            reorder_level=10
        )
        self.assertTrue(product.is_low_stock)

    def test_stock_movement_creation(self):
        """Test stock movement creation"""
        product = Product.objects.create(
            name='Keyboard',
            sku='KEY001',
            category=self.category,
            supplier=self.supplier,
            cost_price=30.00,
            selling_price=50.00,
            quantity_in_stock=100,
            reorder_level=20
        )
        movement = StockMovement.objects.create(
            product=product,
            movement_type='IN',
            quantity=50,
            created_by=self.user
        )
        self.assertEqual(movement.quantity, 50)
        self.assertEqual(movement.movement_type, 'IN')


class InventoryAPITestCase(APITestCase):
    """Test cases for Inventory API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Test Category')
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_person='Jane Doe',
            email='jane@supplier.com',
            phone='+0987654321',
            address='456 Supply Ave'
        )

    def test_list_categories(self):
        """Test listing categories"""
        response = self.client.get('/api/inventory/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """Test creating a product"""
        data = {
            'name': 'Test Product',
            'sku': 'TEST001',
            'category': self.category.id,
            'supplier': self.supplier.id,
            'cost_price': '100.00',
            'selling_price': '150.00',
            'quantity_in_stock': 100,
            'reorder_level': 20,
            'status': 'ACTIVE'
        }
        response = self.client.post('/api/inventory/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_low_stock_endpoint(self):
        """Test low stock products endpoint"""
        Product.objects.create(
            name='Low Stock Item',
            sku='LOW001',
            category=self.category,
            supplier=self.supplier,
            cost_price=10.00,
            selling_price=20.00,
            quantity_in_stock=5,
            reorder_level=10
        )
        response = self.client.get('/api/inventory/products/low_stock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
