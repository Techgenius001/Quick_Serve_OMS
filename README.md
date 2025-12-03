# SmartKibandaski - Hotel Orders Management System

A Django-based food ordering and management system for SmartKibandaski Hotel in Thika Town, Kenya.

## Features

### Current Features (v1.0)

- ✅ User Authentication (Login/Signup)
- ✅ Role-based Access (Admin/Customer)
- ✅ Landing Page with Hero Section
- ✅ Menu Browsing with Categories & Filters
- ✅ Responsive Design (Mobile-First)
- ✅ Menu Item Management (Admin)

### Upcoming Features

- 🔄 Shopping Cart
- 🔄 Checkout Process (M-Pesa & Cash on Delivery)
- 🔄 Customer Dashboard
- 🔄 Admin Dashboard
- 🔄 Order Tracking
- 🔄 Dark/Light Mode

## Tech Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite3 (Development), PostgreSQL (Production)
- **Frontend**: Tailwind CSS, Vanilla JavaScript
- **Authentication**: Django Auth with Custom User Model
- **Deployment**: Render

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Techgenius001/SKOM-Orders_Management_System_Django_F.Project.git
cd SKOM-Orders_Management_System_Django_F.Project
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create superuser:

```bash
python manage.py createsuperuser
```

6. Run development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the application.

## Project Structure

```
smartkibadaski/          # Main project configuration
accounts/                # User authentication & management
orders/                  # Menu & ordering functionality
templates/               # Global templates
static/                  # Static files (CSS, JS, images)
media/                   # User-uploaded files
```

## Deployment on Render

This project is configured for deployment on Render. See deployment documentation for details.

## Contributing

This is a final year project. Contributions are welcome for educational purposes.

## License

All rights reserved - SmartKibandaski © 2024

## Contact

- Location: Thika Town, Central County, Kenya
- Email: info@smartkibandaski.co.ke
- Phone: +254 712 345 678
