# CodeAlpha_SocialMedia

A mini social media platform built with Python, Django, HTML, CSS, and JavaScript for the CodeAlpha Full Stack Development Internship (Task 2).

## Features
- User authentication & profiles (via Django Auth & Profile model)
- Create and view posts in a chronological feed
- Like / unlike posts with live like counts
- Comment on posts
- Follow / unfollow other users

## Setup & Run Locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```
