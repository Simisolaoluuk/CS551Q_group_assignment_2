# Educational Dashboard

This Django-based web application provides an interactive dashboard for exploring and analyzing educational institutions across the United Kingdom. The platform allows users to view institution details, compare performance metrics, manage favorites, and filter institutions by various criteria.This project was developed as part of the CS551Q group assignment to demonstrate full‑stack development using Django.

## Features

- Institution Listings: Browse through a comprehensive database of UK educational institutions including universities, colleges, and schools.
- Detailed Views: Access in-depth information about each institution, including location, category, and performance records.
- Comparison Tool: Compare multiple institutions side-by-side based on key metrics.
- Favorites System: Save and manage a list of favorite institutions.
- User Authentication: Secure login and registration system for personalized experiences.
- Filtering and Search: Advanced filtering options by region, category, and other attributes.
- Responsive Design: Mobile-friendly layouts for desktop, tablet, and mobile devices.

## Project Structure

The project is organized as follows:

- `edu_dashboard/`: Main Django project settings and configuration.
- `institutions/`: Core application containing models, views, templates, and static files.
- `dataset/`: Scripts and CSV files for generating and managing sample data.
- `manage.py`: Django's command-line utility for administrative tasks.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (recommended for environment management)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <gh repo clone Simisolaoluuk/CS551Q_group_assignment_2>
   cd CS551Q_group_assignment_2
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install django
   ```
   Note: If you have a `requirements.txt` file, use `pip install -r requirements.txt` instead.

4. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

## Data Loading

The application uses sample data for demonstration purposes. To load the dataset:

1. **Generate the Dataset** (if not already present):
   ```bash
   cd dataset
   python generate_dataset.py
   ```

2. **Load Data into the Database**:
   ```bash
   python manage.py load_data
   ```

This command will populate the database with regions, institutions, and performance records from the CSV files in the `dataset/` directory.

## Testing

To run the test suite:

```bash
python manage.py test
```

The tests cover model functionality, views, authentication, and other core features. Ensure all tests pass before deploying or making significant changes.

## Testing coverage:
The project includes 41 automated Django test cases covering:
- ⁠models
- ⁠views
- ⁠authentication
- ⁠favourites
- ⁠institution comparison
- ⁠filtering and search
- ⁠invalid inputs
- ⁠data loading functionality

## Run Instructions

1. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the Application**:
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

3. **Admin Interface** (if superuser created):
   Visit `http://127.0.0.1:8000/admin/` to access Django's admin panel.

## Configuration

Key settings can be modified in `edu_dashboard/settings.py`:

- **DEBUG**: Set to `False` for production.
- **SECRET_KEY**: Use a secure key in production.
- **ALLOWED_HOSTS**: Configure for your deployment environment.
- **Database**: Default is SQLite; modify `DATABASES` for other databases.

Environment variables can be used for sensitive settings:
```bash
export SECRET_KEY='your-secret-key'
export DEBUG='False'
export ALLOWED_HOSTS='yourdomain.com'
```
## Deployment
`https://umama2026.pythonanywhere.com/`

## Technologies Used
- Python
- Django
- SQLite
- ⁠HTML5
- ⁠CSS3
- ⁠JavaScript
- ⁠Chart.js
- ⁠Git and GitHub

## Acknowledgments

- Dataset generation inspired by real UK educational institution data.
- Built with Django framework for robust web development.