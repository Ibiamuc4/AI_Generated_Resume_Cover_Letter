#!/usr/bin/env python3
"""
AI-Based Resume & Cover Letter Generator
Main Streamlit Application with Full AI Integration and PDF Download
"""

import streamlit as st
import json
from datetime import datetime
from generator.data_manager import DataManager
from generator.ai_generator import AIGenerator
from generator.pdf_generator import PDFCreator  

# Initialize components (These are the main classes from data_manager.py and ai_generator.py)
dm = DataManager()
ai_gen = AIGenerator()


def main():
    st.set_page_config(
        page_title="AI Resume & Cover Letter Generator",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state for navigation (What does the session state_funtion do)
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Sidebar navigation
    st.sidebar.title("🤖 AI Resume Generator")
    
    # Navigation options
    page_options = {
        "🏠 Home": "Home",
        "👤 User Profile": "Profile", 
        "📄 Generate Resume": "Resume",
        "📝 Write Cover Letter": "Cover Letter",
        "❓ Interview Questions": "Interview",
        "📊 Job Applications": "Applications"
    }
    
    # Sidebar navigation with proper state management
    st.sidebar.markdown("### Navigation")
    
    selected_option = st.sidebar.selectbox(
        "Choose a page:",
        list(page_options.keys()),
        index=list(page_options.values()).index(st.session_state.current_page) if st.session_state.current_page in page_options.values() else 0,
        key="main_navigation"
    )
    
    # Update current page based on selection
    new_page = page_options[selected_option]
    if new_page != st.session_state.current_page:
        st.session_state.current_page = new_page
        st.rerun()
    
    # Display the selected page
    if st.session_state.current_page == 'Home':
        show_home_page()
    elif st.session_state.current_page == 'Profile':
        show_user_profile_page()
    elif st.session_state.current_page == 'Resume':
        show_resume_generator_page()
    elif st.session_state.current_page == 'Cover Letter':
        show_cover_letter_page()
    elif st.session_state.current_page == 'Interview':
        show_interview_questions_page()
    elif st.session_state.current_page == 'Applications':
        show_job_applications_page()

def show_home_page():
    st.title("🤖 AI-Powered Resume & Cover Letter Generator")
    st.markdown("---")
    
    # Welcome message
    profile = dm.load_user_profile()
    if profile:
        st.success(f"👋 Welcome back, **{profile.get('name', 'User')}**!")
    else:
        st.info("👋 Welcome! Please create your profile to get started.")
    
    # Home page layout
    col1, col2 = st.columns([2, 1]) # This defines the ratio of the columns ([2, 1])
    
    with col1:
        st.markdown("""
        ### What This App Does:
        - 📝 **Smart Resume Generation**: Creates tailored resumes based on job descriptions
        - 💼 **Cover Letter Writing**: Generates personalized cover letters for specific positions
        - ❓ **Interview Preparation**: Suggests potential interview questions
        - 📊 **Application Tracking**: Keeps track of your job applications and their status
        - 🎯 **ATS Optimization**: Ensures your documents are ATS-friendly (Automated tracking system)
        """)
        
        st.markdown("""
        ### How It Works:
        1. **Create Your Profile** → Add your skills, experience, and education
        2. **Input Job Description** → Paste the job posting you're interested in  
        3. **Generate Documents** → AI creates tailored resume and cover letter
        4. **Download PDFs** → Get professional documents ready for submission
        5. **Track Applications** → Monitor your job search progress
        """)
    
    with col2:
        st.markdown("### 📊 Your Statistics")
        stats = dm.get_application_stats()
        
        st.metric("Total Applications", stats['total_applications'])
        st.metric("Pending Applications", stats['pending'])
        st.metric("Interviews Scheduled", stats['interview'])
        
        if stats['total_applications'] > 0:
            interview_rate = (stats['interview'] / stats['total_applications']) * 100
            st.metric("Interview Rate", f"{interview_rate:.1f}%")
    
    # Quick actions panel
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Create Resume", key="quick_resume", help="Generate a new resume"):
            st.session_state.current_page = 'Resume'
            st.rerun()
    
    with col2:
        if st.button("📝 Write Cover Letter", key="quick_cover", help="Create a cover letter"):
            st.session_state.current_page = 'Cover Letter'
            st.rerun()
    
    with col3:
        if st.button("📊 View Applications", key="quick_apps", help="See your job applications"):
            st.session_state.current_page = 'Applications'
            st.rerun()
    
    with col4:
        if st.button("❓ Practice Interview", key="quick_interview", help="Get interview questions"):
            st.session_state.current_page = 'Interview'
            st.rerun()

def show_user_profile_page():
    st.title("👤 User Profile")
    st.markdown("---")
    
    # Load existing profile
    profile = dm.load_user_profile()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Personal Information")
        with st.form("user_profile_form"):
            name = st.text_input("Full Name", value=profile.get('name', '') if profile else '')
            email = st.text_input("Email Address", value=profile.get('email', '') if profile else '')
            phone = st.text_input("Phone Number", value=profile.get('phone', '') if profile else '')
            location = st.text_input("Location (City, Country)", value=profile.get('location', '') if profile else '')
            
            st.markdown("### Professional Information")
            current_title = st.text_input("Current Job Title", value=profile.get('current_title', '') if profile else '')
            linkedin = st.text_input("LinkedIn Profile URL", value=profile.get('linkedin', '') if profile else '')
            
            st.markdown("### Skills & Experience")
            skills = st.text_area(
                "Technical Skills (comma-separated)", 
                value=profile.get('skills', '') if profile else '',
                help="e.g., Python, JavaScript, SQL, Project Management"
            )
            
            experience = st.text_area(
                "Work Experience Summary",
                value=profile.get('experience', '') if profile else '',
                help="Brief overview of your work experience",
                height=150
            )
            
            education = st.text_area(
                "Education",
                value=profile.get('education', '') if profile else '',
                help="Your educational background",
                height=100
            )
            
            submitted = st.form_submit_button("💾 Save Profile", type="primary")
            
            if submitted:
                if name and email:
                    profile_data = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'location': location,
                        'current_title': current_title,
                        'linkedin': linkedin,
                        'skills': skills,
                        'experience': experience,
                        'education': education,
                        'updated_at': datetime.now().isoformat()
                    }
                    
                    if dm.save_user_profile(profile_data):
                        st.success("✅ Profile saved successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Error saving profile. Please try again.")
                else:
                    st.error("❌ Please fill in at least Name and Email fields.")
    
    with col2:
        st.markdown("### 👤 Profile Summary")
        if profile:
            st.info(f"""
            **Name:** {profile.get('name', 'Not set')} 
            **Email:** {profile.get('email', 'Not set')} 
            **Location:** {profile.get('location', 'Not set')} 
            **Current Title:** {profile.get('current_title', 'Not set')} 
            **Skills:** {len(profile.get('skills', '').split(',')) if profile.get('skills') else 0} skills listed 
            **Last Updated:** {profile.get('updated_at', 'Never')[:10] if profile.get('updated_at') else 'Never'}
            """)
        else:
            st.warning("No profile created yet. Fill out the form to get started!")
        
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use specific, relevant skills for better AI generation
        - Include quantifiable achievements in experience
        - Keep information current and accurate
        - Add keywords from your target job descriptions
        """)


# This is the PDF download function
def create_pdf_download_button(content_text, user_profile, content_type="resume", filename_prefix="document"):
    """
    Create a download button for PDF generation
    """
    try:
        # Initialize PDF creator
        pdf_creator = PDFCreator()
        
        if content_type == "resume":
            # Generate resume PDF
            pdf_bytes = pdf_creator.create_resume_pdf(content_text, user_profile)
            filename = f"{filename_prefix}_resume.pdf"
            mime_type = "application/pdf"
            
        elif content_type == "cover_letter":
            # Generate cover letter PDF
            pdf_bytes = pdf_creator.create_cover_letter_pdf(content_text, user_profile)
            filename = f"{filename_prefix}_cover_letter.pdf"
            mime_type = "application/pdf"
        
        # Create download button
        st.download_button(
            label=f"📄 Download {content_type.replace('_', ' ').title()} as PDF",
            data=pdf_bytes,
            file_name=filename,
            mime=mime_type,
            key=f"download_{content_type}_{hash(content_text)}"  # Unique key
        )
        return True
        
    except Exception as e:
        st.error(f"Error creating PDF: {str(e)}")
        return False



def show_resume_generator_page():
    st.title("📄 AI Resume Generator")
    st.markdown("---")
    
    # Check if user has profile
    profile = dm.load_user_profile()
    if not profile:
        st.warning("⚠️ Please create your user profile first!")
        if st.button("Go to Profile Page"):
            st.session_state.navigate_to = 'Profile'
            st.rerun()
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Job Description Input")
        job_description = st.text_area(
            "Paste the job description here:",
            height=300,
            placeholder="Copy and paste the full job posting, including requirements, responsibilities, and qualifications..."
        )
        
        company_name = st.text_input("Company Name (optional)", placeholder="e.g., Google, Microsoft, Startup Inc.")
        position_title = st.text_input("Position Title", placeholder="e.g., Senior Python Developer")
        
        if st.button("🤖 Generate Resume", type="primary", disabled=not job_description):
            if job_description.strip():
                with st.spinner("🔄 AI is crafting your tailored resume..."):
                    try:
                        resume_text = ai_gen.generate_resume(profile, job_description)
                        
                        if resume_text:
                            st.session_state.generated_resume = resume_text
                            st.session_state.resume_job_desc = job_description
                            st.session_state.resume_company = company_name
                            st.session_state.resume_position = position_title
                            
                            # Save application record
                            app_data = {
                                'company_name': company_name or 'Unknown Company',
                                'position_title': position_title or 'Unknown Position',
                                'application_date': datetime.now().isoformat(),
                                'status': 'pending',
                                'job_description': job_description[:500] + '...' if len(job_description) > 500 else job_description,
                                'documents_generated': ['resume']
                            }
                            dm.save_job_application(app_data)
                            
                            st.success("✅ Resume generated successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to generate resume. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating resume: {str(e)}")
            else:
                st.warning("Please enter a job description first!")
    
    with col2:
        st.markdown("### 📝 Generated Resume")
        
        if 'generated_resume' in st.session_state:
            st.markdown("#### Preview:")
            st.text_area(
                "Your AI-Generated Resume:",
                value=st.session_state.generated_resume,
                height=300,
                help="Copy this text to your preferred document editor"
            )
            
            # NEW: PDF Download Section
            st.markdown("#### 📄 Download Options:")
            col_a, col_b = st.columns(2)
            
            with col_a:
                # PDF Download Button - NEW FEATURE!
                filename_prefix = profile.get('name', 'resume').replace(' ', '_')
                if create_pdf_download_button(
                    st.session_state.generated_resume,
                    profile,
                    content_type="resume",
                    filename_prefix=filename_prefix
                ):
                    st.success("✅ PDF ready for download!")
            
            with col_b:
                if st.button("📋 Copy to Clipboard"):
                    st.success("Resume copied! Paste it into your document editor.")
            
            # Generate new version button
            if st.button("🔄 Generate New Version"):
                if 'resume_job_desc' in st.session_state:
                    with st.spinner("Generating new version..."):
                        new_resume = ai_gen.generate_resume(profile, st.session_state.resume_job_desc)
                        if new_resume:
                            st.session_state.generated_resume = new_resume
                            st.rerun()
        else:
            st.info("Your generated resume will appear here after you click 'Generate Resume'")
            
            st.markdown("#### 💡 Tips for Better Results:")
            st.markdown("""
            - Include complete job descriptions with requirements
            - Specify the company name for personalization
            - Ensure your profile has relevant skills and experience
            - The AI will match your background to the job requirements
            """)

def show_cover_letter_page():
    st.title("📝 AI Cover Letter Generator")
    st.markdown("---")
    
    profile = dm.load_user_profile()
    if not profile:
        st.warning("⚠️ Please create your user profile first!")
        if st.button("Go to Profile Page"):
            st.session_state.navigate_to = 'Profile'
            st.rerun()
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💼 Job & Company Details")
        
        company_name = st.text_input("Company Name*", placeholder="e.g., Tech Innovations Inc.")
        position_title = st.text_input("Position Title*", placeholder="e.g., Senior Python Developer")
        
        job_description = st.text_area(
            "Job Description:",
            height=200,
            placeholder="Paste the key requirements and responsibilities..."
        )
        
        hiring_manager = st.text_input("Hiring Manager Name (if known)", placeholder="e.g., John Smith")
        
        st.markdown("### ✨ Customization Options")
        tone = st.selectbox(
            "Writing Tone:",
            ["Professional", "Enthusiastic", "Formal", "Conversational"],
            index=0
        )
        
        focus_area = st.selectbox(
            "Focus On:",
            ["Technical Skills", "Leadership Experience", "Problem Solving", "Team Collaboration", "Innovation"],
            index=0
        )
        
        if st.button("✍️ Generate Cover Letter", type="primary", disabled=not (company_name and position_title)):
            if company_name.strip() and position_title.strip():
                with st.spinner("🔄 AI is writing your personalized cover letter..."):
                    try:
                        cover_letter = ai_gen.generate_cover_letter(
                            profile, 
                            company_name, 
                            position_title, 
                            job_description or "No specific job description provided."
                        )
                        
                        if cover_letter:
                            st.session_state.generated_cover_letter = cover_letter
                            st.session_state.cl_company = company_name
                            st.session_state.cl_position = position_title
                            
                            # Save/update application record
                            app_data = {
                                'company_name': company_name,
                                'position_title': position_title,
                                'application_date': datetime.now().isoformat(),
                                'status': 'pending',
                                'job_description': job_description[:500] + '...' if len(job_description) > 500 else job_description,
                                'documents_generated': ['cover_letter']
                            }
                            dm.save_job_application(app_data)
                            
                            st.success("✅ Cover letter generated successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to generate cover letter. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating cover letter: {str(e)}")
            else:
                st.warning("Please fill in Company Name and Position Title!")
    
    with col2:
        st.markdown("### 📄 Generated Cover Letter")
        
        if 'generated_cover_letter' in st.session_state:
            st.markdown("#### Preview:")
            st.text_area(
                "Your AI-Generated Cover Letter:",
                value=st.session_state.generated_cover_letter,
                height=300,
                help="Copy this text to your preferred document editor"
            )
            
            # NEW: PDF Download Section
            st.markdown("#### 📄 Download Options:")
            col_a, col_b = st.columns(2)
            
            with col_a:
                # PDF Download Button - NEW FEATURE!
                company_safe = st.session_state.get('cl_company', 'company').replace(' ', '_')
                filename_prefix = f"{profile.get('name', 'cover_letter').replace(' ', '_')}_{company_safe}"
                if create_pdf_download_button(
                    st.session_state.generated_cover_letter,
                    profile,
                    content_type="cover_letter",
                    filename_prefix=filename_prefix
                ):
                    st.success("✅ PDF ready for download!")
            
            with col_b:
                if st.button("📋 Copy Cover Letter"):
                    st.success("Cover letter copied! Paste it into your document editor.")
            
            # Generate new version button
            if st.button("🔄 Generate New Version"):
                if 'cl_company' in st.session_state and 'cl_position' in st.session_state:
                    with st.spinner("Generating new version..."):
                        new_cover_letter = ai_gen.generate_cover_letter(
                            profile, 
                            st.session_state.cl_company, 
                            st.session_state.cl_position,
                            job_description or "No specific job description provided."
                        )
                        if new_cover_letter:
                            st.session_state.generated_cover_letter = new_cover_letter
                            st.rerun()
        else:
            st.info("Your generated cover letter will appear here")
            
            st.markdown("#### 📝 Cover Letter Tips:")
            st.markdown("""
            - Research the company before generating
            - Mention specific job requirements you meet
            - Highlight relevant achievements with numbers
            - Keep it concise (3-4 paragraphs)
            - Always proofread before sending
            """)

def show_interview_questions_page():
    st.title("❓ Interview Questions Predictor")
    st.markdown("---")
    
    profile = dm.load_user_profile()
    if not profile:
        st.warning("⚠️ Please create your user profile first!")
        if st.button("Go to Profile Page"):
            st.session_state.navigate_to = 'Profile'
            st.rerun()
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 Job Details")
        
        position_title = st.text_input("Position Title", placeholder="e.g., Senior Python Developer")
        company_type = st.selectbox(
            "Company Type:",
            ["Startup", "Mid-size Company", "Large Corporation", "Non-profit", "Government", "Consulting"]
        )
        
        job_description = st.text_area(
            "Job Requirements & Responsibilities:",
            height=200,
            placeholder="Paste key requirements, skills needed, and main responsibilities..."
        )
        
        interview_type = st.selectbox(
            "Interview Type:",
            ["General", "Technical", "Behavioral", "Case Study", "Panel Interview"]
        )
        
        num_questions = st.slider("Number of Questions:", min_value=5, max_value=20, value=10)
        
        if st.button("🤖 Generate Interview Questions", type="primary"):
            if position_title.strip():
                with st.spinner("🔄 AI is predicting potential interview questions..."):
                    try:
                        questions = ai_gen.generate_interview_questions(
                            profile,
                            position_title,
                            job_description or f"Standard {position_title} position requirements."
                        )
                        
                        if questions:
                            st.session_state.interview_questions = questions
                            st.session_state.iq_position = position_title
                            st.session_state.iq_company_type = company_type
                            
                            st.success(f"✅ Generated {len(questions)} interview questions!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to generate questions. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating questions: {str(e)}")
            else:
                st.warning("Please enter a position title!")
    
    with col2:
        st.markdown("### 📝 Predicted Questions")
        
        if 'interview_questions' in st.session_state:
            st.markdown(f"#### Questions for: {st.session_state.get('iq_position', 'Unknown Position')}")
            
            questions = st.session_state.interview_questions
            for i, question in enumerate(questions, 1):
                st.markdown(f"**{i}.** {question}")
                
            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📋 Copy All Questions"):
                    st.success("Questions copied to clipboard!")
            
            with col_b:
                if st.button("🔄 Generate New Set"):
                    if st.session_state.get('iq_position'):
                        with st.spinner("Generating new questions..."):
                            new_questions = ai_gen.generate_interview_questions(
                                profile,
                                st.session_state.iq_position,
                                job_description or f"Standard {st.session_state.iq_position} position."
                            )
                            if new_questions:
                                st.session_state.interview_questions = new_questions
                                st.rerun()
        else:
            st.info("Interview questions will appear here after generation")
            
            st.markdown("#### 🎯 Interview Preparation Tips:")
            st.markdown("""
            - **Practice the STAR method** (Situation, Task, Action, Result)
            - **Research the company** thoroughly before the interview
            - **Prepare specific examples** from your experience
            - **Practice out loud**, not just in your head
            - **Prepare questions to ask them** about the role and company
            - **Review your resume** and be ready to explain any gaps
            """)

def show_job_applications_page():
    st.title("📊 Job Application Tracker")
    st.markdown("---")
    
    # Load applications
    applications = dm.get_job_applications()
    
    if not applications:
        st.info("🔍 No job applications tracked yet. Generate some resumes and cover letters to see them here!")
        return
    
    # Statistics overview
    col1, col2, col3, col4 = st.columns(4)
    stats = dm.get_application_stats()
    
    with col1:
        st.metric("Total Applications", stats['total_applications'])
    with col2:
        st.metric("Pending", stats['pending'])
    with col3:
        st.metric("Interview", stats['interview'])
    with col4:
        st.metric("Rejected", stats['rejected'])
    
    st.markdown("---")
    
    # Applications table
    st.markdown("### 📋 Application History")
    
    for i, app in enumerate(applications):
        with st.expander(f"**{app.get('company_name', 'Unknown')}** - {app.get('position_title', 'Unknown Position')}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Applied:** {app.get('application_date', 'Unknown')[:10]}")
                st.write(f"**Status:** {app.get('status', 'pending').title()}")
                # First, show the job description with Markdown formatting
                if app.get('job_description'):
                    st.markdown("**Job Description:**")
                    st.markdown(app['job_description'])  # This will render **bold** correctly
            
            with col2:
                current_status = st.selectbox(
                    "Update Status:",
                    ["pending", "interview", "rejected", "offered", "accepted"],
                    index=["pending", "interview", "rejected", "offered", "accepted"].index(app.get('status', 'pending')),
                    key=f"status_{i}"
                )
                
                if st.button("Update", key=f"update_{i}"):
                    # Update application status
                    app['status'] = current_status
                    if dm.update_application_status(i, current_status):
                        st.success("Status updated!")
                        st.rerun()
                    else:
                        st.error("Failed to update status")
                
                if app.get('documents_generated'):
                    st.write("**Generated:**")
                    for doc in app['documents_generated']:
                        st.write(f"• {doc.title()}")

if __name__ == "__main__":
    main()