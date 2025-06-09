# Intego360 Project

## 🎯 Project Overview

**Intego360** is a centralized digital platform that simplifies the management of **agriculture**, **health**, and **education** data in one place. It empowers organizations to track activities, monitor progress, and make data-driven decisions through real-time dashboards, alerts, and AI-powered insights. Intego360 enhances efficiency, ensures timely interventions, and strengthens cross-sectoral planning for greater societal impact.

## 📘 Description

Intego360 provides a seamless digital experience with modular features tailored to each sector:

- **Agriculture**: Track farmers, crops, yields, market prices, alerts, and extension services.
- **Health**: Manage patients, appointments, medical records, and health analytics.
- **Education**: Oversee students, attendance, courses, facilities, and academic performance.

With cross-sector AI, the platform delivers performance monitoring, recommendations, forecasting, and automated alerts—helping governments, NGOs, and institutions make smarter, faster decisions.

## 🔗 GitHub Repository

👉 [https://github.com/uwasejeannine/Intego360](https://github.com/uwasejeannine/Intego360)

---

## 🚀 Features

### 🌾 Agriculture Module
- Manage farmer profiles, crops, yields, and production history
- Real-time market prices and trend analysis
- Alerts for weather changes, pest outbreaks, and policy changes
- Track farmer cooperatives and training services

### 🏥 Health Module
- Patient profiles, appointment scheduling, and treatment records
- Health facility tracking: equipment, supplies, staffing
- Community health programs: vaccination, maternal health, outreach
- Disease outbreak monitoring and public health indicators

### 🎓 Education Module
- Student records, attendance, academic progress
- Course management and teacher qualifications
- Infrastructure and resource tracking
- Adult literacy and skills development programs

### 🤖 AI-Powered Insights
- Cross-sector performance scoring with KPIs
- Forecast trends, detect risks, and identify gaps
- Resource allocation recommendations
- Real-time alerts when thresholds are breached

---

## ⚙️ Prerequisites

Ensure the following are installed:

- Node.js (LTS)
- npm or yarn
- Python 3.8+
- pip
- Git

---

## 🛠️ Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/uwasejeannine/Intego360.git
cd Intego360
```

### 2. Backend Setup (Django)

```bash
cd backend/intego360_backend
python -m venv venv

# Activate the environment
source venv/bin/activate  # macOS/Linux
# OR
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API will run on http://127.0.0.1:8000/api/

### 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

Frontend will open on http://localhost:3000

### 🌍 Environment Variables

Create a `.env` file in both frontend and backend with:

```plaintext
# Backend
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

### 🎨 Designs

#### 📐 Figma Mockups
[Figma Designs](https://www.figma.com/design/2PZLV68pGB9oOBMS4y9WfM/Intego360?node-id=1-2&p=f&t=SrWStKZnyUsg3nXU-0)

#### 🖼️ UI Screenshots

<img width="950" alt="image" src="https://github.com/user-attachments/assets/37261edb-f6d9-4fa2-8890-e360e49d53bc" />
<img width="950" alt="image" src="https://github.com/user-attachments/assets/9e0cebab-8caf-424d-bae8-d4bd5afe4c5b" />
<img width="955" alt="image" src="https://github.com/user-attachments/assets/b6ec2752-23bf-4a5a-bfa3-eff370b76f7a" />
<img width="959" alt="image" src="https://github.com/user-attachments/assets/3aee4ab3-338c-48f1-8ca2-3509630c36bb" />
<img width="959" alt="image" src="https://github.com/user-attachments/assets/aded597c-7d6c-4399-a6ab-466744434503" />

## 🚀 Deployment Plan

1. **Backend Deployment**:
   - Deploy the Django backend on a cloud platform like Heroku or DigitalOcean
   - Set up a production database (e.g., PostgreSQL)
   - Configure environment variables for production

2. **Frontend Deployment**:
   - Build the React application for production using `npm run build` or `yarn build`
   - Deploy the built files on a static hosting service like Netlify, Vercel, or AWS S3

3. **Domain and SSL**:
   - Set up a custom domain for the application
   - Configure SSL certificates for secure HTTPS connections

4. **Monitoring and Maintenance**:
   - Set up monitoring tools to track application performance and errors
   - Regularly update dependencies and apply security patches

## 🎥 Video Demonstration

[Watch Full Demo (7 mins)](https://vimeo.com/1091802560/724c85d516?ts=0&share=copy)

The video focuses on live demonstration of functionalities across modules with real-time data flow, alerts, and analytics. No long intros—just results.

## 📁 Folder Structure

```
Intego360/
├── backend/
│   └── intego360_backend/
├── frontend/
│   └── [React App]
├── README.md
├── demo/
│   └── intego360_demo.mp4
└── .env.example
```

---

## 🔧 Troubleshooting

*   **CORS Issues**: If you encounter CORS errors, ensure `django-cors-headers` is installed and configured correctly in your Django settings.
*   **404 Not Found**: Verify your Django `urls.py` configurations and ensure your `ViewSet` and `Serializer` are correctly defined.
*   **Frontend Data Loading**: Check your browser's developer console for network requests and ensure the backend is running and accessible. 
