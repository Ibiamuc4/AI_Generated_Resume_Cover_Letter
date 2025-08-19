"""
PDF Creator for Resume and Cover Letter Generation
Step 10: Professional PDF generation with multiple templates
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black, blue, gray, darkblue
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import io
from datetime import datetime
from typing import Dict, List, Optional

class PDFCreator:
    def __init__(self):
        """Initialize PDF Creator with professional styles"""
        
        # Define professional color schemes
        self.color_schemes = {
            'professional': {
                'primary': darkblue,
                'secondary': gray,
                'text': black,
                'accent': blue
            },
            'modern': {
                'primary': black,
                'secondary': gray,
                'text': black,
                'accent': darkblue
            },
            'classic': {
                'primary': black,
                'secondary': black,
                'text': black,
                'accent': black
            }
        }
        
        # Default color scheme
        self.colors = self.color_schemes['professional']
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles for professional formatting"""
        
        # Remove existing custom styles if they exist
        custom_style_names = [
            'CustomTitle', 'ContactInfo', 'SectionHeader', 
            'BodyText', 'BulletPoint', 'JobTitle', 'CompanyInfo'
        ]
        
        for name in custom_style_names:
            if name in self.styles.byName:
                del self.styles.byName[name]
            if name in self.styles.byAlias:
                del self.styles.byAlias[name]
        
        # Now re-add the styles
        # Header styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=6,
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            textColor=self.colors['text'],
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=12,
            spaceAfter=6,
            textColor=self.colors['primary'],
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=0,
            leftIndent=0,
            borderColor=self.colors['primary']
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=self.colors['text'],
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            textColor=self.colors['text'],
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=8,
            spaceAfter=2,
            textColor=self.colors['primary'],
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=self.colors['secondary'],
            fontName='Helvetica-Oblique'
        ))

    def create_resume_pdf(self, resume_text: str, user_profile: Dict, 
                         template_style: str = 'professional') -> bytes:
        """
        Create a professional PDF resume from formatted text
        """
        try:
            # Create PDF buffer
            buffer = io.BytesIO()
            
            # Set up document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Parse resume text into structured sections
            sections = self._parse_resume_text(resume_text)
            
            # Build PDF content
            story = []
            story.extend(self._build_header_section(sections, user_profile))
            story.extend(self._build_body_sections(sections))
            
            # Generate PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            return pdf_bytes
            
        except Exception as e:
            raise Exception(f"Error creating PDF: {str(e)}")
        
    def _parse_resume_text(self, resume_text: str) -> Dict:
        """Parse the resume text into structured sections"""
        
        sections = {
            'name': '',
            'contact': '',
            'summary': '',
            'skills': '',
            'experience': '',
            'education': '',
            'additional': ''
        }

        lines = resume_text.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('}') or line.startswith('{'):
                continue  # Skip empty or garbage lines

            # Detect section headers
            line_upper = line.upper()
            if 'PROFESSIONAL SUMMARY' in line_upper:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = 'summary'
                current_content = []
            elif 'TECHNICAL SKILLS' in line_upper or 'SKILLS' in line_upper:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = 'skills'
                current_content = []
            elif 'PROFESSIONAL EXPERIENCE' in line_upper or 'EXPERIENCE' in line_upper:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = 'experience'
                current_content = []
            elif 'EDUCATION' in line_upper:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = 'education'
                current_content = []
            elif not sections['name'] and '@' not in line and 'http' not in line:
                # First non-empty line is the name
                sections['name'] = line
            elif '@' in line or '|' in line or ('Phone' in line or 'Email' in line):
                # Contact info
                sections['contact'] = line.replace('•', '').strip()
            elif current_section:
                current_content.append(line)
            else:
                # Fallback for unstructured content
                sections['additional'] += line + '\n'

        # Save any remaining content
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _build_header_section(self, sections: Dict, user_profile: Dict) -> List:
        """Build the header section with name and contact info"""
        
        story = []
        
        # Name
        name = sections.get('name') or user_profile.get('name', 'Your Name')
        story.append(Paragraph(name, self.styles['CustomTitle']))
        
        # Contact information
        contact = sections.get('contact')
        if not contact:
            email = user_profile.get('email', 'email@example.com')
            phone = user_profile.get('phone', '(123) 456-7890')
            location = user_profile.get('location', 'City, State')
            contact = f"{email} | {phone} | {location}"
        
        story.append(Paragraph(contact, self.styles['ContactInfo']))
        story.append(Spacer(1, 0.2*inch))
        
        return story

    def _build_body_sections(self, sections: Dict) -> List:
        """Build the main body sections of the resume"""
        
        story = []
        
        # Section order for professional layout
        section_order = [
            ('summary', 'PROFESSIONAL SUMMARY'),
            ('skills', 'TECHNICAL SKILLS'),
            ('experience', 'PROFESSIONAL EXPERIENCE'),
            ('education', 'EDUCATION'),
            ('additional', 'ADDITIONAL QUALIFICATIONS')
        ]
        
        for section_key, section_title in section_order:
            content = sections.get(section_key, '').strip()
            if content and len(content) > 5:  # Only add if content exists
                story.extend(self._format_section(section_title, content))
        
        return story

    def _format_section(self, title: str, content: str) -> List:
        """Format a section with title and content"""
        
        story = []
        
        # Section header with line
        header_table = Table([
            [Paragraph(title, self.styles['SectionHeader']), '']
        ], colWidths=[3*inch, 4*inch])
        
        header_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.colors['primary']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 0.1*inch))
        
        # Format content based on section type
        if title in ['TECHNICAL SKILLS', 'SKILLS']:
            story.extend(self._format_skills_content(content))
        elif title in ['PROFESSIONAL EXPERIENCE', 'EXPERIENCE']:
            story.extend(self._format_experience_content(content))
        else:
            # Regular paragraph content
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # Check if it's a bullet point
                    if para.strip().startswith('•') or para.strip().startswith('-'):
                        lines = para.split('\n')
                        for line in lines:
                            if line.strip():
                                story.append(Paragraph(line.strip(), self.styles['BulletPoint']))
                    else:
                        story.append(Paragraph(para.strip(), self.styles['BodyText']))
        
        story.append(Spacer(1, 0.15*inch))
        return story

    def _format_skills_content(self, content: str) -> List:
        """Format skills content with proper bullet points"""
        
        story = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or ':' in line):
                story.append(Paragraph(line, self.styles['BulletPoint']))
        
        return story

    def _format_experience_content(self, content: str) -> List:
        """Format experience content with job titles and descriptions"""
        
        story = []
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            lines = para.split('\n')
            
            # First line is usually job title/company
            if lines:
                first_line = lines[0].strip()
                if '|' in first_line or any(word in first_line.upper() for word in ['DEVELOPER', 'ENGINEER', 'ANALYST', 'MANAGER']):
                    story.append(Paragraph(first_line, self.styles['JobTitle']))
                    # Rest are bullet points
                    for line in lines[1:]:
                        line = line.strip()
                        if line:
                            if not line.startswith('•'):
                                line = '• ' + line
                            story.append(Paragraph(line, self.styles['BulletPoint']))
                else:
                    # Treat as regular content
                    story.append(Paragraph(para, self.styles['BodyText']))
        
        return story

    def create_cover_letter_pdf(self, cover_letter_text: str, user_profile: Dict) -> bytes:
        """
        Create a professional PDF cover letter
        """
        try:
            # Create PDF buffer
            buffer = io.BytesIO()
            
            # Set up document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=1*inch,
                leftMargin=1*inch,
                topMargin=1*inch,
                bottomMargin=1*inch
            )
            
            story = []
            
            # Header with contact info
            name = user_profile.get('name', 'Your Name')
            email = user_profile.get('email', 'email@example.com')
            phone = user_profile.get('phone', '(123) 456-7890')
            location = user_profile.get('location', 'City, State')
            
            # Contact header
            story.append(Paragraph(name, self.styles['CustomTitle']))
            contact_info = f"{email} | {phone} | {location}"
            story.append(Paragraph(contact_info, self.styles['ContactInfo']))
            story.append(Spacer(1, 0.3*inch))
            
            # Date
            date_str = datetime.now().strftime("%B %d, %Y")
            story.append(Paragraph(date_str, self.styles['BodyText']))
            story.append(Spacer(1, 0.2*inch))
            
            # Cover letter content
            paragraphs = cover_letter_text.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if para:
                    story.append(Paragraph(para, self.styles['BodyText']))
                    story.append(Spacer(1, 0.1*inch))
            
            # Generate PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            return pdf_bytes
            
        except Exception as e:
            raise Exception(f"Error creating cover letter PDF: {str(e)}")

    def set_color_scheme(self, scheme: str):
        """Change the color scheme for PDFs"""
        if scheme in self.color_schemes:
            self.colors = self.color_schemes[scheme]
            self._create_custom_styles()


# Test function
if __name__ == "__main__":
    print("🧪 Testing PDF Creator...")
    
    # Initialize PDF creator
    pdf_creator = PDFCreator()
    
    # Sample resume text (as generated by AI)
    sample_resume = """
JOHN DOE
john@example.com | (123) 456-7890 | New York, NY

PROFESSIONAL SUMMARY
Experienced Software Developer with 3 years of professional experience in designing and implementing robust applications.
Expertise in Python, JavaScript, SQL, React with proven track record of delivering high-quality solutions on time and within budget.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, SQL
• Web Technologies: React, HTML, CSS
• Tools & Frameworks: Git, Docker
• Soft Skills: Problem Solving, Team Collaboration

PROFESSIONAL EXPERIENCE
SOFTWARE DEVELOPER | Various Projects & Experience | 3 Years
• Developed and maintained applications using Python, JavaScript, SQL
• Collaborated with cross-functional teams to deliver high-quality software solutions
• Participated in code reviews and implemented best practices for software development

EDUCATION
Bachelor of Science in Computer Science
XYZ University, 2021
    """
    
    # Sample user profile
    sample_profile = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '(123) 456-7890',
        'location': 'New York, NY'
    }
    
    # Sample cover letter
    sample_cover_letter = """
Dear Hiring Manager,

I am writing to express my strong interest in the Software Developer position at your organization. With 3 years of experience in software development and a proven track record in Python, JavaScript, SQL, I am excited about the opportunity to contribute to your team.

In my professional experience, I have developed expertise in the key areas outlined in your job requirements. My background in Python and JavaScript aligns well with your needs, and I am particularly drawn to your organization's commitment to innovation and teamwork.

Key strengths I would bring to this role include:
• Strong technical foundation with practical experience in relevant technologies
• Proven ability to work collaboratively in team environments while delivering individual results
• Commitment to writing clean, efficient, and maintainable code

Thank you for considering my application. I look forward to hearing from you.

Sincerely,
John Doe
    """
    
    try:
        print("📄 Testing Resume PDF Generation...")
        resume_pdf = pdf_creator.create_resume_pdf(sample_resume, sample_profile)
        print(f"✅ Resume PDF created successfully! Size: {len(resume_pdf)} bytes")
        
        print("\n📝 Testing Cover Letter PDF Generation...")
        cover_letter_pdf = pdf_creator.create_cover_letter_pdf(sample_cover_letter, sample_profile)
        print(f"✅ Cover Letter PDF created successfully! Size: {len(cover_letter_pdf)} bytes")
        
        # Test saving to file (optional)
        print("\n💾 Testing File Save...")
        with open("test_resume.pdf", "wb") as f:
            f.write(resume_pdf)
        with open("test_cover_letter.pdf", "wb") as f:
            f.write(cover_letter_pdf)
        print("✅ Test PDF files saved: test_resume.pdf, test_cover_letter.pdf")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("📦 Make sure to install reportlab: pip install reportlab")
    
    print("\n🎉 PDF Creator testing complete!")