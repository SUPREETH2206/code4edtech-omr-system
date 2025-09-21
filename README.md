Automated OMR Evaluation & Scoring System
Submission for the Code4Edtech Challenge by Innomatics Research Labs

This project is a scalable, automated OMR evaluation system designed to solve the challenges of manual OMR sheet grading. It provides fast, accurate, and auditable results through a user-friendly web interface, reducing evaluation turnaround from days to minutes.

Live Application Demo
You can access and test the live web application here:

https://code4edtech-omr-system-bbfsekhiperc5tcysyfkee.streamlit.app/

1. Problem Statement
Educational institutions and assessment centers like Innomatics Research Labs process thousands of OMR sheets, which is a time-consuming, error-prone, and resource-intensive task. The manual process delays feedback to students, which is critical for their learning and placement preparation.

This project aims to build an automated system that:

Accurately evaluates OMR sheets from images captured via mobile phone.

Provides per-subject and total scores.

Handles multiple exam versions (sets).

Maintains a secure and exportable audit log of all evaluations.

2. Our Approach & Features
We have built a complete web application using Streamlit and OpenCV that serves as a robust Minimum Viable Product (MVP) to solve the core problem.

Key Features:

Dual Input Methods: Supports both batch uploading of multiple OMR sheets (PNG, JPG, PDF) and live scanning via a webcam or phone camera.

Automated Evaluation Pipeline: The backend, powered by OpenCV, preprocesses the image to correct for distortions and accurately detects marked bubbles.

Multi-Version Support: Easily handles different question paper sets (e.g., SET-A, SET-B) by matching against the correct pre-loaded answer key.

Comprehensive Audit Trail: Every evaluation is logged in a persistent SQLite database. The system saves processed images, visual overlays of the results, and a detailed JSON file for full transparency and review.

Interactive Dashboard: The application includes a dashboard to view the audit log, filter results, and get quick analytical insights (like average scores).

Data Export: All evaluation data can be easily exported to CSV or Excel for further analysis or reporting.

3. Tech Stack
Language: Python

Web Framework: Streamlit

Computer Vision: OpenCV, Pillow

Data Handling: Pandas, NumPy

Database: SQLite

4. Installation and Local Setup
To run this project on your local machine, please follow these steps:

Prerequisites:

Python 3.8+ installed

Git installed

Steps:

Clone the repository:

git clone [https://github.com/SUPREETH2206/code4edtech-omr-system.git](https://github.com/SUPREETH2206/code4edtech-omr-system.git)
cd code4edtech-omr-system

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required libraries:

pip install -r requirements.txt

Run the Streamlit application:

streamlit run app.py

The application will open in your default web browser.

5. How to Use the Application
Select Exam Set: In the sidebar, choose the appropriate exam version (e.g., SET-A).

Choose Input Method:

Select "File Uploader" to drag and drop one or more image files of OMR sheets.

Select "Live Camera Scan" to use your computer's webcam to capture an image.

Start Evaluation: Click the "✨ Start Evaluation" button to begin processing.

View Results: The application will display the processing status and show a visual overlay of the most recently scanned sheet.

Audit & Export: Scroll down to the "Audit Log & Analytics" section to view a table of all evaluations, search for specific records, or download the entire log as a CSV/Excel file.

Project Author:

Supreeth Theru
