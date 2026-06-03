# School Management System (SMS) API

An advanced, secure backend REST API developed with **Django 6.0**, **Django REST Framework (DRF)**, and **drf-spectacular**.

This application bridges a local authentication system with an existing remote **Supabase PostgreSQL** instance. It implements strict role-based access control (Admin, Teacher, Student) alongside an automated console-logged email notification system triggering on major business actions.

---

## Key Features

### Role-Based Access Control & Security
* **Admin:** Full CRUD access to all models. The only role authorized to provision new user credentials.
* **Teacher:** Filtered access to view assigned courses and profiles of students enrolled in their classes. Authorized to manage registrations exclusively for their own courses. Personal info editable (except email address).
* **Student:** Read-only access to their own profile and active course enrollments. PROFILE update capabilities are strictly hard-locked to Name and Password changes to preserve administrative data integrity (ID, Email, Category, Sex, WSH, DCA fields are completely immutable).

### Automated Email Notifications (Dev Console)
* **Account Provisioning:** Sends credentials immediately upon User creation.
* **Course Registration:** Sends a dual confirmation to the registered Student and the corresponding Course's Teacher.
* **Course Unregistration:** Alerts both the Student and Teacher instantly if a student is pulled from a course.
* **Course Assignment:** Triggers a notification to a specific Teacher when an Admin assigns them to lead a course.

---

## Installation & Setup Guide

Follow these steps to deploy and run the project locally on any operating system.

### 1. Prerequisites
Ensure you have **Python 3.12+** installed on your host system or setup your pre-configured **Vagrant** environment.

### 2. Clone the Repository & Environment Setup
```bash
# Clone the repository
git clone https://github.com/ShahJahan-del/profiles-rest-api.git
cd student_management_project

---

## Local Development Setup (Vagrant Environment)

Follow these exact steps to boot up the virtual development machine and launch the local server.

### 1. Initialization & Booting the VM
1. Open **Oracle VirtualBox** and **Git Bash**.
   *(Note: If the virtual machine is already suspended or unstable, double-click it, exit, and choose "Power off the machine").*
2. Navigate to the local project folder:
   ```bash
   cd /profiles-rest-api
Boot up the Vagrant environment:

Bash
vagrant up
Access the virtual machine secure shell:

Bash
vagrant ssh
Move into the synchronized shared project directory:

Bash
cd /vagrant

Vagrant Connection Troubleshooting
If the vagrant ssh connection times out or refuses to connect, attempt these fallback operational workflows sequentially:

Turn off the VM completely inside the Oracle VirtualBox GUI, then execute vagrant up and vagrant ssh again.

Run a clean reload sequence: vagrant halt ➔ vagrant reload ➔ vagrant ssh.

Force allocate a pseudo-terminal: vagrant ssh -- -t.

Establish a direct raw SSH bypass link using the private key path:

Bash
ssh vagrant@127.0.0.1 -p 2222 -i .vagrant/machines/default/virtualbox/private_key

### 2. Launching the Django Server
Once connected inside the Vagrant container shell, activate your Python workspace dependencies:

Bash
#Move to the project folder
cd /vagrant/student_management_project

Bash
# Activate the isolated Python environment
source ~/env/bin/activate

# Launch the development server binding (Ignore development warnings)
python manage.py runserver 0.0.0.0:8000
To leave the virtual workspace environment later, simply execute: deactivate

API Documentation & Swagger Interface
The project features a fully dynamic OpenAPI 3 implementation allowing downstream frontend engineering squads or evaluators to interactively discover routes, review expected JSON payloads, and test live responses.

Interactive Swagger UI Endpoint: http://127.0.0.1:8000/api/docs/
