# AI Resume & Cover Letter Generator

A Streamlit-powered web application that generates **professional, ATS-friendly resumes and cover letters** using AI. Users can input their profile, paste a job description, and instantly receive tailored documents — all downloadable as PDFs.

 Perfect for job seekers who want to save time and apply smart functional systems to their advantage.


## CONTRIBUTORS
- **Ocheni Glory**
- **Ibiam Uchenna**
- **Awwal Abba**
- **Ismail Muhammad**


## Features

- **AI-Powered Generation**: Uses [Together AI](https://together.ai) (Llama 3) to generate the resume and cover letter
- **PDF Export**: Download resumes and cover letters as clean, professional PDFs
- **Job Application Tracker**: Saves and monitors your applications 
- **ATS Optimization**: Documents are formatted to pass Applicant Tracking Systems this is done by the utilization of key words from the job description
- **User-Friendly Interface**: Built with Streamlit for a smooth experience

## Technologies Used

- **Streamlit** – Web interface
- **Together AI** – LLM for resume/cover letter generation
- **ReportLab** – This handles the whole PDF creation process 
- **JSON** – Local data storage which stores data in dictionary format
- **dotenv** – Secure API key management, for concealing too and calling the API KEY

## Project Structure

- AI_Generated_Resume/
- │
- ├── main.py # Main Streamlit app(The main entry point of the code)
- ├── requirements.txt # Python requirements
- ├── README.md # This file you are reading right now
- │
- ├── generator/
- │ ├── data_manager.py # Saves user profile & applications. 
- │ ├── ai_generator.py # AI content generation
- │ └── pdf_generator.py # Creates PDFs
- │
- ├── data/
- │ ├── user_profiles.json # Saves the users data
- │ └── job_applications.json # Saves the applications

