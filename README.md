# Django E-Commerce Platform

A multi-vendor e-commerce application built using Django. The platform allows vendors to manage their products, customers to browse and purchase items, and includes features such as cart management, order processing, and secure payment integration.

---


## 🚀 Features
- Multi-vendor functionality with separate vendor dashboards.
- Product management with support for color and size variants.
- Shopping cart with dynamic updates.
- Coupon and discount management.
- Seamless order processing with address selection and payment integration.
- Search functionality and category-based product filtering.
- Responsive UI styled with Bootstrap and CSS.

---


## 🛠️ Tech Stack
**Frontend:**
- HTML, CSS, and JavaScript (with jQuery for interactions)
- Bootstrap and CSS

**Backend:**
- Django
- PostgreSQL (or your chosen database)

---


## ⚙️ Installation and Setup
Follow these steps to set up the project on your local machine:


### Prerequisites
- Python 3.8+
- PostgreSQL (or your chosen database)


### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Jayesh-cj/Multi-Vendor-Ecommerce-Application
    cd Multi-Vendor-Ecommerce-Application
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    env\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    - Update `settings.py` with your database credentials.
    - Run migrations:
        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

---


## Usage

After starting the server, you can access the application at `http://127.0.0.1:8000/`. Log in using the superuser credentials created earlier to manage the system.


## Contact

For any inquiries or feedback, feel free to reach out:

- **Name:** Jayesh C .J
- **Email:** jayeshcj2003@gmail.com
- **GitHub:** [Jayesh-cj](https://github.com/Jayesh-cj)

---