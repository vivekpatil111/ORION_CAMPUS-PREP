from typing import Dict, Optional
import PyPDF2
import docx
import io
import re

class ResumeParser:
    """
    Service for parsing resume files (PDF/DOCX) and extracting information
    """
    
    def __init__(self):
        pass

    def parse_resume(self, file_bytes: bytes, filename: str) -> Dict:
        """
        Parse resume file and extract structured data
        """
        if filename.endswith('.pdf'):
            return self._parse_pdf(file_bytes)
        elif filename.endswith('.docx'):
            return self._parse_docx(file_bytes)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

    def _parse_pdf(self, pdf_bytes: bytes) -> Dict:
        """Parse PDF resume"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return self._extract_information(text)
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")

    def _parse_docx(self, docx_bytes: bytes) -> Dict:
        """Parse DOCX resume"""
        try:
            docx_file = io.BytesIO(docx_bytes)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return self._extract_information(text)
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")

    def _extract_information(self, text: str) -> Dict:
        """Extract structured information from resume text"""
        # Basic extraction using regex patterns
        # In production, use NLP libraries or ML models for better extraction
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        email = re.findall(email_pattern, text)
        phone = re.findall(phone_pattern, text)
        
        # Extract skills (common keywords)
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'mongodb', 'postgresql', 'linux',
            'machine learning', 'ai', 'data science', 'agile', 'scrum'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        # Extract education (simplified)
        education = self._extract_education(text)
        
        # Extract experience (simplified)
        experience = self._extract_experience(text)
        
        return {
            'email': email[0] if email else None,
            'phone': phone[0] if phone else None,
            'skills': found_skills,
            'education': education,
            'experience': experience,
            'summary': text[:500] + '...' if len(text) > 500 else text,
            'raw_text': text
        }

    def _extract_education(self, text: str) -> list:
        """Extract education information"""
        # Simplified extraction
        # In production, use NER (Named Entity Recognition) models
        education_keywords = ['university', 'college', 'bachelor', 'master', 'phd', 'degree']
        lines = text.split('\n')
        education_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                education_lines.append(line.strip())
        
        return education_lines[:3]  # Return top 3 matches

    def _extract_experience(self, text: str) -> list:
        """Extract work experience"""
        # Simplified extraction
        # In production, use structured parsing
        experience_keywords = ['experience', 'work', 'employed', 'position', 'role']
        lines = text.split('\n')
        experience_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in experience_keywords):
                experience_lines.append(line.strip())
        
        return experience_lines[:5]  # Return top 5 matches
