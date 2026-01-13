from typing import Dict, List, Any, Optional
from datetime import datetime
from app.services.gemini_service import GeminiService
import random


class GDService:
    """Service for Group Discussion functionality"""
    
    def __init__(self):
        self.gemini = GeminiService()
    
    # AI Participants with fixed personalities
    AI_PARTICIPANTS = [
        {
            "id": "leader",
            "name": "Alex",
            "personality": "Leader",
            "traits": ["initiates discussions", "summarizes points", "keeps group focused", "moderates"],
            "speech_style": "Confident and directive, often starts topics and wraps up discussions"
        },
        {
            "id": "aggressive",
            "name": "Sam",
            "personality": "Aggressive",
            "traits": ["interrupts others", "challenges viewpoints", "assertive", "competitive"],
            "speech_style": "Direct and confrontational, frequently interrupts and questions others"
        },
        {
            "id": "logical",
            "name": "Jordan",
            "personality": "Logical",
            "traits": ["fact-based", "structured thinking", "gives examples", "analytical"],
            "speech_style": "Clear and structured, provides facts, data, and examples"
        },
        {
            "id": "silent",
            "name": "Riley",
            "personality": "Silent/Observer",
            "traits": ["speaks rarely", "listens carefully", "makes impactful points when speaking"],
            "speech_style": "Thoughtful and selective, speaks less but with meaningful contributions"
        }
    ]
    
    def create_ai_participants(self) -> List[Dict[str, Any]]:
        """Create AI participants with fixed personalities"""
        return self.AI_PARTICIPANTS.copy()
    
    async def generate_topic(self) -> str:
        """Generate a dynamic GD topic using AI"""
        topics_pool = [
            "Should social media platforms be held accountable for spreading fake news?",
            "Is remote work the future of corporate culture?",
            "Should artificial intelligence be regulated by governments?",
            "Is online education as effective as traditional classroom learning?",
            "Should college degrees be mandatory for all high-paying jobs?",
            "Is universal basic income a solution to automation-related job loss?",
            "Should voting be made compulsory in democratic countries?",
            "Is cryptocurrency the future of financial transactions?",
            "Should companies prioritize diversity over merit in hiring?",
            "Is climate change the most pressing global issue today?"
        ]
        
        # For MVP, use random selection from pool
        # In production, could use AI to generate unique topics
        topic = random.choice(topics_pool)
        
        # Optional: Use AI to generate topic if gemini is available
        try:
            prompt = f"""Generate a realistic placement-style Group Discussion topic. 
The topic should be:
- Relevant to current issues (technology, social, business, abstract)
- Suitable for campus placement interviews
- Open-ended with multiple perspectives

Return ONLY the topic text, nothing else."""
            
            ai_topic = self.gemini._make_request(prompt)
            if ai_topic and len(ai_topic.strip()) > 10:
                return ai_topic.strip()
        except:
            pass
        
        return topic
    
    async def get_ai_responses(
        self,
        topic: str,
        conversation_history: List[Dict],
        ai_participants: List[Dict],
        student_message: str
    ) -> List[Dict[str, Any]]:
        """Get AI participant responses based on their personalities"""
        responses = []
        
        # Determine which AI participants should respond (not all always)
        # Leader responds more frequently, Silent responds rarely
        response_probabilities = {
            "leader": 0.7,
            "aggressive": 0.6,
            "logical": 0.65,
            "silent": 0.25  # Silent speaks rarely
        }
        
        # Determine who responds
        responding_participants = []
        for participant in ai_participants:
            if random.random() < response_probabilities.get(participant["id"], 0.5):
                responding_participants.append(participant)
        
        # If no one responds, ensure at least one does (usually leader)
        if not responding_participants:
            responding_participants = [ai_participants[0]]  # Leader
        
        # Generate responses for each responding participant
        for participant in responding_participants:
            response = await self._generate_ai_response(
                participant=participant,
                topic=topic,
                conversation_history=conversation_history,
                student_message=student_message
            )
            
            if response:
                responses.append({
                    "speaker": participant["id"],
                    "speaker_name": participant["name"],
                    "message": response["message"],
                    "action": response.get("action", "speaks"),  # speaks, interrupts, agrees, disagrees
                    "timestamp": datetime.utcnow().isoformat(),
                    "personality": participant["personality"]
                })
        
        return responses
    
    async def _generate_ai_response(
        self,
        participant: Dict,
        topic: str,
        conversation_history: List[Dict],
        student_message: str
    ) -> Optional[Dict[str, Any]]:
        """Generate response for a specific AI participant based on their personality"""
        try:
            # Build context from conversation history
            recent_context = "\n".join([
                f"{msg.get('speaker_name', msg.get('speaker', 'Unknown'))}: {msg['message']}"
                for msg in conversation_history[-5:]
            ])
            
            prompt = f"""You are {participant['name']}, a participant in a Group Discussion.

Topic: {topic}

Your Personality: {participant['personality']}
Your Traits: {', '.join(participant['traits'])}
Your Speech Style: {participant['speech_style']}

Recent conversation:
{recent_context}

Student just said: "{student_message}"

Based on your personality, respond naturally. You can:
- Agree or disagree with the student
- Add your perspective
- Interrupt if you're the aggressive type
- Provide facts/examples if you're logical
- Stay concise if you're silent/observer
- Summarize if you're the leader

Return your response (1-3 sentences, natural conversational style)."""
            
            response_text = self.gemini._make_request(prompt)
            
            if not response_text:
                # Fallback response based on personality
                response_text = self._get_fallback_response(participant, student_message)
            
            # Determine action type
            action = "speaks"
            if participant["id"] == "aggressive" and random.random() < 0.4:
                action = "interrupts"
            elif "agree" in response_text.lower() or "yes" in response_text.lower():
                action = "agrees"
            elif "disagree" in response_text.lower() or "but" in response_text.lower():
                action = "disagrees"
            
            return {
                "message": response_text.strip() if response_text else "",
                "action": action
            }
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return {
                "message": self._get_fallback_response(participant, student_message),
                "action": "speaks"
            }
    
    def _get_fallback_response(self, participant: Dict, student_message: str) -> str:
        """Fallback responses based on personality"""
        fallbacks = {
            "leader": [
                "That's a good point. Let me add that we should also consider...",
                "I think we're on the right track. To summarize what's been said...",
                "Building on that, I'd like to emphasize..."
            ],
            "aggressive": [
                "I disagree with that perspective. Here's why...",
                "Wait, I need to challenge that point because...",
                "That's not entirely accurate. Let me correct..."
            ],
            "logical": [
                "From a data perspective, studies show that...",
                "To support this point, here's an example...",
                "Looking at this logically, we should consider..."
            ],
            "silent": [
                "I think we should also consider...",
                "One more point to add...",
                "I agree, and would like to add..."
            ]
        }
        return random.choice(fallbacks.get(participant["id"], ["That's an interesting point."]))
    
    async def evaluate_gd_performance(
        self,
        topic: str,
        conversation_history: List[Dict],
        behavior_tracking: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate student's GD performance based on behavior"""
        try:
            # Build evaluation prompt
            behavior_summary = f"""
Student Participation Metrics:
- Total times student spoke: {behavior_tracking.get('student_speaks_count', 0)}
- Initiated discussion: {'Yes' if behavior_tracking.get('student_initiated') else 'No'}
- Number of interruptions: {behavior_tracking.get('student_interruptions', 0)}
- Times interrupted: {behavior_tracking.get('student_interrupted_count', 0)}
- Summarized discussion: {'Yes' if behavior_tracking.get('student_summarized') else 'No'}
- Concluded discussion: {'Yes' if behavior_tracking.get('student_concluded') else 'No'}
"""
            
            conversation_text = "\n".join([
                f"{msg.get('speaker_name', msg.get('speaker', 'Unknown'))}: {msg['message']}"
                for msg in conversation_history
            ])
            
            prompt = f"""You are evaluating a student's performance in a Group Discussion.

Topic: {topic}

{behavior_summary}

Full Conversation:
{conversation_text}

Evaluate the student's performance based on:
1. Communication clarity & confidence (0-10)
2. Content relevance & structure (0-10)
3. Participation level (0-10)
4. Team behavior (respect, interruptions, listening) (0-10)
5. Leadership signals (initiative, summary, direction) (0-10)

Consider behavior during discussion, not just answer quality.

Return a JSON object with this exact structure:
{{
    "overall_score": <number 0-10>,
    "scores": {{
        "communication": <number 0-10>,
        "content": <number 0-10>,
        "participation": <number 0-10>,
        "team_behavior": <number 0-10>,
        "leadership": <number 0-10>
    }},
    "strengths": [<array of 3-5 strength strings>],
    "weaknesses": [<array of 3-5 weakness strings>],
    "role_suitability": "<one role: Analyst, Leader, Consultant, Team Player, Observer>",
    "improvement_suggestions": [<array of 3-5 actionable suggestions>],
    "detailed_feedback": "<2-3 paragraph detailed feedback>"
}}

Return ONLY valid JSON, no other text."""
            
            response = self.gemini._make_request(prompt)
            
            if response:
                # Try to parse JSON from response
                import json
                import re
                
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    eval_data = json.loads(json_match.group())
                    return eval_data
            
            # Fallback evaluation
            return self._get_fallback_evaluation(behavior_tracking)
            
        except Exception as e:
            print(f"Error in GD evaluation: {e}")
            return self._get_fallback_evaluation(behavior_tracking)
    
    def _get_fallback_evaluation(self, behavior_tracking: Dict) -> Dict[str, Any]:
        """Fallback evaluation based on behavior metrics"""
        speaks_count = behavior_tracking.get('student_speaks_count', 0)
        initiated = behavior_tracking.get('student_initiated', False)
        summarized = behavior_tracking.get('student_summarized', False)
        
        # Calculate scores based on behavior
        participation_score = min(10, speaks_count * 2)
        communication_score = 7 if speaks_count > 0 else 5
        leadership_score = 6
        if initiated:
            leadership_score += 2
        if summarized:
            leadership_score += 2
        
        overall = (participation_score + communication_score + leadership_score + 7 + 7) / 5
        
        return {
            "overall_score": round(overall, 1),
            "scores": {
                "communication": communication_score,
                "content": 7,
                "participation": participation_score,
                "team_behavior": 7,
                "leadership": leadership_score
            },
            "strengths": [
                "Participated in the discussion",
                "Engaged with the topic"
            ] if speaks_count > 0 else ["Attempted to engage"],
            "weaknesses": [
                "Could speak more frequently" if speaks_count < 3 else "Good participation",
                "Could take more initiative" if not initiated else "Showed initiative"
            ],
            "role_suitability": "Team Player" if speaks_count < 5 else "Leader",
            "improvement_suggestions": [
                "Practice speaking more frequently in group settings",
                "Work on initiating discussions",
                "Learn to summarize key points effectively"
            ],
            "detailed_feedback": f"Student participated {speaks_count} times in the discussion. "
                               f"{'Initiated the discussion' if initiated else 'Did not initiate the discussion'}. "
                               f"Focus on increasing participation and taking leadership roles."
        }

