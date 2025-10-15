# OmniMerch-ERP

A comprehensive Enterprise Resource Planning (ERP) system built with Django REST Framework, featuring JWT authentication, MySQL support, and modular architecture.

## Features

### 🔐 Authentication & Security
- JWT (JSON Web Token) authentication
- Secure token-based API access
- User management and permissions

### 📦 Inventory Management
- Product catalog with SKU tracking
- Supplier management
- Category organization
- Stock movement tracking (in/out/adjustments)
- Low stock alerts
- Real-time inventory levels

### 👥 CRM (Customer Relationship Management)
- Customer database (Individual & Business)
- Lead management with status tracking
- Contact history and interaction logs
- Lead conversion tracking

### 🔧 Maintenance Management
- Asset tracking and management
- Work order system
- Priority-based task management
- Cost estimation and tracking
- Schedule management

### 💰 Sales (POS + Online)
- Point of Sale (POS) transactions
- Online order management
- Order status tracking
- Payment processing (Multiple payment methods)
- Order history and analytics

### 📊 Basic Accounting
- Invoice generation and management
- Chart of accounts
- General ledger entries
- Expense tracking
- Payment records

### 📈 Admin Dashboard
- Business overview metrics
- Sales analytics
- Inventory reports
- Revenue tracking
- Real-time statistics

## Technology Stack

- **Backend Framework:** Django 5.2.7
- **API Framework:** Django REST Framework 3.16.1
- **Authentication:** djangorestframework-simplejwt 5.5.1
- **Database:** MySQL 8.0 (with SQLite fallback for development)
- **API Documentation:** drf-yasg (Swagger/OpenAPI)
- **Caching:** Redis
- **Deployment:** Docker & Docker Compose
- **Web Server:** Gunicorn

## Project Structure

```
OmniMerch-ERP/
├── omnimerch_erp/          # Main project settings
│   ├── settings.py         # Django settings with environment variables
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── inventory/             # Inventory management app
├── crm/                   # Customer relationship management app
├── maintenance/           # Maintenance management app
├── sales/                 # Sales (POS + Online) app
├── accounting/            # Basic accounting app
├── dashboard/             # Admin dashboard and analytics app
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Multi-container Docker setup
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── manage.py             # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.12+
- MySQL 8.0+ (or use SQLite for development)
- Docker & Docker Compose (for containerized deployment)

### Option 1: Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MoedCode/OmniMerch-ERP.git
   cd OmniMerch-ERP
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000`

### Option 2: Docker Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/MoedCode/OmniMerch-ERP.git
   cd OmniMerch-ERP
   ```

2. **Update docker-compose.yml**
   - Change default passwords
   - Update SECRET_KEY

3. **Build and start containers**
   ```bash
   docker-compose up -d --build
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

   The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/`
- **Django Admin:** `http://localhost:8000/admin/`

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh access token

### Inventory
- `/api/inventory/products/` - Product CRUD operations
- `/api/inventory/suppliers/` - Supplier management
- `/api/inventory/categories/` - Category management
- `/api/inventory/stock-movements/` - Stock movement tracking
- `/api/inventory/products/low_stock/` - Low stock alerts

### CRM
- `/api/crm/customers/` - Customer management
- `/api/crm/leads/` - Lead management
- `/api/crm/contacts/` - Contact history

### Maintenance
- `/api/maintenance/assets/` - Asset management
- `/api/maintenance/work-orders/` - Work order management

### Sales
- `/api/sales/orders/` - Order management (POS & Online)
- `/api/sales/order-items/` - Order line items
- `/api/sales/payments/` - Payment processing
- `/api/sales/orders/pos_orders/` - POS orders only
- `/api/sales/orders/online_orders/` - Online orders only

### Accounting
- `/api/accounting/invoices/` - Invoice management
- `/api/accounting/accounts/` - Chart of accounts
- `/api/accounting/ledger-entries/` - Ledger entries
- `/api/accounting/expenses/` - Expense tracking

### Dashboard
- `/api/dashboard/overview/` - Business overview metrics
- `/api/dashboard/reports/sales/` - Sales reports
- `/api/dashboard/reports/inventory/` - Inventory reports

## Authentication Usage

1. **Obtain Token**
   ```bash
   curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username":"your_username","password":"your_password"}'
   ```

2. **Use Token in Requests**
   ```bash
   curl -X GET http://localhost:8000/api/inventory/products/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

## Environment Variables

Key environment variables (see `.env.example`):

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DB_ENGINE` - Database engine
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `JWT_ACCESS_TOKEN_LIFETIME` - JWT access token lifetime (minutes)
- `JWT_REFRESH_TOKEN_LIFETIME` - JWT refresh token lifetime (minutes)

## Development

### Running Tests
```bash
python manage.py test
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Roadmap

- [ ] Multi-tenant support
- [ ] Advanced reporting and analytics
- [ ] Email notifications
- [ ] Export data to PDF/Excel
- [ ] Mobile app integration
- [ ] Barcode/QR code scanning
- [ ] Multi-currency support
- [ ] Advanced inventory forecasting
