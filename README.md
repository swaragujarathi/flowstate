# FlowState – AI-Powered Study Planner

FlowState is an AI-powered study planner that helps students organize their studies more effectively. It creates personalized study schedules, dynamically adapts them as progress changes, and uses Google's Gemini AI to convert natural language study plans into structured tasks.

# Key Features

✔ AI-powered task generation
✔ Dynamic timetable generation
✔ Deadline-aware and priority based scheduling
✔ Progress tracking
✔ Productivity analytics and study streak tracking
✔ JWT Authentication
✔ Responsive modern UI

## Tech Stack

**Frontend**

* React
* TypeScript
* Vite
* Tailwind CSS
* Recharts

**Backend**

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication
* Google Gemini API

**Deployment**

* Vercel (Frontend)
* Render (Backend)
* Neon PostgreSQL (Database)

## Local Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## What I Learned

- Building full-stack applications with React and FastAPI
- REST API design and backend architecture
- PostgreSQL database design with SQLAlchemy
- JWT-based authentication and authorization
- Prompt engineering and LLM integration using Google Gemini
- Parsing unstructured text into structured data
- Deploying production applications using Vercel, Render and Neon PostgreSQL

## Live Demo

Frontend: [https://panic-planner.vercel.app/]

## Future Improvements
AI-powered study recommendations
Burnout detection
Calendar integration
Pomodoro timer intergration
