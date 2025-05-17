# Disease History Application

**Disease History** is a web application designed for healthcare professionals to manage patient records, track treatment progress, and analyze medical histories to determine effective treatment paths. Built with React for the frontend and FastAPI for the backend, it integrates Google OAuth for secure authentication.

---

## Features

### Patient Management
- Add and manage patient profiles with **general information** (name, age, contact) and **medical anamnesis** (past illnesses, allergies, family history).
- Organize patient data in a structured, easy-to-navigate interface.

### Treatment Tracking
- Create **chronological records** for each patient's disease history (symptoms, diagnoses, medications).

### History Analysis
- Visualize treatment timelines to identify patterns or correlations.

### Security & Authentication
- Secure access via **Google OAuth** for doctors and authorized personnel.

---

## Technologies Used

### Frontend
- **React** (with React Router for navigation)
- **Bootstrap**

### Backend
- **FastAPI** (Python framework)
- **Relational Database** (e.g., PostgreSQL, SQLite)
- **SQLAlchemy** (ORM for database operations)

### Authentication
- **Google OAuth 2.0** for user sign-in
- **JWT** (JSON Web Tokens) for session management

---

## Installation

### Prerequisites
- Node.js (v14+) and npm/yarn for the frontend
- Python (v3.7+) and pip for the backend
- PostgreSQL (or another relational database)

### Backend Setup
1. Clone the repository:
   git clone https://github.com/denis-96/disease-history.git
   cd disease-history-app/backend
   
3. Create a virtual environment and install dependencies:
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   
5. Set up the database:
   alembic upgrade head  # If using Alembic for migrations

### Frontend Setup
1. Navigate to the frontend directory:
   cd ../frontend
   
3. Install dependencies:
   npm install


---

## Configuration

### Backend
Create a `.env` file in the `backend` directory:

DATABASE_URL=postgresql://user:password@localhost/disease_history
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret
SECRET_KEY=your_secret_key_for_jwt


### Frontend
Create a `.env` file in the `frontend` directory:

REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_GOOGLE_OAUTH_CLIENT_ID=your_google_client_id_for_frontend

---

## Usage

1. Start the backend server:
   cd backend
   uvicorn main:app --reload

2. Start the frontend development server:
   cd frontend
   npm start

3. Sign in with your Google account (configured in the Google Cloud Console) to begin managing patients.

## Authentication Flow
1. Users click "Sign in with Google" on the frontend.
2. The backend redirects to Google's OAuth consent screen.
3. Upon successful authentication, Google returns an authorization code.
4. The backend exchanges the code for a JWT token, which is used for subsequent API requests.

---

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Ensure tests pass and document changes clearly.

---

**Contact**  
Denis Bargan - denn.bargan@gmail.com
