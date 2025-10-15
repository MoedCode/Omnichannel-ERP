# Deployment Guide

This guide provides step-by-step instructions for deploying the OmniMerch ERP system.

## Prerequisites

### For Local Development
- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment support

### For Production Deployment
- Docker and Docker Compose
- MySQL 8.0+ (or use the provided Docker setup)
- Redis (optional, for caching)
- A domain name (for production)
- SSL certificate (recommended for production)

## Local Development Deployment

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/MoedCode/OmniMerch-ERP.git
   cd OmniMerch-ERP
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the development server**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python manage.py runserver
   ```

4. **Access the application**
   - API: http://localhost:8000/
   - Swagger Documentation: http://localhost:8000/swagger/
   - Admin Panel: http://localhost:8000/admin/

### Manual Setup

If you prefer manual setup:

1. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Docker Deployment

### Quick Start with Docker Compose

1. **Clone the repository**
   ```bash
   git clone https://github.com/MoedCode/OmniMerch-ERP.git
   cd OmniMerch-ERP
   ```

2. **Update docker-compose.yml**
   
   Edit the `docker-compose.yml` file and update these values:
   - Change `MYSQL_ROOT_PASSWORD`
   - Change `MYSQL_PASSWORD`
   - Change `SECRET_KEY` (generate a secure key)

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

6. **Access the application**
   - API: http://localhost:8000/
   - Swagger Documentation: http://localhost:8000/swagger/
   - Admin Panel: http://localhost:8000/admin/

### Docker Commands

```bash
# View logs
docker-compose logs -f web

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# Access Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test

# Create backup of database
docker-compose exec db mysqldump -u root -p omnimerch_erp > backup.sql
```

## Production Deployment

### Recommended Production Setup

1. **Use a reverse proxy** (Nginx or Apache)
2. **Enable HTTPS** with SSL certificates (Let's Encrypt)
3. **Use a production database** (MySQL or PostgreSQL)
4. **Configure Redis** for caching
5. **Set up monitoring** (Sentry, New Relic, etc.)
6. **Configure backup** strategy

### Environment Variables for Production

Update your `.env` file:

```bash
SECRET_KEY=your-very-secure-secret-key-min-50-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.mysql
DB_NAME=omnimerch_erp
DB_USER=erp_user
DB_PASSWORD=secure-database-password
DB_HOST=your-db-host
DB_PORT=3306

# JWT Settings (in minutes)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/OmniMerch-ERP/staticfiles/;
    }

    location /media/ {
        alias /path/to/OmniMerch-ERP/media/;
    }
}
```

### Systemd Service (For Linux Servers)

Create `/etc/systemd/system/omnimerch.service`:

```ini
[Unit]
Description=OmniMerch ERP
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/OmniMerch-ERP
Environment="PATH=/path/to/OmniMerch-ERP/venv/bin"
ExecStart=/path/to/OmniMerch-ERP/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    omnimerch_erp.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable omnimerch
sudo systemctl start omnimerch
sudo systemctl status omnimerch
```

## Cloud Deployment Options

### AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI
2. Initialize EB application
   ```bash
   eb init -p python-3.12 omnimerch-erp
   ```
3. Create environment
   ```bash
   eb create omnimerch-env
   ```
4. Deploy
   ```bash
   eb deploy
   ```

### Heroku

1. Create Heroku app
   ```bash
   heroku create omnimerch-erp
   ```

2. Add PostgreSQL addon
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Set environment variables
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```

4. Deploy
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Digital Ocean App Platform

1. Connect your GitHub repository
2. Configure environment variables in the dashboard
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn omnimerch_erp.wsgi:application`
5. Deploy automatically on push

## Database Migration

### From SQLite to MySQL

1. **Export data from SQLite**
   ```bash
   python manage.py dumpdata > data.json
   ```

2. **Update .env with MySQL settings**
   ```bash
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=omnimerch_erp
   # ... other MySQL settings
   ```

3. **Run migrations on MySQL**
   ```bash
   python manage.py migrate
   ```

4. **Import data**
   ```bash
   python manage.py loaddata data.json
   ```

## Monitoring and Maintenance

### Health Check Endpoints

Create a simple health check:
- Database connectivity
- Redis connectivity (if using)
- Disk space
- Memory usage

### Logging

Configure logging in production:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/omnimerch/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Backup Strategy

1. **Database backups** - Daily automated backups
2. **Media files** - Regular backup to S3 or similar
3. **Configuration files** - Version controlled
4. **Testing backups** - Regular restore tests

## Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use HTTPS (SSL/TLS)
- [ ] Keep dependencies updated
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Use strong database passwords
- [ ] Enable database backups
- [ ] Set up monitoring and alerts
- [ ] Review Django security checklist
- [ ] Configure rate limiting
- [ ] Set up fail2ban or similar

## Performance Optimization

1. **Enable Redis caching**
2. **Use CDN for static files**
3. **Configure database connection pooling**
4. **Enable gzip compression**
5. **Use database indexes properly**
6. **Configure proper logging levels**
7. **Monitor and optimize slow queries**

## Troubleshooting

### Common Issues

**Issue: Database connection errors**
- Check database credentials in .env
- Ensure database server is running
- Verify firewall rules

**Issue: Static files not loading**
- Run `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL settings
- Verify web server configuration

**Issue: JWT token errors**
- Check JWT_ACCESS_TOKEN_LIFETIME setting
- Ensure system time is synchronized
- Verify SECRET_KEY hasn't changed

**Issue: CORS errors**
- Update CORS_ALLOWED_ORIGINS in .env
- Check corsheaders middleware order
- Verify frontend URL is correct

## Support

For issues and questions:
- GitHub Issues: https://github.com/MoedCode/OmniMerch-ERP/issues
- Documentation: See README.md and API_EXAMPLES.md
- Email: contact@omnimerch.com

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
