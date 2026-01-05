====== Steps to run my program on the local server:
Open a Terminal
In PyCharm: Click View → Tool Windows → Terminal (or press Alt+F12)
Navigate to Your Project
bash
cd C:\Users\TechiesRobotics\PycharmProjects\adc
Install Required Packages
bash
pip install -r requirements.txt
Run the Flask Application
bash
python app.py
Access the Game Open your web browser and go to:
http://127.0.0.1:5000/


==== steps to deploy my application to pythonAnyWhere server:

## Deploying to PythonAnywhere

This project can be deployed to PythonAnywhere so it can run online instead of only on a local computer.

### Prerequisites
- A PythonAnywhere account
- This repository pushed to GitHub

---

### Step 1: Open a Bash console on PythonAnywhere
1. Log in to PythonAnywhere
2. Go to **Dashboard → Consoles**
3. Under **Other**, click **Bash**

---

### Step 2: Clone the repository
In the Bash console, run:

```bash
git clone https://github.com/leoleoleo11912/hangman.git
cd hangman
Step 3: Create and activate a virtual environment

In the Bash console, run:

python3.10 -m venv venv
source venv/bin/activate


You should see (venv) in the terminal prompt.

Step 4: Install dependencies

In the Bash console, run:

pip install flask


(Optional but recommended)

pip freeze > requirements.txt

Step 5: Create a web app

Go to Dashboard → Web

Click Add a new web app

Choose:

Manual configuration

Python 3.10

Step 6: Set the virtual environment path

Stay on the Web tab

Find Virtualenv

Enter the following path:

/home/YOUR_USERNAME/hangman/venv


Replace YOUR_USERNAME with your PythonAnywhere username.

Step 7: Configure the WSGI file

On the Web tab, click WSGI configuration file

Delete everything in the file

Paste the following code:

import sys

path = '/home/YOUR_USERNAME/hangman'
if path not in sys.path:
    sys.path.append(path)

from app import app as application


Save the file

Step 8: Reload and run the app

Go back to the Web tab

Click Reload

Open the following URL in your browser:

https://YOUR_USERNAME.pythonanywhere.com
