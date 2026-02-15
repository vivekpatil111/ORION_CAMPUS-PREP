# 🚀 CampusPrep — From Campus to Career

CampusPrep is an AI-powered interview preparation platform designed to bridge the gap between academic learning and real-world industry expectations.

The platform follows a structured Student → Alumni → Admin → Platform Services workflow, powered by an intelligent MCP Tool (Model Control & Processing Tool) that dynamically decides interview complexity based on student readiness.

---

## 🧠 Problem Statement

Many students enter placements without real interview exposure, industry-relevant feedback, or structured evaluation.  
Traditional mock interviews are limited, biased, and not scalable.

---

## 🎯 Solution Overview

CampusPrep provides:
- AI-driven mock interviews  
- Resume-based interview routing using MCP Tool  
- Alumni involvement for real-world validation  
- Admin-level monitoring and control  
- Secure, immutable interview results in PDF format  

---

## 🧩 System Roles

### 🧑‍🎓 Student
- Upload resume  
- Request interview  
- Attend interview rounds (voice / video / AI)  
- View feedback and result PDF  

### 🎓 Alumni
- View student interview requests  
- Accept or reject requests  
- Validate interview flow with industry perspective  

### 🛡️ Admin
- Verify alumni  
- Monitor interview requests  
- Oversee interview quality and fairness  

---

## 🧠 MCP Tool (Model Control & Processing Tool)

The MCP Tool acts as the decision engine of CampusPrep.

### Responsibilities
- Analyze student resumes  
- Evaluate interview request details  
- Decide the appropriate interview level  

### Decision Logic
- YES (Qualified Resume) → Specific / Real Technical Interview  
- NO (Beginner / Incomplete Resume) → Basic Interview  

This ensures fair, adaptive, and student-friendly interview experiences.

---

## 🔄 Complete Workflow

Student  
→ Student Dashboard  
→ Resume Upload  
→ Interview Request  
→ MCP Tool Decision  
→ Interview Rounds  
→ AI Evaluation  
→ Result PDF Generated  
→ Secure Storage  
→ Linked to All Dashboards  

---

## 📊 Dashboards

### Student Dashboard
- Interview request status  
- Interview history  
- Feedback and PDF reports  

### Alumni Dashboard
- Student interview requests  
- Accept / Reject actions  
- Interview records  

### Admin Dashboard
- Alumni verification  
- Request monitoring  
- Interview oversight  

All dashboards are synced to a central system ensuring transparency and consistency.

---

## ☁️ Platform Services

- Secure Storage (Firebase / Cloud Storage)  
- Immutable Storage to prevent tampering  
- Auto-generated interview result PDFs  
- Dashboard-linked results  

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)  
- Tailwind CSS  
- Firebase Authentication  
- Firebase Storage  

### Backend
- Python (FastAPI)  
- Firebase Admin SDK  
- Gemini API (LLM)  
- REST APIs  

### AI Layer
- Resume analysis  
- Interview question generation  
- Answer evaluation  
- MCP Tool decision engine  

---

## 🔐 Security Practices

- Environment files excluded via .gitignore  
- Firebase service account keys are never committed  
- Backend secrets are not exposed to frontend  
- Interview results stored immutably  

---

## 🎯 Expected Outcomes

- Realistic interview preparation  
- Industry-aligned evaluation  
- Transparent and verifiable results  
- Scalable solution for colleges and training cells  

---

## 🧪 Use Cases

- College placement preparation  
- Training & Placement cells  
- Hackathons and tech fests  
- Individual interview practice  

---

## 👨‍💻 Team

**Team Name:** BlockMinds  

**Team Leader:**  
Vivek N Patil
Team Member 1 : Roshni Rajput 
Team Member 2 : Khushi Dhamani 
Team Member 3 : Mansvi Patel

---

## 📜 License

This project is intended for educational, academic, and hackathon purposes.  
Commercial usage requires proper authorization.

---

## 

CampusPrep leverages AI, alumni validation, and an intelligent MCP decision engine to deliver secure, scalable, and industry-ready interview preparation for students.
