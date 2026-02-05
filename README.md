# Habit Quest 🧠🎮

Habit Quest is a **production-style, containerized Flask application** designed and built as a **cloud / DevOps–focused portfolio project**.
It demonstrates how a modern web app is **designed, containerized, configured, and prepared for deployment** using real-world tooling and practices.

The project intentionally goes beyond CRUD by combining **gamification logic**, **stateful data**, and a **multi-container architecture** that mirrors how applications are deployed in cloud environments.

---

## 🚀 Why This Project (DevOps Perspective)

This project was built to showcase skills relevant to **Cloud / DevOps / Platform roles**, including:

* Designing a **12-factor style application**
* Running Flask behind **Gunicorn (WSGI)**
* Using **Nginx as a reverse proxy**
* Orchestrating services with **Docker Compose**
* Managing **environment-based configuration**
* Working with **stateful services (PostgreSQL)**
* Preparing the app for **CI/CD and EC2-style deployments**

This is not a tutorial app — it is structured like a **real deployable service**.

---

## 🧱 Architecture Overview

```
Client (Browser)
   ↓
Nginx (Reverse Proxy)
   ↓
Gunicorn (WSGI Server)
   ↓
Flask Application
   ↓
PostgreSQL Database
```

**Key architectural decisions:**

* Flask does **not** run with the development server in production
* Gunicorn handles application workers
* Nginx manages HTTP traffic and proxying
* PostgreSQL runs in its own container with persistent volumes

---

## 🐳 Containers & Services

| Service | Purpose                       |
| ------- | ----------------------------- |
| `web`   | Flask app served via Gunicorn |
| `nginx` | Reverse proxy & entry point   |
| `db`    | PostgreSQL database           |

All services are orchestrated using **Docker Compose**.

---

## 🎮 Application Features (Brief)

### Core

* Gamified habit tracking
* XP, levels, streaks, achievements
* Dark mode UI

### Authentication

* Secure login & registration
* Password hashing
* Session-based auth

### Data Layer

* PostgreSQL + SQLAlchemy ORM
* Relational models & constraints
* Migration-ready schema

---

## 🖼 Application Screenshots

The UI is fully responsive, supports dark mode, and is rendered using server-side templates (Jinja),
keeping the frontend lightweight while remaining production-friendly and easy to deploy.


### Dashboard (Light Mode)
![Dashboard Light](screenshots/dashboard-light.png)

### Dashboard (Dark Mode)
![Dashboard Dark](screenshots/dashboard-dark.png)

### Habits Page
![Habits](screenshots/habits.png)

### Achievements Page
![Achievements](screenshots/achievements.png)

### Authentication (Login & Register)
![Login](screenshots/login.png)
![Register](screenshots/register.png)

---

## ▶️ Running Locally (Docker)

### Prerequisites

* Docker
* Docker Compose

### Setup

```bash
git clone https://github.com/Shriniwas-Mudliyar/habit-quest.git
cd habit-quest
cp .env.example .env
```
### Start the Application

```bash
docker-compose up --build
```

The application will be available at:

* http://localhost (served via Nginx)
  
### Database Setup (First Run Only)

On first run, the database schema must be initialized manually.

This is a **one-time step per database volume** and applies to both:
- local development
- cloud deployments

See **Database Initialization (First Deployment Only)** in the  
[Cloud Deployment](#-cloud-deployment-aws-ec2) section for the full commands.

---

## ⚙️ Environment Configuration

Application configuration is handled entirely via environment variables,
following **12-factor app principles**.

A sample configuration file is provided:

```bash
.env.example
```
Create your runtime configuration before starting the application:
```bash
cp .env.example .env
```
Required Variables

DATABASE_URL – PostgreSQL connection string

SECRET_KEY – Flask secret key

FLASK_ENV – Application environment (development / production)

No secrets are hardcoded in the application or committed to the repository.

---

## 📦 Database

* PostgreSQL 16
* Persistent volume for data
* Relational schema with foreign keys

Seed data can be loaded for demo/testing purposes.

---

## ☁️ Cloud Deployment (AWS EC2)
Habit Quest is deployed and running on an AWS EC2 instance using a production-style, containerized architecture.

The EC2 instance is used strictly as a container host, with all application concerns (web server, WSGI server, database) handled inside Docker containers. This mirrors how modern cloud workloads are typically deployed.

### ▶️ Deploying on EC2
Clone the repository on the EC2 instance:
```bash
git clone https://github.com/Shriniwas-Mudliyar/habit-quest.git
cd habit-quest
```
Configure environment variables:
```bash
cp .env.example .env
```
Start the application:
```bash
docker-compose up -d --build
```
Nginx exposes the application publicly and routes traffic internally to Gunicorn and Flask.

## 🗄 Database Initialization (First Deployment Only)
On a fresh EC2 instance or new database volume, the database schema must be initialized manually.

This step is required only once per database volume.
```bash
docker-compose exec web bash

export FLASK_APP=app
export FLASK_ENV=development

rm -rf migrations
flask db init
flask db migrate -m "baseline schema"
flask db upgrade
```
Once completed, database state is persisted via Docker volumes and does not need to be repeated on restarts or redeployments.

### 🔄 Operational Notes

Application restarts do not affect persisted data

Containers can be safely restarted or rebuilt

All runtime behavior is controlled via environment variables

The setup is ready for future CI/CD automation

---

## 🔄 CI/CD (Planned)

The project is designed to support CI/CD and cloud deployment.

Planned additions:

* GitHub Actions CI
* Docker image build & validation
* EC2 deployment workflow
* Nginx + Gunicorn production tuning

---

## 🧠 Key Takeaway

Habit Quest demonstrates how to:

* Take a Flask app **from local development to production-style deployment**
* Structure a project with **real DevOps constraints in mind**
* Combine backend logic with infrastructure fundamentals

This repository is intentionally built as a **cloud-ready portfolio project**, not just a feature demo.



