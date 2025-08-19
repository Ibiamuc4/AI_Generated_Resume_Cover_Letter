#!/usr/bin/env python3
"""
AI Generator Module
Handles AI-powered resume, cover letter, and interview question generation
"""
import together
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

import re
import json
import random
from typing import Dict, List, Any, Optional

class AIGenerator:
    """Generates AI-powered content for resumes, cover letters, and interviews"""
    
    def __init__(self):
        self.resume_templates = self._load_resume_templates()
        self.cover_letter_templates = self._load_cover_letter_templates()
        self.question_templates = self._load_question_templates()

      
        
    def _load_resume_templates(self) -> Dict[str, str]:
        """Load resume section templates"""
        return {
            'professional_summary': [
                "Experienced {title} with {years}+ years in {skills}. Proven track record of {achievements}. Seeking to leverage expertise in {target_skills} to contribute to {company_type} success.",
                "Results-driven {title} specializing in {skills}. {years} years of experience delivering {achievements}. Passionate about {target_skills} and driving innovation in {industry}.",
                "Dynamic {title} with extensive background in {skills}. Known for {achievements} and excellence in {target_skills}. Ready to bring proven skills to {company_type}."
            ],
            'skills_intro': [
                "Technical Expertise:",
                "Core Competencies:",
                "Key Skills:",
                "Technical Proficiencies:"
            ]
        }
        
    def _load_cover_letter_templates(self) -> List[str]:
        """Load cover letter templates"""
        return [
            """Dear Hiring Manager,

I am writing to express my strong interest in the {position} role at {company}. With my background in {skills} and {experience}, I am excited about the opportunity to contribute to your team.

In my previous experience, I have {achievements}. My expertise in {key_skills} aligns perfectly with the requirements outlined in your job posting. I am particularly drawn to {company} because of {company_reason}.

Key qualifications that make me an ideal candidate:
• {qualification_1}
• {qualification_2}
• {qualification_3}

I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to {company}'s continued success. Thank you for considering my application.

Sincerely,
{name}""",

            """Dear {company} Team,

I am excited to apply for the {position} position at {company}. Your commitment to {company_value} resonates strongly with my professional values and career aspirations.

With {experience} in {field}, I have developed strong skills in {skills}. My experience includes {specific_achievement}, which directly relates to the challenges outlined in your job description.

What I bring to {company}:
• Proven expertise in {skill_1}
• Experience with {skill_2}
• Track record of {achievement}

I am eager to bring my passion for {field} and proven problem-solving abilities to your innovative team. I look forward to the opportunity to discuss how I can contribute to {company}'s mission.

Best regards,
{name}"""
        ]
    
    def _load_question_templates(self) -> Dict[str, List[str]]:
        """Load interview question templates"""
        return {
            'general': [
                "Tell me about yourself and your background in {field}.",
                "Why are you interested in this {position} role?",
                "What attracts you to our company?",
                "Describe your experience with {skill}.",
                "How do you stay updated with the latest {field} trends?"
            ],
            'technical': [
                "Explain your experience with {technical_skill}.",
                "How would you approach {technical_challenge}?",
                "Describe a challenging {technical_project} you worked on.",
                "What tools and technologies do you use for {task}?",
                "How do you ensure code quality in your projects?"
            ],
            'behavioral': [
                "Describe a time when you had to learn a new {skill} quickly.",
                "Tell me about a challenging project and how you overcame obstacles.",
                "How do you handle tight deadlines and pressure?",
                "Describe a situation where you had to work with a difficult team member.",
                "Give an example of how you've contributed to team success."
            ]
        }
    
 

    def generate_resume(self, profile: Dict[str, Any], job_description: str) -> str:
        """Generate a tailored resume using Together AI (llama 3 model)"""
        
        # Get API key
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            print("⚠️ Together AI API key not found. Using template-based generation.")
            return self._generate_resume_template(profile, job_description)
        
        # Initialize Together AI client
        client = together.Together(api_key=api_key)
        
        try:
            prompt = f"""
You are a professional resume writer. Generate a clean, ATS-friendly resume based on the user's profile and job description.

USER PROFILE:
Name: {profile.get('name', 'John Doe')}
Email: {profile.get('email', 'email@example.com')}
Phone: {profile.get('phone', '123-456-7890')}
Location: {profile.get('location', 'City, State')}
Title: {profile.get('current_title', 'Professional')}
Skills: {profile.get('skills', 'Not specified')}
Experience: {profile.get('experience', 'Not specified')}
Education: {profile.get('education', 'Not specified')}

Job Description: {job_description}

Format: Name, Email, Phone, Location, Title, Summary, Skills, Experience, Education
Use bullet points (•). Keep it concise and ATS-friendly.
Do NOT return code, explanations, or function definitions.
- Do NOT add any closing remarks like "The resume is ATS-friendly and concise... NB: This is a proffessional document and it is converted to a pdf document immediately it is generated. Hence it does not require any uneccessary addition."
- Do NOT include any extra explanations, summaries, or evaluations of the resume, what is generated is converted directly into a resume pdf so no extra words are needed before or after the resume
- Do NOT use vertical bars (|) or table-like formatting or any other unecessary symbols
- Return ONLY the resume content — nothing else
"""

            # Call Together AI
            response = client.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9
            )

            # Get raw AI output
            raw_text = response.choices[0].text.strip()

            # Remove anything after common code-like patterns
            if "def " in raw_text or "```" in raw_text or "print(" in raw_text:
                # Remove code blocks
                if "```" in raw_text:
                    parts = raw_text.split("```")
                    for part in parts:
                        if "def " not in part and "print(" not in part and "class " not in part:
                            raw_text = part.strip()
                            break

            # Remove any line that starts with "#"
            lines = [line for line in raw_text.split('\n') if not line.strip().startswith('#')]
            clean_text = '\n'.join(lines)

            # Remove common unwanted trailing explanations
            if "this code" in clean_text.lower() or "note that" in clean_text.lower():
                # Try to cut off everything after the real resume ends
                lines = clean_text.split('\n')
                filtered_lines = []
                for line in lines:
                    if any(trigger in line.lower() for trigger in ["this code", "note that", "recommended to use", "simple implementation"]):
                        break
                    filtered_lines.append(line)
                clean_text = '\n'.join(filtered_lines).strip()

            # Final cleanup: remove any lingering unwanted content
            clean_text = raw_text.strip()

            # Remove everything before the first real line (e.g., "Here is the resume:")
            if '\n' in clean_text:
                lines = clean_text.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('**') or line.strip().startswith(profile.get('name', '')) or 'Dear' in line:
                        clean_text = '\n'.join(lines[i:])
                        break

            # Remove any trailing explanations
            triggers = ["this code", "note that", "recommended to use", "simple implementation", "function", "def ", "return "]
            for trigger in triggers:
                if trigger in clean_text.lower():
                    parts = clean_text.lower().split(trigger)
                    if len(parts) > 1:
                        clean_text = clean_text[:parts[0].rfind('\n')].strip()
                    break

            # Final strip
            clean_text = clean_text.strip()

            # After all post-processing, reformat the resume properly
            clean_text = clean_text.strip()

            # Extract key info from profile
            name = profile.get('name', 'Your Name')
            email = profile.get('email', 'email@example.com')
            phone = profile.get('phone', 'Phone')
            location = profile.get('location', 'Location')
            current_title = profile.get('current_title', 'Professional')

            # Rebuild the resume in the correct format
            formatted_resume = f"""{name}
            {email} | {phone} | {location}

            PROFESSIONAL SUMMARY
            {clean_text.split('Summary:')[-1].split('Skills:')[0].strip() if 'Summary:' in clean_text else 'Summary not available.'}

            TECHNICAL SKILLS
            {clean_text.split('Skills:')[-1].split('Experience:')[0].strip().replace('•', '• ') if 'Skills:' in clean_text else 'Skills not available.'}

            PROFESSIONAL EXPERIENCE
            {clean_text.split('Experience:')[-1].split('Education:')[0].strip().replace('•', '• ') if 'Experience:' in clean_text else 'Experience not available.'}

            EDUCATION
            {clean_text.split('Education:')[-1].split('}')[0].strip() if 'Education:' in clean_text else 'Education not available.'}
            """

            # Final cleanup: remove any remaining } } } } } 
            formatted_resume = ''.join([char for char in formatted_resume if char not in ['{', '}']]).strip()

            # Final cleanup: Remove everything after the first complete resume
            # Look for the end of EDUCATION and cut off anything after
            end_markers = [
                "Note:", 
                "The above is the actual resume", 
                "resume writer's work is done",
                "PROFESSIONAL SUMMARY" in clean_text.split("EDUCATION")[1].upper() if "EDUCATION" in clean_text else False
            ]

            for marker in end_markers:
                if marker and isinstance(marker, str) and marker in clean_text:
                    index = clean_text.find(marker)
                    if index != -1:
                        clean_text = clean_text[:index].strip()
                        break

            # Remove any lines with only | symbols (table-like formatting)
            lines = clean_text.split('\n')
            cleaned_lines = []
            for line in lines:
                stripped = line.strip()
                # Remove lines that are just separators like | | | | | 
                if '|' in stripped and stripped.replace('|', '').replace(' ', '').replace('\t', '') == '':
                    continue
                # Remove empty or whitespace-only lines
                if stripped == '':
                    continue
                cleaned_lines.append(line)

            clean_text = '\n'.join(cleaned_lines).strip()

            # Final: Remove any duplicate sections
            # If "TECHNICAL SKILLS" appears twice, keep only the first
            for section in ["TECHNICAL SKILLS", "PROFESSIONAL EXPERIENCE", "EDUCATION"]:
                parts = clean_text.split(section)
                if len(parts) > 2:
                    # Rebuild: first part + section + second part (the real content)
                    clean_text = parts[0] + section + parts[1]
                    # If there's a third part, don't include it

            return formatted_resume

        except Exception as e:
            print(f"❌ Error with Together AI: {e}")
            return self._generate_resume_template(profile, job_description)

    def _generate_resume_template(self, profile: Dict[str, Any], job_description: str) -> str:
        """
        Fallback: Generate resume using local templates (no AI)
        """
        name = profile.get('name', 'Your Name')
        email = profile.get('email', 'email@example.com')
        phone = profile.get('phone', 'Phone')
        skills = profile.get('skills', 'Skills not specified')
        experience = profile.get('experience', 'Experience not specified')
        education = profile.get('education', 'Education not specified')

        # Simple resume format
        resume = f"""
        {name}
        {email} | {phone}

        PROFESSIONAL SUMMARY
        Experienced professional with skills in {skills}. 
        Seeking to leverage expertise in a challenging new role.

        TECHNICAL SKILLS
        • {skills}

        PROFESSIONAL EXPERIENCE
        • {experience}

        EDUCATION
        • {education}
        """.strip()

        return resume

    def _extract_job_keywords(self, job_description: str) -> List[str]:
        """Extract relevant keywords from job description"""
        # Simple keyword extraction (in a real app, this would be more sophisticated)
        common_keywords = [
            'python', 'javascript', 'sql', 'react', 'node.js', 'aws', 'docker',
            'machine learning', 'data analysis', 'project management', 'leadership',
            'communication', 'problem solving', 'teamwork', 'agile', 'scrum'
        ]
        
        job_lower = job_description.lower()
        found_keywords = [keyword for keyword in common_keywords if keyword in job_lower]
        return found_keywords[:10]  # Return top 10 relevant keywords
    
    def _generate_professional_summary(self, profile: Dict[str, Any], job_keywords: List[str]) -> str:
        """Generate professional summary based on profile and job requirements"""
        name = profile.get('name', 'Professional')
        current_title = profile.get('current_title', 'Experienced Professional')
        experience_text = profile.get('experience', '')
        skills_text = profile.get('skills', '')
        
        # Extract years of experience
        years = "several"
        if "years" in experience_text.lower():
            import re
            years_match = re.search(r'(\d+)\s*years?', experience_text.lower())
            if years_match:
                years = years_match.group(1)
        
        # Create summary
        summary = f"Experienced {current_title} with {years} years of professional experience. "
        
        if skills_text:
            skills_list = [s.strip() for s in skills_text.split(',')[:3]]  # Take first 3 skills
            summary += f"Specialized in {', '.join(skills_list)}. "
        
        summary += "Proven track record of delivering high-quality solutions and driving project success. "
        
        if job_keywords:
            summary += f"Strong background in {', '.join(job_keywords[:3])} with focus on innovation and continuous improvement."
        
        return summary
    
    def _format_skills(self, skills_list: List[str], job_keywords: List[str]) -> str:
        """Format skills section with emphasis on job-relevant skills"""
        if not skills_list:
            return "• Technical skills to be specified based on experience"
        
        # Prioritize skills that match job keywords
        prioritized_skills = []
        other_skills = []
        
        for skill in skills_list:
            if any(keyword in skill.lower() for keyword in job_keywords):
                prioritized_skills.append(skill)
            else:
                other_skills.append(skill)
        
        all_skills = prioritized_skills + other_skills
        
        # Format skills in bullet points
        formatted_skills = []
        for skill in all_skills[:8]:  # Limit to 8 skills
            formatted_skills.append(f"• {skill.strip()}")
        
        return '\n'.join(formatted_skills)
    
    def _format_experience(self, experience_text: str, job_keywords: List[str]) -> str:
            """Format experience section with job-relevant emphasis"""
            if not experience_text:
                return "Professional experience details to be added based on background."
            
            # Clean up the experience text and add structure
            lines = experience_text.split('\n')
            formatted_lines = []
            
            for line in lines:
                if line.strip():
                    if not line.startswith('•') and not line.startswith('-'):
                        formatted_lines.append(f"• {line.strip()}")
                    else:
                        formatted_lines.append(line.strip())
            
            formatted_experience = '\n'.join(formatted_lines)
            
            # Add emphasis on job-relevant keywords if present
            if job_keywords:
                formatted_experience += f"\n\n• Relevant expertise: {', '.join(job_keywords[:5])}"
            
            return formatted_experience
        
    def generate_cover_letter(self, profile: Dict[str, Any], company_name: str, position_title: str, job_description: str = "") -> str:
        """Generate a personalized cover letter using Together AI"""
        
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            print("⚠️ Together AI API key not found. Using template-based generation.")
            return self._generate_cover_letter_template(profile, company_name, position_title, job_description)
        
        client = together.Together(api_key=api_key)
        
        try:
            prompt = f"""
You are a career coach. Write a professional cover letter for the {position_title} role at {company_name}.

APPLICANT:
Name: {profile.get('name', 'Your Name')}
Skills: {profile.get('skills', 'Not specified')}
Experience: {profile.get('experience', 'Not specified')}
Title: {profile.get('current_title', 'Professional')}

JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
- Write a 3–4 paragraph cover letter
- Address the hiring manager professionally
- Show enthusiasm for the role and company
- Highlight relevant skills and experience
- Connect the applicant's background to the job
- Use natural line breaks between paragraphs
- Do NOT return any code, variables, or programming syntax
- Do NOT use f-strings, `return` statements, or function definitions
- Do NOT include code blocks (```) or comments
- Do NOT say things like "This code generates a cover letter"
- Do NOT add explanations or tutorials
- Return ONLY the cover letter text — nothing else

Now write the cover letter:
"""

            response = client.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
                prompt=prompt,
                max_tokens=600,
                temperature=0.8,
                top_p=0.9
            )
            
            # Step 1: Get raw AI output
            raw_text = response.choices[0].text.strip()

            # Step 2: Remove /* */ comment wrappers if present
            if raw_text.startswith('/*'):
                raw_text = raw_text[2:].lstrip()
            if raw_text.endswith('*/'):
                raw_text = raw_text[:-2].rstrip()

            # Step 3: If the AI returned a code block, extract only the content inside
            if "```" in raw_text:
                parts = raw_text.split("```")
                for part in parts:
                    if part.strip().startswith("Dear") or "Hiring Manager" in part:
                        raw_text = part.strip()
                        break

            # Step 4: Remove only lines that are clearly comments (start with # and are short)
            lines = raw_text.split('\n')
            cleaned_lines = []
            for line in lines:
                stripped = line.strip()
                if not (stripped.startswith('#') and len(stripped) < 80):
                    cleaned_lines.append(line)

            clean_text = '\n'.join(cleaned_lines).strip()

            # Step 5: Find the first closing line and cut everything after it
            closing_signs = ['Sincerely,', 'Best regards,', 'Yours truly,', 'Kind regards,']
            closing_found = False
            final_lines = []

            for line in clean_text.split('\n'):
                line_stripped = line.strip()
                
                # Add the line
                final_lines.append(line)
                
                # Check if this line starts with a closing phrase
                if any(line_stripped.startswith(closing) for closing in closing_signs):
                    closing_found = True
                    # Also include the next line (the name)
                    continue
                
                # If we already found the closing and the next line is the name, stop
                if closing_found:
                    # Assume the next line after closing is the name
                    # So we stop after that
                    if len(final_lines) >= 2:
                        last_line = final_lines[-1].strip()
                        second_last = final_lines[-2].strip()
                        if any(second_last.startswith(c) for c in closing_signs) and last_line:
                            break  # Stop here

            # Join the final lines
            final_text = '\n'.join(final_lines).strip()

            # Step 6: Ensure we don't have trailing garbage
            # If there's a line like "Here is the cover letter written in a professional tone", remove it
            if "Here is the cover letter" in final_text or "This code defines" in final_text or "Note that" in final_text:
                # Find the last "Sincerely," or similar and cut off after name
                lines = final_text.split('\n')
                end_index = len(lines)
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if any(stripped.startswith(c) for c in closing_signs) and i + 1 < len(lines):
                        end_index = i + 2  # Include the name line
                        break
                final_text = '\n'.join(lines[:end_index]).strip()

            return final_text

        except Exception as e:
            print(f"❌ Error with Together AI: {e}")
            return self._generate_cover_letter_template(profile, company_name, position_title, job_description)
            

    def _generate_cover_letter_template(self, profile: Dict[str, Any], company_name: str, position_title: str, job_description: str = "") -> str:
        """
        Fallback: Generate a simple cover letter using templates (no AI)
        """
        name = profile.get('name', 'Your Name')
        email = profile.get('email', 'email@example.com')
        skills = ', '.join(profile.get('skills', ['Python']))
        experience = profile.get('experience', 'several years of experience')

        return f"""
    Dear Hiring Manager,

    I am writing to express my interest in the {position_title} position at {company_name}. With my background in {skills}, I am confident in my ability to contribute effectively to your team.

    My experience includes {experience}, and I have a proven track record of solving complex problems and delivering high-quality results.

    Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your organization.

    Sincerely,
    {name}
        """.strip()
    
    
    def generate_interview_questions(self, profile: Dict[str, Any], position_title: str, job_description: str = "") -> List[str]:
        """Generate potential interview questions based on profile and position"""
        try:
            questions = []
            
            # Get question templates
            templates = self._load_question_templates()
            
            # Extract skills from profile
            skills_text = profile.get('skills', '')
            skills_list = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
            
            # Add general questions
            general_questions = templates['general'][:2]
            for template in general_questions:
                question = template.format(
                    field=position_title.lower(),
                    position=position_title.lower(),
                    skill=skills_list[0] if skills_list else "your field"
                )
                questions.append(question)
            
            # Add technical questions based on skills
            if skills_list:
                tech_templates = templates['technical'][:3]
                for i, template in enumerate(tech_templates):
                    skill = skills_list[i % len(skills_list)]
                    question = template.format(
                        technical_skill=skill,
                        technical_challenge=f"{skill} implementation",
                        technical_project=f"{skill} project",
                        task=f"{skill} development"
                    )
                    questions.append(question)
            
            # Add behavioral questions
            behavioral_questions = templates['behavioral'][:3]
            for template in behavioral_questions:
                question = template.format(
                    skill=skills_list[0] if skills_list else "technology"
                )
                questions.append(question)
            
            # Add position-specific questions
            questions.extend([
                f"What interests you most about this {position_title} role?",
                f"How do you see yourself contributing to our {position_title} team?",
                f"What are your long-term career goals in {position_title.lower()}?"
            ])
            
            return questions[:10]  # Return first 10 questions
            
        except Exception as e:
            print(f"Error generating interview questions: {e}")
            return [
                "Tell me about your background and experience.",
                "Why are you interested in this position?",
                "What are your key strengths?",
                "How do you handle challenging situations?",
                "Where do you see yourself in 5 years?"
            ]


# Test the AI Generator (only runs when file is executed directly)
if __name__ == "__main__":
    print("🧪 Testing AI Generator...")
    
    ai_gen = AIGenerator()
    
    # Test profile
    test_profile = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "location": "New York, NY",
        "current_title": "Python Developer",
        "skills": "Python, JavaScript, SQL, React, Docker",
        "experience": "5 years of software development experience focusing on web applications and data analysis",
        "education": "Bachelor's in Computer Science"
    }
    
    # Test job description
    test_job = """We are seeking a Senior Python Developer with expertise in web development 
    and data analysis. The ideal candidate should have experience with Python, JavaScript, 
    SQL, and modern web frameworks. Strong problem-solving skills required."""
    
    print("📄 Testing Resume Generation...")
    resume = ai_gen.generate_resume(test_profile, test_job)
    if resume and not resume.startswith("Error"):
        print("✅ Resume generated successfully!")
        print("Preview:", resume[:200] + "...")
    else:
        print("❌ Resume generation failed!")
        print(resume)
    
    print("\n📝 Testing Cover Letter Generation...")
    cover_letter = ai_gen.generate_cover_letter(test_profile, "TechCorp Inc", "Senior Python Developer", test_job)
    if cover_letter and not cover_letter.startswith("Error"):
        print("✅ Cover letter generated successfully!")
    else:
        print("❌ Cover letter generation failed!")
        print(cover_letter)
    
    print("\n❓ Testing Interview Questions...")
    questions = ai_gen.generate_interview_questions(test_profile, "Senior Python Developer", test_job)
    if questions:
        print(f"✅ Generated {len(questions)} interview questions")
        for i, q in enumerate(questions[:3]):
            print(f"  {i+1}. {q}")
    else:
        print("❌ Interview questions generation failed!")
    
    print("\n🎉 AI Generator testing complete!")