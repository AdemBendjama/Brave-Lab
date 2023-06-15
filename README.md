

# Brave Lab

Welcome to Brave Lab! We are a blood laboratory that provides convenient and efficient services. We provide the option to book appointments online, while also having fast online payment integrations with PayPal. The results of our tests are accurate and are powered by Modern AI Technologies. Our mission is to deliver clean and timely results while utilizing advanced AI models for disease predictions, such as anemia and diabetes.

## Features

- **Appointment Booking**: Easily schedule appointments online.
- **Fast Online Payments**: Secure and hassle-free payment options, including PayPal integration.
- **Real-time Result Tracking**: Clients can track the progress of their test results in real-time.
- **Complaint System**: A built-in system for handling complaints, which automatically sends emails to relevant parties for resolution.
- **Accurate Results**: Trustworthy and precise blood test results.
- **Disease Predictions**: AI-powered models for predicting diseases like anemia and diabetes.
- **Simple Interface**: A user-friendly interface for managing all steps of testing and appointment management.
- **Profile Settings**: A basic interface for users to manage their profile settings, such as profile picture, email, and password.
- **Chat System**: Real-time communication between nurses and the chief medical supervisor (auditor) using AJAX for seamless interaction.
- **Search, Filter, and Sort**: Enhanced functionality to search, filter, and sort various lists within the application.
- **Nurse Account**: A dedicated account for nurses to manage clients in the lobby and input test results.
- **Receptionist Account**: An account for receptionists to handle appointment booking, client account creation, and payment and invoice management.
- **Auditor Account**: An account for the chief medical supervisor to access various statistics of the company, approve and sign test results, and handle complaints.
- **Admin Account**: An account with privileges for performing basic CRUD (Create, Read, Update, Delete) operations.

## Collaborators

- [Farouk Rahal](https://github.com/FaroukRahal)
- [Ahmed Amoukrane](https://github.com/zMARTVAL)

## Technologies Used

- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: Django
- Database: SQLite3
- AI/ML: Logistic Regression algorithms for anemia and diabetes prediction

## Getting Started

To get started with Brave Lab, follow these steps:

1. Clone the repository:
```
git clone git@github.com:AdemBendjama/Brave-Lab.git
```
2. Install the required dependencies: 
```
pip install Django joblib numpy scipy pytz setuptools tzdata wheel pandas scikit-learn xhtml2pdf django
```
3. Configure the environment:
   - For Visual Studio Code: Open the cloned folder in Visual Studio Code, set up your virtual environment, install recommended extensions, and configure environment-specific settings.
   - For PyCharm: Open the project in PyCharm, set up your virtual environment, and configure environment-specific settings.
4. Run the application using 
```
python manage.py runserver 
```
or
```
py manage.py runserver
```
5. Visit `http://localhost:8000` in your browser to access Brave Lab.

> **Note**: In order to use the email functionality, make sure to define the `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` variables in the `settings.py` file with the appropriate values for your email host and password.

## Screenshots

### Homepage

![Homepage](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/493fbec5-dad3-4078-a915-492d403fb519)

### Manage Profile

![Profile](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/e56e704b-c7bf-45c7-8f0b-6149fa1b7d3e)

### Client Book Appointment

![Book](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/27317e03-7035-46cc-b6bf-febb78202ce7)

### Client Test Results

![CResults](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/981f508f-4672-45b6-ad1f-3f91c3178ff9)

### Client Online Payment With PayPal

![Paypal01](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/f4bf3614-0000-430f-9389-89390843e0a9)

### Nurse Fill Test Values

![FillTest](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/e4bd7b74-4a64-4cff-b9c9-8d54e230c0c5)

### Nurse Chat

![NChat](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/f2808f4b-0189-4799-b1dc-c1041abcefa2)

###  Auditor Chat Rooms

![ChatRooms](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/cbc4b048-5300-44ae-9edd-cf2a41e40a4c)

###  Auditor Chat

![AChat](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/0f85e827-271b-4c4b-b083-597b9f69ff4c)

### Auditor Stats

![Stats](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/182496cd-8d96-4d78-9f00-4504f61edf20)

### Admin Interface

![Admin](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/82869da1-c0de-4d8c-a008-d676cb9624a0)

### Invoice

![InvoicePDF](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/4fbdb821-1128-4a50-a6db-070dca44ef98)

### Test Results and AI Prediction

![ResultsPDF](https://github.com/AdemBendjama/Brave-Lab/assets/93732841/8dd0db57-0fb2-4d73-8ed5-6a2994a81158)

## Future Work

Here are the several areas i could work on to improve the site's functionality, security and Code readability:

- Enhancing the security of the payment integration with PayPal to ensure the safety of user transactions.
- Hosting the website with Https and SSLTLS and a custom domain.
- Conducting code reviews and optimizing the codebase to improve efficiency and maintainability.
- Adding comprehensive documentation to guide users and developers in understanding the system.
- Organizing files and folders to enhance the project's structure and maintain a clean codebase.
- Adding more styles and visual enhancements to improve the overall user experience.
- Investigating the possibility of integrating face recognition and OCR (Optical Character Recognition) AI models for advanced functionality.
- Changing the current database Sqlite3 into a more secure and robust database management system like PostgreSQL or MySQL.

We are committed to continuously improving Brave Lab and providing an exceptional user experience. Stay tuned for updates and new features!

## Contact

If you have any questions or inquiries, feel free to contact me at adembendjama22@gmail.com.
