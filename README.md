# Intego360 Project

## Project Overview

Intego360 is a comprehensive agricultural management system designed to streamline various aspects of farming operations. It comprises a React/TypeScript frontend for an intuitive user interface and a Django/Django Rest Framework (DRF) backend for robust data management and API services.

## Description

Intego360 aims to provide a seamless experience for managing agricultural, health, and educational data. It offers features for tracking farmers, crops, production, market prices, alerts, and extension services in agriculture. Additionally, it includes functionalities for patient management, medical records, appointment scheduling, and health analytics in the health sector. For education, it provides student management, course management, attendance tracking, and performance analytics.

## GitHub Repository

[Link to the GitHub Repository](https://github.com/yourusername/Intego360)

## Features

### Agriculture

Track and manage comprehensive farmer profiles including contact information, land ownership, and farming history
Keep detailed records of different crops, planting seasons, and agricultural activities
Monitor agricultural production yields, harvest quantities, and crop quality metrics
Stay updated with real-time market prices and analyze pricing trends for better decision-making
Receive timely alerts for critical events such as weather warnings, pest outbreaks, and market fluctuations
Manage extension services including farmer training programs, technical assistance, and educational workshops
Track farmer cooperatives, membership data, and collective agricultural activities

### Health

Track and manage comprehensive patient profiles with medical histories and demographic information
Keep detailed records of patient medical history, treatments, diagnoses, and health outcomes
Manage patient appointments, healthcare provider schedules, and medical facility bookings
Analyze health data to generate insights on disease patterns, treatment effectiveness, and population health trends
Monitor health facility resources including equipment, staff capacity, and medical supplies
Track disease outbreaks, epidemiological data, and public health indicators across regions
Oversee vaccination campaigns, maternal health programs, and community health initiatives

### Education

Track and manage comprehensive student profiles including enrollment, academic progress, and personal information
Keep detailed records of courses, curricula, academic programs, and educational materials
Monitor student and teacher attendance with automated tracking and reporting systems
Analyze student performance data to identify learning gaps and educational outcomes
Track school facilities, infrastructure needs, equipment, and educational resources
Monitor teacher qualifications, professional development, training programs, and performance evaluations
Manage literacy programs, adult education initiatives, and skills development courses

### AI-Powered Analytics & Recommendations

AI continuously analyzes data across Agriculture, Health, and Education sectors to identify performance patterns
Generate automated performance scores for each sector based on key performance indicators and benchmarks
Machine learning algorithms identify trends, patterns, and correlations in cross-sectoral data over time
AI intelligently identifies which sectors require immediate attention and prioritizes intervention areas
Provide smart recommendations for optimal resource allocation across districts and sectors
Generate AI-powered suggestions for targeted interventions to improve underperforming areas
Forecast future sector performance and identify potential risks before they become critical issues
Send automated alerts when sector performance declines below acceptable thresholds

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

## Designs

### Figma Mockups
[Figma Mockups](https://www.figma.com/design/2PZLV68pGB9oOBMS4y9WfM/Intego360?node-id=1-2&p=f&t=SrWStKZnyUsg3nXU-0)

### Project Interface Screenshots

<img width="950" alt="image" src="https://github.com/user-attachments/assets/37261edb-f6d9-4fa2-8890-e360e49d53bc" />
<img width="950" alt="image" src="https://github.com/user-attachments/assets/9e0cebab-8caf-424d-bae8-d4bd5afe4c5b" />
<img width="955" alt="image" src="https://github.com/user-attachments/assets/b6ec2752-23bf-4a5a-bfa3-eff370b76f7a" />
<img width="959" alt="image" src="https://github.com/user-attachments/assets/3aee4ab3-338c-48f1-8ca2-3509630c36bb" />
<img width="959" alt="image" src="https://github.com/user-attachments/assets/aded597c-7d6c-4399-a6ab-466744434503" />

## Deployment Plan

1. **Backend Deployment**:
   - Deploy the Django backend on a cloud platform like Heroku or DigitalOcean.
   - Set up a production database (e.g., PostgreSQL).
   - Configure environment variables for production.

2. **Frontend Deployment**:
   - Build the React application for production using `npm run build` or `yarn build`.
   - Deploy the built files on a static hosting service like Netlify, Vercel, or AWS S3.

3. **Domain and SSL**:
   - Set up a custom domain for my  application.
   - Configure SSL certificates for secure HTTPS connections.

4. **Monitoring and Maintenance**:
   - Set up monitoring tools to track application performance and errors.
   - Regularly update dependencies and apply security patches.

---

## Troubleshooting

*   **CORS Issues**: If you encounter CORS errors, ensure `django-cors-headers` is installed and configured correctly in your Django settings.
*   **404 Not Found**: Verify your Django `urls.py` configurations and ensure your `ViewSet` and `Serializer` are correctly defined.
*   **Frontend Data Loading**: Check your browser's developer console for network requests and ensure the backend is running and accessible. 
