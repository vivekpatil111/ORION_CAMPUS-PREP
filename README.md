🚀 CampusPrep — From Campus to Career

CampusPrep is an AI-powered interview preparation platform designed to bridge the gap between academic learning and real-world industry expectations.

The platform follows a structured Student → Alumni → Admin → Platform Services workflow, powered by an intelligent MCP Tool (Model Control & Processing Tool) that dynamically decides interview complexity based on student readiness.

🧠 Problem Statement

Many students enter placements without:

Real interview exposure

Industry-relevant feedback

Structured evaluation

Traditional mock interviews are limited, biased, or not scalable.

🎯 Solution Overview

CampusPrep solves this by providing:

AI-driven mock interviews

Resume-based interview routing using MCP Tool

Alumni involvement for real-world validation

Admin-level monitoring and control

Secure, immutable interview results in PDF format

🧩 System Roles
🧑‍🎓 Student

Upload resume

Request interview

Attend interview rounds (voice / video / AI)

View feedback and result PDF

🎓 Alumni

View student interview requests

Accept or reject requests

Validate interview flow with industry perspective

🛡️ Admin

Verify alumni

Monitor interview requests

Oversee interview quality and fairness

🧠 MCP Tool (Model Control & Processing Tool)

The MCP Tool acts as the decision engine of CampusPrep.

What it does

Analyzes the student’s resume

Evaluates interview request details

Decides the appropriate interview level

Decision Logic

YES (Qualified Resume) → Specific / Real Technical Interview

NO (Beginner / Incomplete Resume) → Basic Interview

This ensures:

Beginners are not overwhelmed

Advanced students receive industry-level challenges

🔄 Complete Workflow (Architecture-Based)
Student
→ Student Dashboard
→ Resume Upload
→ Interview Request
→ MCP Tool Decision
    ├── YES → Specific / Real Technical Interview
    └── NO  → Basic Interview
→ Interview Rounds
→ AI Evaluation
→ Result PDF Generated
→ Secure Storage
→ Linked to All Dashboards

📊 Dashboards
Student Dashboard

Request status

Interview history

Feedback & PDF reports

Alumni Dashboard

Student requests

Accept / Reject actions

Interview records

Admin Dashboard

Alumni verification

Request monitoring

Interview oversight

Central Dashboard

All roles are synced to a central system ensuring transparency and consistency.

☁️ Platform Services

Secure Storage: Firebase / Cloud Storage

Immutable Storage: Prevents result tampering

PDF Generation: Auto-generated interview reports

Dashboard Linking: PDFs visible to Student, Alumni, and Admin

🛠️ Tech Stack
Frontend

React (Vite)

Tailwind CSS

Firebase Authentication

Firebase Storage

Backend

Python (FastAPI)

Firebase Admin SDK

Gemini API (LLM)

REST APIs

AI Layer

Resume analysis

Interview question generation

Answer evaluation

MCP Tool decision engine

🔐 Security Practices

.env files excluded via .gitignore

Firebase service account keys are never committed

Backend secrets are not exposed to frontend

Interview results stored immutably

🎯 Expected Outcomes

Realistic interview preparation

Industry-aligned evaluation

Transparent and verifiable results

Scalable solution for colleges and training cells

🧪 Use Cases

College placement preparation

Training & Placement cells

Hackathons and tech fests

Individual interview practice

👨‍💻 Team

Team Name: BlockMinds

Team Leader:
Vivek N Patil

Team Members:

Mansvi Patel

Roshni Rajput

Khushi Dhamani

📜 License

This project is intended for educational, academic, and hackathon purposes.
Commercial usage requires proper authorization.
