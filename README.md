**WRITING BLOG WEB APPLICATION:**

This project is a writing blog platform built with flask where users can register  and publish
their posts or choose to be readers and enjoy content from various writers.The app handles user registration
and authentication using itsdangerous and allows writers to add,update and delete
posts.Users can comment and like posts depending on preference.

**FEATURES**

.User authentication with roles;
```bash
  users can signup,sign in and reset their password.
  ```
.The users can create,update and delete blog posts.

.Commenting and liking posts is also enabled.

.Users can get email notifications via flask-mail.

.Users can upload,update and delete their preferred profile pictures.

**Technologies**

1.Frontend:HTML,CSS

2.Backend:Python(Flask)

3.Database:MySQL

4.Authentication:Flask-login

**How to run the project:**

1.Open the terminal

2.Clone the Repository
```bash
git clone https://github.com/Carolkariuki/blog_app-repo.git
cd blog_app-repo
```
3.Create and activate a virtual environment;
```bash
   python -m venv venv
   source venv/bin/activate
   ```
4.Install dependancies;
```bash
   pip install -r requirements.txt
   ```
5.Set up an environmental variable by creating a .env file and configuring;
  ```bash 
 cp .env_sample .env 
  ```
6.Initialize the database;
```bash
  flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade
  ```
7.Run the application;
```bash
  flask run
  The app will run on **http://127.0.0.1:5000/** by default.
  ```






