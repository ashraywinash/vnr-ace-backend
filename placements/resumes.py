import pdfplumber
from docx import Document
from pathlib import Path
import json
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
from pyparsing import Dict
from pydantic import BaseModel
from typing import List, Dict

load_dotenv()




class SectionFeedback(BaseModel):
    issues: List[str]
    suggestions: List[str]
    example_rewrites: List[str]

class ResumeAnalysis(BaseModel):
    overall_score: int
    summary: List[str]
    section_feedback: Dict[str, SectionFeedback]
    ats_issues: List[str]
    priority_fixes: List[str]

class ResumeAdvisor:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def _call_gemini(self, messages: list) -> str:

        """
        messages = [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
        ]
        """
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        MODEL_NAME = "models/gemini-2.5-flash"

        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=messages[0]["content"]
        )

        chat = model.start_chat(history=[])

        response = chat.send_message(
            messages[1]["content"],
            generation_config=genai.types.GenerationConfig(
                temperature=0.2
            )
        )

        return response.text

    
    def _extract_text(self, file_path: str) -> str:
        path = Path(file_path)

        if path.suffix.lower() == ".pdf":
            return self._extract_pdf(path)
        elif path.suffix.lower() == ".docx":
            return self._extract_docx(path)
        elif path.suffix.lower() == ".txt":
            return path.read_text(encoding="utf-8")
        else:
            raise ValueError("Unsupported file format")

    def _extract_pdf(path: Path) -> str:
        text = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)

    def _extract_docx(path: Path) -> str:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    
    def _normalize_resume(self, text: str) -> str:
        text = re.sub(r"\r", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[•●▪]", "-", text)
        return text.strip()

    def _analyze_resume(
            self,
            resume_text: str,
            target_role: str = "General",
            experience_level: str = "Unknown"
        ) -> ResumeAnalysis:

        SYSTEM_PROMPT = """
        You are an expert resume reviewer, recruiter, and ATS optimization specialist.
        You are critical, specific, and practical.
        """
        user_prompt = f"""
        Analyze the resume below.

        Target Role: {target_role}
        Experience Level: {experience_level}

        Return STRICT JSON matching this schema:

        {{
        "overall_score": number (0-100),
        "summary": [string],
        "section_feedback": {{
            "experience": {{
            "issues": [string],
            "suggestions": [string],
            "example_rewrites": [string]
            }}
        }},
        "ats_issues": [string],
        "priority_fixes": [string]
        }}

        Be specific. Provide concrete rewrite examples.

        Resume:
        \"\"\"
        {resume_text}
        \"\"\"
        """

        response = self._call_gemini([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ])

        response = response.replace("```json", " ").strip()
        response = response.replace("```", " ").strip()

        parsed = json.loads(response)
        return ResumeAnalysis(**parsed)
    



    def review_resume(self, resume_path: str):
        raw_text = self._extract_text(resume_path)
        clean_text = self._normalize_resume(raw_text)

        analysis = self._analyze_resume(
            resume_text=clean_text,
            target_role="Backend Engineer", # Example target role
            experience_level="Mid-Senior" # Example experience level
        )

        print("\n=== OVERALL SCORE ===")
        print(analysis.overall_score)

        print("\n=== SUMMARY ===")
        for s in analysis.summary:
            print("-", s)

        print("\n=== PRIORITY FIXES ===")
        for p in analysis.priority_fixes:
            print("-", p)

    


