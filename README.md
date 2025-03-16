# FériasFlow: Backend API for Vacation Management

## Overview

The Férias (Vacation) backend is a robust Django REST Framework API for managing employee vacation periods. It provides a complete set of endpoints for creating, retrieving, updating, and deleting vacation records with comprehensive filtering and sorting options.

## Technology Stack

- **Framework**: Django with Django REST Framework
- **Database**: PostgreSQL (configurable)
- **API**: RESTful API architecture
- **Authentication**: Token-based authentication
- **Documentation**: Auto-generated API documentation with Swagger/OpenAPI

## Key Features

- 📊 **Complete CRUD Operations**: Full API for vacation records management
- 🔒 **Permission-Based Access**: Role-based access control for different operations
- 🔍 **Advanced Filtering**: Filter vacations by status, date ranges, and employees
- 📱 **Mobile-Ready API**: Optimized endpoints for mobile and web clients
- 🔄 **Status Workflow**: Built-in vacation approval workflow (pending, approved, rejected)
- 📅 **Date Validation**: Server-side validation for vacation date ranges
- 📝 **Detailed Logging**: Comprehensive logging of all operations
- 👤 **Admin Integration**: Custom Django admin interface for easy management

## API Endpoints

```
GET    /api/vacations/         - List all vacation records
POST   /api/vacations/         - Create a new vacation record
GET    /api/vacations/{id}/    - Retrieve a specific vacation record
PUT    /api/vacations/{id}/    - Update a specific vacation record
DELETE /api/vacations/{id}/    - Delete a specific vacation record
GET    /api/vacations/pending/ - List all pending vacation requests
GET    /api/vacations/approved/ - List all approved vacation requests
```

## Technical Architecture

### Directory Structure

```
/Férias
├── __init__.py
├── admin.py          # Admin interface configuration
├── apps.py           # App configuration
├── models.py         # Data models
├── serializers.py    # API serializers
├── tests.py          # Unit tests
├── urls.py           # URL routing
└── views.py          # API views and business logic
```

## Models

The `Vacation` model is the core data structure for vacation records:

```python
class Vacation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    employee_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## API Usage Examples

### Listing Vacation Records

```bash
curl -X GET http://localhost:8000/api/vacations/ -H "Content-Type: application/json"
```

Response:
```json
[
  {
    "id": 1,
    "employee_name": "John Smith",
    "start_date": "2023-08-01",
    "end_date": "2023-08-15",
    "status": "approved",
    "reason": "Summer vacation",
    "notes": null,
    "created_at": "2023-07-01T10:00:00Z",
    "updated_at": "2023-07-05T14:30:00Z"
  },
  ...
]
```

### Creating a Vacation Record

```bash
curl -X POST http://localhost:8000/api/vacations/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee_name": "Jane Doe",
    "start_date": "2023-09-10",
    "end_date": "2023-09-20",
    "reason": "Family visit"
  }'
```

## File Descriptions

### models.py
Defines the data structure for vacation records, including status choices, date fields, and metadata.

### serializers.py
Converts between Python objects and JSON representations for the API.

### views.py
Contains the ViewSet that handles all API operations, including custom actions for filtering by status.

### urls.py
Configures URL routing for all API endpoints using Django REST Framework's router.

### admin.py
Customizes the Django admin interface for vacation management.

## Installation and Setup

1. Clone the repository
   ```
   git clone https://github.com/MarcioMiguel22/Test02.git
   cd Test02
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run migrations
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Start the development server
   ```
   python manage.py runserver
   ```

5. Access the API at `http://localhost:8000/api/vacations/`

## Dependencies

- Django
- Django REST Framework
- djangorestframework-simplejwt (optional, for JWT authentication)
- django-filter (for advanced filtering)
- drf-yasg (for API documentation)

## Frontend Integration

This backend is designed to work seamlessly with the FériasFlow frontend component. The API provides exactly the data structure expected by the frontend:

- Vacation records include all necessary fields
- Custom endpoints for status filtering
- Proper error handling and validation responses
- CORS configuration for cross-domain requests

## API Authentication

The API can be configured to use various authentication methods:

```python
# settings.py example
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

## Error Handling

The API provides standardized error responses for various scenarios:

- 400 Bad Request: For validation errors
- 401 Unauthorized: For authentication failures
- 403 Forbidden: For permission issues
- 404 Not Found: For non-existent resources
- 500 Internal Server Error: For server-side issues

## Code Practices

- RESTful API design
- Proper model validation
- Comprehensive serialization
- Custom admin interface
- Extensive filtering options
- Proper status codes for responses

## Contributing

To contribute to this backend:

1. Follow Django and DRF best practices
2. Write unit tests for new features
3. Update the documentation for API changes
4. Maintain backward compatibility
