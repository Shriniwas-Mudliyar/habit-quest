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
* Implementing CI/CD with GitHub Actions for automated EC2 deployment

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
### ⚡ DevOps Highlights

This project demonstrates real-world DevOps practices:

- Containerized multi-service architecture
- Reverse proxy setup using Nginx
- Production-ready Gunicorn configuration
- Automated database migrations during startup
- Environment-based configuration management
- Persistent storage using Docker volumes
- CI/CD pipeline using GitHub Actions
- Cloud deployment on AWS EC2
- Stateless application design with externalized state

### Deployment & Automation Flow

```
Developer Push (GitHub)
↓
GitHub Actions (CI/CD)
↓
Secure SSH to EC2
↓
Docker Compose Build & Restart
↓
Live Application Update
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

### Authentication
![Login](screenshots/login.png)

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
docker compose up --build
```

The application will be available at:

* http://localhost (served via Nginx)
  
### Database Setup

Database migrations run automatically when the application starts.

The container entrypoint waits for PostgreSQL to become available and executes:

```
flask db upgrade
```
This ensures the database schema is always up to date without requiring any manual intervention.

This approach mirrors production deployment practices where services self-initialize during startup.

---

## ⚙️ Environment Configuration

Application configuration is handled entirely via environment variables,
following **12-factor app principles**.

A sample configuration file is provided:

```bash
.env.example
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
Habit Quest is deployed on AWS EC2 using an automated CI/CD pipeline powered by GitHub Actions.

GitHub Actions is used to automate deployment to the EC2 instance.

The workflow securely connects via SSH, pulls the latest code, rebuilds Docker images, and restarts services using Docker Compose.

Habit Quest is deployed and running on an AWS EC2 instance using a production-style, containerized architecture.

The EC2 instance is used strictly as a container host, with all application concerns (web server, WSGI server, database) handled inside Docker containers. This mirrors how modern cloud workloads are typically deployed.

### ▶️ Initial EC2 Setup (One-Time)
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
docker compose up -d --build
```
After this initial setup, all future deployments are handled automatically via GitHub Actions.

Nginx exposes the application publicly and routes traffic internally to Gunicorn and Flask.

### 🗄 Database Initialization

Database migrations are applied automatically during container startup using Flask-Migrate.

This ensures:

• consistent schema across environments  
• zero manual setup on new deployments  
• production-safe initialization  

Persistent Docker volumes ensure data is retained across restarts and redeployments.

### 🔄 Operational Notes

Application restarts do not affect persisted data

Containers can be safely restarted or rebuilt

All runtime behavior is controlled via environment variables

The setup supports automated and repeatable deployments using CI/CD

### 🧯 Infrastructure Lifecycle Note

The EC2 instance used for deployment is intentionally terminated when not in use to avoid unnecessary cloud costs.

The CI/CD pipeline remains fully functional, and deployment can be re-enabled at any time by launching a new EC2 instance and manually triggering the GitHub Actions deployment workflow.


---

## 🔄 CI/CD (GitHub Actions)

This project includes a GitHub Actions–based CI/CD pipeline

### Continuous Integration (CI)
- Triggered automatically on every push to `main`
- Builds the Docker image to validate the application and Docker configuration
- Ensures the project remains deployable at all times

### Continuous Deployment (CD)
- Deployment to AWS EC2 is **manual**
- Triggered via `workflow_dispatch` in GitHub Actions
- Prevents failed deployments when the EC2 instance is intentionally stopped or terminated

This approach reflects real-world DevOps practices where deployment is often a controlled action rather than automatic on every commit.


### Why This Matters
- No manual SSH deployments
- Consistent, repeatable releases
- Production-style DevOps workflow
- Mirrors real-world CI/CD pipelines used in cloud teams


---

## 🧠 Key Takeaway

Habit Quest demonstrates the complete lifecycle of a modern cloud-deployed application:

• Application development using Flask  
• Containerization using Docker  
• Service orchestration using Docker Compose  
• Production-grade serving using Gunicorn and Nginx  
• Persistent database management using PostgreSQL  
• Automated CI/CD using GitHub Actions  
• Cloud deployment on AWS EC2  

This project reflects how real production systems are built, deployed, and managed.









