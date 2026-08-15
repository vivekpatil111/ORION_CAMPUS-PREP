# 🚀 CampusPrep — From Campus to Career

**CampusPrep** is an AI-powered interview preparation platform that gives students realistic, voice-driven mock interviews — evaluated by AI, validated by real alumni, and monitored by admins — so they walk into placements with actual practice, not guesswork.

> Think of it as a **flight simulator for job interviews**: students practice real, spoken interview rounds with an AI agent that listens, responds, adapts its difficulty to their resume, and gives them a verifiable result — all before they ever face a real recruiter.

[

![Live Demo](https://img.shields.io/badge/Live%20Demo-campus--prep.vercel.app-brightgreen?style=for-the-badge)

](https://campus-prep.vercel.app/)
[

![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)

](https://github.com/vivekpatil111/ORION_CAMPUS-PREP)

🔗 **Live App:** [https://campus-prep.vercel.app/](https://campus-prep.vercel.app/)
🔗 **Source Code:** [https://github.com/vivekpatil111/ORION_CAMPUS-PREP](https://github.com/vivekpatil111/ORION_CAMPUS-PREP)

---

## 📌 Table of Contents
- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [How It Works (At a Glance)](#-how-it-works-at-a-glance)
- [Voice AI System](#️-voice-ai-system)
- [System Roles](#-system-roles)
- [MCP Agent Harness](#-mcp-tool-model-control--processing-tool--agent-harness)
- [Complete Workflow](#-complete-workflow)
- [Dashboards](#-dashboards)
- [Platform Services](#️-platform-services)
- [Tech Stack](#️-tech-stack)
- [Security Practices](#-security-practices)
- [Expected Outcomes](#-expected-outcomes)
- [Use Cases](#-use-cases)
- [Team](#-team)
- [License](#-license)

---

## 🧠 Problem Statement

Most students enter campus placements without real interview exposure, industry-relevant feedback, or structured evaluation. Traditional mock interviews are:

- **Limited** — only a handful of seniors/faculty can conduct them
- **Biased** — feedback quality depends entirely on who's interviewing
- **Not scalable** — a college of 5,000 students can't get everyone real practice

CampusPrep solves this by replacing scarce human bandwidth with an **AI interviewer that's always available, consistent, and adaptive** — while still keeping real alumni in the loop for authenticity.

---

## 🎯 Solution Overview

CampusPrep provides:

- 🎙️ **AI-driven mock interviews** conducted through real-time voice conversation, not just text forms
- 🧭 **Resume-based interview routing** — the AI decides how hard your interview should be based on how prepared you actually are
- 🎓 **Alumni involvement** for real-world validation of the interview process
- 🛡️ **Admin-level monitoring** for quality and fairness
- 📄 **Secure, immutable interview results** delivered as tamper-proof PDF reports

---

## ⚡ How It Works (At a Glance)

```
1. Student uploads resume
        ↓
2. AI agent (MCP) reads it and decides interview difficulty
        ↓
3. Student takes a LIVE VOICE interview with the AI
   (AI speaks questions → student answers by talking → AI listens, responds, adapts)
        ↓
4. AI evaluates the answers
        ↓
5. A secure, downloadable result PDF is generated
        ↓
6. Alumni can review and validate the process
        ↓
7. Admin oversees the whole system for fairness
```

That's the entire product in one loop — **no forms to fill mid-interview, no typing answers. You just talk, like a real interview.**

👉 **Try it live:** [campus-prep.vercel.app](https://campus-prep.vercel.app/)

---

## 🎙️ Voice AI System

This is the core of what makes CampusPrep feel like a *real* interview instead of a quiz.

### Speech Pipeline
- **Speech-to-Text (STT):** Converts the candidate's spoken answers into text in real time, using the Web Speech API
- **Text-to-Speech (TTS):** The AI interviewer *speaks* its questions and feedback out loud, using the Web Speech API
- Built for **low latency**, so the back-and-forth feels like a natural conversation, not a call-and-wait system

### Guardrails & Reliability
Real conversations are messy — people pause, get cut off, or mumble. CampusPrep's voice agent is built to handle that:

- **Interruption handling** — if the candidate starts speaking while the AI is still talking, the AI's speech is immediately cancelled, just like a real interviewer would stop and listen
- **Low-confidence / silence re-prompting** — if the AI isn't confident about what it heard (or heard nothing at all), it doesn't fail silently — it politely asks the candidate to repeat themselves
- Manually tested against unpredictable, real-world speech patterns to make the experience feel dependable rather than robotic

---

## 🧩 System Roles

### 🧑‍🎓 Student
- Upload resume
- Request an interview
- Attend live interview rounds (voice / video / AI)
- View feedback and download the result PDF

### 🎓 Alumni
- View incoming student interview requests
- Accept or reject requests to conduct/validate interviews
- Bring an industry perspective to the interview flow

### 🛡️ Admin
- Verify alumni accounts
- Monitor all interview requests across the platform
- Oversee interview quality and fairness system-wide

---

## 🧠 MCP Tool (Model Control & Processing Tool) — Agent Harness

The MCP Tool is the **decision engine and agent harness** of CampusPrep — the layer that makes the AI act intelligently instead of asking the same generic questions to everyone.

### What it does
- Analyzes the student's uploaded resume
- Evaluates the interview request details
- Decides, in real time, what level of interview the student is ready for

### Decision Logic

| Resume Quality | Interview Type Assigned |
|---|---|
| ✅ Qualified / Strong Resume | Specific, real technical interview |
| ⚠️ Beginner / Incomplete Resume | Basic, foundational interview |

This means a final-year student with strong projects and a first-year student exploring their first internship **get genuinely different interviews** — fair to both, useful to both.

---

## 🔄 Complete Workflow

```
Student
   ↓
Student Dashboard
   ↓
Resume Upload
   ↓
Interview Request
   ↓
MCP Agent Decision (routes difficulty)
   ↓
Live Voice Interview Round
   (STT: candidate speaks → LLM: AI reasons & responds → TTS: AI speaks back)
   ↓
AI Evaluation of Answers
   ↓
Result PDF Generated (secure & immutable)
   ↓
Linked to Student, Alumni & Admin Dashboards
```

---

## 📊 Dashboards

### 🧑‍🎓 Student Dashboard
- Live interview request status
- Full interview history
- Feedback + downloadable PDF reports

### 🎓 Alumni Dashboard
- Incoming student interview requests
- Accept / reject controls
- Access to past interview records

### 🛡️ Admin Dashboard
- Alumni verification queue
- Platform-wide request monitoring
- Interview quality oversight

All three dashboards are synced to a central system in real time — what a student sees, alumni and admins see reflected instantly too.

---

## ☁️ Platform Services

- **Secure Storage** — Firebase / Google Cloud Platform backed
- **Immutable Storage** — interview results can't be tampered with after generation
- **Auto-generated PDFs** — every interview produces a verifiable result document
- **Dashboard-linked results** — nothing lives in isolation; every result is traceable across roles

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React (Vite), Tailwind CSS, Firebase Authentication, Firebase Storage |
| **Voice AI** | Web Speech API (Speech-to-Text + Text-to-Speech) |
| **Backend** | Python, FastAPI, Firebase Admin SDK, REST APIs |
| **AI / LLM** | Gemini API, MCP-based agent decision engine |
| **Cloud & Deployment** | Google Cloud Platform (via Firebase), Vercel — [Live App](https://campus-prep.vercel.app/) |

---

## 🔐 Security Practices

- Environment files excluded via `.gitignore`
- Firebase service account keys are never committed to the repo
- Backend secrets are never exposed to the frontend
- Interview results are stored immutably to prevent post-hoc tampering

---

## 🎯 Expected Outcomes

- Realistic, voice-driven interview practice — not just another quiz app
- Industry-aligned, resume-adaptive evaluation
- Transparent, verifiable results students can actually trust
- A scalable solution colleges and training & placement cells can deploy campus-wide

---

## 🧪 Use Cases

- 🎓 College placement preparation
- 🏢 Training & Placement (T&P) cell adoption
- 🏆 Hackathons and tech fest demonstrations
- 🙋 Individual, self-driven interview practice

---

## 📜 License

This project is intended for educational, academic, and hackathon purposes. Commercial usage requires proper authorization.

---

<p align="center">
<b>CampusPrep</b> — where students don't just prepare for interviews, they practice them, out loud, with an AI that actually listens.
<br><br>
🔗 <a href="https://campus-prep.vercel.app/">Live Demo</a> &nbsp;|&nbsp; 🔗 <a href="https://github.com/vivekpatil111/ORION_CAMPUS-PREP">GitHub Repo</a>
</p>