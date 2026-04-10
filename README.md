**DO NOT USE SAFARI**


## Tech Stack

- Database: MongoDB
- Backend: FastAPI (Python)
- Frontend: React.js (JavaScript)

---

## 1. Required Software

Python 3.11+
Node.js 18+ (for React frontend)
npm or yarn (frontend package manager)
MongoDB Compass (local database)

## 2. Run the Project

### Backend (FastAPI)

#### 1. Install Python dependencies:

pip install -r requirements.txt

### 1.5 Install Mongo DB Server
Install mongo db server, add mongod.exe to system path or navigate to this directory
Then run the following in a new cmd
```
cd C:\Program Files\MongoDB\Server\8.2\bin
mkdir C:\data\db
mongod --dbpath C:\data\db
```

#### 2. Create .env in project root directory with following contents:

\# Generate with: python -c "import secrets; print(secrets.token_hex(32)) and place here"
SECRET_KEY=

\# MongoDB
MONGODB_URL=mongodb://localhost:27017
DB_NAME=myapp

\# Token expiry
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

#### 4. Navigate to the frontend folder

cd src

#### 3. Start the backend server:

uvicorn app.main:app --reload

FastAPI server runs at localhost:8000
API docs available at localhost:8000/docs

### Frontend (React)

#### 1. Navigate to the frontend folder

cd frontend

#### 2. Install Node dependencies

##### If using npm:

npm install

##### If using yarn:

yarn

#### 3. Start the frontend server

##### If using npm

npm start

##### If using yarn

yarn start

React frontend runs at http://localhost:3000

## 3. Expected Result

Login page loads in browser (http://localhost:3000)
Backend API accessible and routes respond (stubbed if database is not fully connected)
FastAPI docs visible at /docs

## 4. Common Problems
