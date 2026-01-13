import os
import json
import re
from typing import Optional, Dict, List, Any, Callable
import requests
from app.config import settings


class GeminiService:
    """
    GeminiService using OpenRouter (Gemini Free Model)
    Model: google/gemini-2.0-flash-exp:free
    """
    
    def __init__(self):
        self.model = "google/gemini-2.0-flash-exp:free"
        # Try to get API key from multiple sources
        self.api_key = (
            settings.GEMINI_API_KEY or 
            os.getenv("GEMINI_API_KEY") or 
            os.getenv("OPENROUTER_API_KEY") or
            "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"  # Fallback key from test.py
        )
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self._update_headers()
        print(f"GeminiService initialized. API Key present: {bool(self.api_key)}")
    
    def _update_headers(self):
        """Update headers with current API key"""
        self.headers = {
            "Content-Type": "application/json",
            "HTTP-Referer": "https://prepwise.com",  # Optional: for analytics
            "X-Title": "PrepWise Interview Platform"  # Optional: for analytics
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def _make_request(self, prompt: str) -> Optional[str]:
        """Make a request to OpenRouter API"""
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not set, using fallback responses")
            print("Please set GEMINI_API_KEY or OPENROUTER_API_KEY environment variable")
            return None
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            print(f"Making request to OpenRouter API (model: {self.model})...")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            print(f"API Response status: {response.status_code}")
            
            if data.get("choices") and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                if content:
                    print(f"Successfully received response from API")
                    return content.strip()
            
            print(f"Warning: No content in response. Response keys: {list(data.keys())}")
            if "error" in data:
                print(f"API Error: {data.get('error')}")
            return None
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None:
                error_msg = f"HTTP {e.response.status_code}"
                try:
                    error_data = e.response.json()
                    error_detail = error_data.get('error', {}).get('message', e.response.text[:200])
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f": {e.response.text[:200]}"
                print(f"OpenRouter API HTTP error: {error_msg}")
            else:
                print(f"OpenRouter API HTTP error: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"OpenRouter API request error: {str(e)}")
            return None
        except Exception as error:
            print(f"OpenRouter API unexpected error: {type(error).__name__}: {str(error)}")
            import traceback
            print(traceback.format_exc())
            return None

    # ============================================================
    # QUESTION GENERATION
    # ============================================================

    async def generate_question(
        self,
        interview_type: str,
        question_number: int,
        previous_answers: Optional[List[str]] = None,
        resume_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate an interview question"""
        try:
            prompt = self._build_context_prompt(
                interview_type,
                question_number,
                previous_answers or [],
                resume_data
            )
            
            print(f"[GeminiService] Generating question {question_number} for {interview_type} interview...")
            print(f"[GeminiService] API Key available: {bool(self.api_key)}")
            
            result = self._make_request(prompt)
            
            if result and result.strip():
                print(f"[GeminiService] Successfully generated question: {result[:100]}...")
                return result.strip()
            else:
                print(f"[GeminiService] API returned empty result, using fallback question")
                fallback = self._get_fallback_question(interview_type, question_number)
                print(f"[GeminiService] Using fallback: {fallback}")
                return fallback
        except Exception as e:
            import traceback
            print(f"[GeminiService] Error in generate_question: {type(e).__name__}: {str(e)}")
            print(traceback.format_exc())
            fallback = self._get_fallback_question(interview_type, question_number)
            print(f"[GeminiService] Using fallback after error: {fallback}")
            return fallback

    # ============================================================
    # ANSWER ANALYSIS
    # ============================================================

    async def analyze_answer(
        self,
        question: str,
        answer: str,
        interview_type: str
    ) -> Dict[str, Any]:
        """Analyze a candidate's answer"""
        prompt = f"""
You are an expert interviewer.

Interview Type: {interview_type}
Question: {question}
Candidate Answer: {answer}

Evaluate the answer and provide:
SCORE: (0-100)
FEEDBACK: (2-3 lines)
STRENGTHS: (2-3 bullet points)
IMPROVEMENTS: (2-3 bullet points)

Return only the evaluation.
"""
        
        result = self._make_request(prompt)
        if result:
            return self._parse_analysis_response(result)
        
        return self._get_default_analysis()

    # ============================================================
    # FINAL INTERVIEW FEEDBACK
    # ============================================================

    async def generate_final_feedback(
        self,
        interview_type: str,
        all_qa_pairs: List[Dict[str, str]],
        emotion_analysis: Optional[Dict[str, Any]] = None,
        video_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate final feedback for the interview"""
        prompt = f"Generate final feedback for a {interview_type} interview.\n\n"
        
        for index, qa in enumerate(all_qa_pairs, 1):
            prompt += f"{index}. Question: {qa.get('question', '')}\n"
            prompt += f"Answer: {qa.get('answer', '')}\n\n"
        
        if emotion_analysis:
            prompt += f"Emotion Analysis:\n{json.dumps(emotion_analysis)}\n\n"
        
        if video_analysis:
            prompt += f"Video Analysis:\n{json.dumps(video_analysis)}\n\n"
        
        prompt += """
Provide:
1. Overall Score (0-100)
2. Score Breakdown (content, communication, confidence)
3. Top Strengths
4. Areas of Improvement
5. Final Summary Paragraph
"""
        
        result = self._make_request(prompt)
        if result:
            return self._parse_feedback_response(result, all_qa_pairs)
        
        return self._get_default_feedback()

    # ============================================================
    # STREAMING RESPONSE (OPTIONAL)
    # ============================================================

    async def stream_response(self, prompt: str, on_token: Optional[Callable[[str], None]] = None):
        """Stream response from OpenRouter"""
        if not self.api_key:
            return
        
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            data = json.loads(data_str)
                            token = data.get("choices", [{}])[0].get("delta", {}).get("content")
                            if token and on_token:
                                on_token(token)
                        except json.JSONDecodeError:
                            continue
        except Exception as error:
            print(f"OpenRouter streaming error: {error}")

    # ============================================================
    # PROMPT BUILDERS
    # ============================================================

    def _build_context_prompt(
        self,
        interview_type: str,
        question_number: int,
        previous_answers: List[str],
        resume_data: Optional[Dict[str, Any]]
    ) -> str:
        """Build context prompt for question generation"""
        type_contexts = {
            "hr": "HR interview focusing on behavior, attitude, and soft skills",
            "technical": "Technical interview focusing on coding, logic, and problem-solving",
            "gd": "Group discussion focusing on communication and opinion sharing"
        }
        
        prompt = f"""You are an expert interviewer conducting a {type_contexts.get(interview_type, "General Interview")}.

Generate interview question number {question_number}.

IMPORTANT: Return ONLY the question text, nothing else. No explanations, no prefixes, just the question.

Guidelines:
- Make it clear, concise, and professional
- Relevant to {interview_type} interview type
- If this is question 1, start with an opening/introductory question
- If previous answers exist, ask a thoughtful follow-up question
- Keep it conversational and engaging"""
        
        if resume_data and resume_data.get("skills"):
            skills = resume_data["skills"]
            if isinstance(skills, list) and len(skills) > 0:
                prompt += f"\n\nCandidate has skills in: {', '.join(skills[:10])}"
            elif isinstance(skills, str):
                prompt += f"\n\nCandidate skills: {skills}"
        
        if previous_answers and len(previous_answers) > 0:
            prompt += "\n\nPrevious answers from candidate:"
            for i, ans in enumerate(previous_answers[-3:], 1):
                # Truncate long answers
                ans_preview = ans[:200] + "..." if len(ans) > 200 else ans
                prompt += f"\n{i}. {ans_preview}"
            prompt += "\n\nAsk a follow-up question based on their previous answers."
        
        prompt += "\n\nGenerate the question now:"
        return prompt.strip()

    # ============================================================
    # PARSERS
    # ============================================================

    def _parse_analysis_response(self, text: str) -> Dict[str, Any]:
        """Parse analysis response from AI"""
        return {
            "raw": text,
            "score": self._extract_number(text) or 75,
            "feedback": text,
            "strengths": self._extract_list_items(text, "STRENGTHS", "strengths"),
            "improvements": self._extract_list_items(text, "IMPROVEMENTS", "improvements")
        }
    
    def _parse_feedback_response(
        self,
        text: str,
        all_qa_pairs: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Parse final feedback response from AI"""
        overall_score = self._extract_number(text) or 75
        
        # Extract scores breakdown
        scores = {
            "content": self._extract_score_from_text(text, "content") or 75,
            "communication": self._extract_score_from_text(text, "communication") or 75,
            "confidence": self._extract_score_from_text(text, "confidence") or 75
        }
        
        return {
            "raw": text,
            "overall_score": overall_score,
            "scores": scores,
            "strengths": self._extract_list_items(text, "strengths", "top strengths"),
            "weaknesses": self._extract_list_items(text, "improvements", "areas of improvement"),
            "detailed_feedback": text
        }
    
    def _extract_number(self, text: str) -> Optional[int]:
        """Extract first number from text (0-100)"""
        # Look for score patterns like "SCORE: 85" or "85/100" or just "85"
        patterns = [
            r'SCORE:\s*(\d{1,3})',
            r'score:\s*(\d{1,3})',
            r'(\d{1,3})\s*/?\s*100',
            r'\b(\d{1,2})\b'  # Fallback: any 1-2 digit number
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                num = int(match.group(1))
                if 0 <= num <= 100:
                    return num
        
        return None
    
    def _extract_score_from_text(self, text: str, keyword: str) -> Optional[int]:
        """Extract score for a specific keyword"""
        pattern = rf'{keyword}.*?(\d{{1,3}})'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            if 0 <= num <= 100:
                return num
        return None
    
    def _extract_list_items(self, text: str, *keywords: str) -> List[str]:
        """Extract list items from text based on keywords"""
        items = []
        lines = text.split('\n')
        capturing = False
        
        for line in lines:
            line_lower = line.lower()
            # Check if we hit a keyword section
            if any(keyword.lower() in line_lower for keyword in keywords):
                capturing = True
                continue
            
            # Stop if we hit another major section
            if capturing and any(keyword in line_lower for keyword in ["improvements", "feedback", "score", "summary"]):
                if not any(kw in line_lower for kw in keywords):
                    break
            
            # Capture bullet points or numbered items
            if capturing:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('*') or 
                           re.match(r'^\d+[\.\)]', line)):
                    item = re.sub(r'^[-*\d+\.\)]\s*', '', line).strip()
                    if item:
                        items.append(item)
        
        return items[:5] if items else ["See detailed feedback"]

    # ============================================================
    # FALLBACKS
    # ============================================================

    def _get_fallback_question(self, interview_type: str, number: int) -> str:
        """Get fallback question if API fails"""
        fallback = {
            "hr": [
                "Tell me about yourself.",
                "What are your strengths?",
                "Why should we hire you?",
                "Where do you see yourself in 5 years?",
                "How do you handle stress?"
            ],
            "technical": [
                "Explain a project you worked on.",
                "How do you debug code?",
                "Explain OOP concepts.",
                "What is your approach to testing?",
                "How do you optimize database queries?"
            ],
            "gd": [
                "What is teamwork?",
                "What are the pros and cons of remote work?",
                "Is AI a threat to jobs?",
                "How important is communication in a team?",
                "What makes a good leader?"
            ]
        }
        
        questions = fallback.get(interview_type, fallback["hr"])
        return questions[(number - 1) % len(questions)]
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default analysis if API fails"""
        return {
            "score": 75,
            "feedback": "Good answer, but needs improvement.",
            "strengths": ["Relevant response", "Shows understanding"],
            "improvements": ["More clarity needed", "Could provide more examples"]
        }
    
    def _get_default_feedback(self) -> Dict[str, Any]:
        """Get default feedback if API fails"""
        return {
            "overall_score": 75,
            "scores": {
                "content": 75,
                "communication": 75,
                "confidence": 75
            },
            "strengths": ["Completed interview successfully", "Showed engagement"],
            "weaknesses": ["Needs more practice", "Could improve clarity"],
            "detailed_feedback": "Keep practicing to improve performance. Focus on providing specific examples and clearer explanations."
        }
