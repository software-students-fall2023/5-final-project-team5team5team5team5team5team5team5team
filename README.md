# Recipie Finder App

## Coverage Note

```
Coverage report
Name                  Stmts   Miss  Cover
-----------------------------------------
tests/test_app.py .......                                                [ 50%]
web_app/tests/test_fetch_spoon.py ..                                     [ 64%]
web_app/tests/test_recipe.py ..                                          [ 78%]
web_app/tests/test_signup_and_login.py ...                               [100%]
```

For the web-app, this is the coverage report

```
Name                  Stmts   Miss  Cover
-----------------------------------------
web_app/__init__.py       0      0   100%
web_app/app.py          132     27    80%
-----------------------------------------
TOTAL                   132     27    80%
```

## What Does The App Do?

Our containerized app helps users find recipies catered to their preferences.  Users can login and submit ingredients they are allergic to and what ingredients they have.  Our app will then show the users recipies and dishes that match the specified requirements.

## How To Run?

### Method 1: Cloning the Github

1. Using Git Bash, clone the directory using:

```
git clone https://github.com/software-students-fall2023/5-final-project-team5team5team5team5team5team5team5team
```

2. Open Docker Desktop

3. Open command prompt (accessible through windows search)

4. Go to the directory where you cloned the repository with:
```
cd "path_to_directory"
```

5. You should be in the root directory. Now, do:
```
docker-compose build
docker-compose up
```

6. Open a web browser and go to: http://localhost:5000/

You should now see tha app running.

### Method 2: Access the website

To try the application directly through this url: http://134.209.168.140:5000/

## Contributors

- [BradFeng02](https://github.com/BradFeng02)
- [IvanJing](https://github.com/IvanJing)
- [FrozenEclipse](https://github.com/FrozenEclipse)
- [jeffreysaeteros](https://github.com/jeffreysaeteros)


