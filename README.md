# Intego360 Project

## Project Overview

Intego360 is a comprehensive agricultural management system designed to streamline various aspects of farming operations. It comprises a React/TypeScript frontend for an intuitive user interface and a Django/Django Rest Framework (DRF) backend for robust data management and API services.

## Features

### Agriculture
*   **Farmer Management**: Track and manage farmer profiles.
*   **Crop Management**: Keep records of different crops.
*   **Production Tracking**: Monitor agricultural production.
*   **Market Price Analysis**: Stay updated with market prices.
*   **Alert System**: Receive timely alerts for critical events.
*   **Extension Services**: Manage extension activities.

### Health
*   **Patient Management**: Track and manage patient profiles.
*   **Medical Records**: Keep records of patient medical history.
*   **Appointment Scheduling**: Manage patient appointments.
*   **Health Analytics**: Analyze health data for insights.

### Education
*   **Student Management**: Track and manage student profiles.
*   **Course Management**: Keep records of different courses.
*   **Attendance Tracking**: Monitor student attendance.
*   **Performance Analytics**: Analyze student performance data.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Node.js** (LTS version recommended)
*   **npm** or **Yarn**
*   **Python 3.8+**
*   **pip** (Python package installer)
*   **Git**

## Project Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Intego360
```

### 2. Backend Setup (Django/DRF)

Navigate to the backend directory:

```bash
cd backend/intego360_backend
```

Create and activate a Python virtual environment:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, you can create it by installing Django and Django REST Framework:

```bash
pip install django djangorestframework
pip freeze > requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Create a superuser (optional, for Django Admin):

```bash
python manage.py createsuperuser
```

Run the backend server:

```bash
python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000/api/`.

### 3. Frontend Setup (React/TypeScript)

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the Node.js dependencies:

```bash
npm install
# or
yarn install
```

Ensure your `package.json` in the `frontend` directory has the proxy configured to point to your backend. It should look something like this:

```json
"proxy": "http://localhost:8000"
```

Run the frontend development server:

```bash
npm start
# or
yarn start
```

The frontend application will open in your browser, typically at `http://localhost:3000`.

## Environment Variables

Create a `.env` file in the root of your project directory with the following example variables:

```plaintext
# Backend Environment Variables
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=your_database_url_here

# Frontend Environment Variables
REACT_APP_API_URL=http://localhost:8000/api
```

Replace `your_secret_key_here` and `your_database_url_here` with your actual secret key and database URL.

## Project Interface Screenshots

<img width="950" alt="image" src="https://github.com/user-attachments/assets/37261edb-f6d9-4fa2-8890-e360e49d53bc" />
<img width="950" alt="image" src="https://github.com/user-attachments/assets/9e0cebab-8caf-424d-bae8-d4bd5afe4c5b" />
<img width="955" alt="image" src="https://github.com/user-attachments/assets/b6ec2752-23bf-4a5a-bfa3-eff370b76f7a" />
<img width="959" alt="image" src="https://github.com/user-attachments/assets/3aee4ab3-338c-48f1-8ca2-3509630c36bb" />
<img width="959" alt="image" src="https://github.com/user-attachments/assets/aded597c-7d6c-4399-a6ab-466744434503" />





---

## Troubleshooting

*   **CORS Issues**: If you encounter CORS errors, ensure `django-cors-headers` is installed and configured correctly in your Django settings.
*   **404 Not Found**: Verify your Django `urls.py` configurations and ensure your `ViewSet` and `Serializer` are correctly defined.
*   **Frontend Data Loading**: Check your browser's developer console for network requests and ensure the backend is running and accessible. 
