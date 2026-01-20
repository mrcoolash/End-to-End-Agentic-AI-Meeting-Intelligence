"""
Meeting Minutes AI Agent using Phidata and Google Gemini
"""
import json
import time
from typing import Dict, List, Optional, Tuple
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class MeetingMinutesAgent:
    def __init__(self):
        # Configure Gemini AI
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        
        # Initialize Phidata agent with Gemini model
        self.agent = Agent(
            name="Meeting Minutes Specialist",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo()],
            markdown=True,
        )
    
    def process_meeting_transcript(
        self, 
        transcript: str, 
        agenda: Optional[str] = None,
        meeting_title: str = "Meeting"
    ) -> Dict:
        """
        Process meeting transcript and extract structured information
        
        Args:
            transcript: The meeting transcript text
            agenda: Optional agenda items
            meeting_title: Title of the meeting
            
        Returns:
            Dict containing summary, decisions, action items, and agenda coverage
        """
        start_time = time.time()
        
        # Build the prompt for structured extraction
        prompt = self._build_extraction_prompt(transcript, agenda, meeting_title)
        
        try:
            # Process with AI agent
            response = self.agent.run(prompt)
            result = self._parse_agent_response(response.content)
            
            # Add timing information
            result['processing_time'] = time.time() - start_time
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def _build_extraction_prompt(self, transcript: str, agenda: Optional[str], meeting_title: str) -> str:
        """Build the prompt for extracting meeting information"""
        
        agenda_section = ""
        if agenda:
            agenda_section = f"""
            **MEETING AGENDA:**
            {agenda}
            
            **AGENDA ANALYSIS REQUIRED:**
            - Identify which agenda items were discussed in the transcript
            - Mark items as "covered" or "not covered"
            - Provide specific evidence from transcript for covered items
            """
        
        prompt = f"""
        You are a professional meeting minutes specialist. Analyze the following meeting transcript and extract structured information.
        
        **MEETING TITLE:** {meeting_title}
        
        **MEETING TRANSCRIPT:**
        {transcript}
        
        {agenda_section}
        
        **REQUIRED OUTPUT FORMAT (JSON):**
        Please provide your analysis in the following JSON structure:
        
        {{
            "summary": "3-7 sentence summary of the meeting highlighting key topics and outcomes",
            "decisions": [
                "List of specific decisions made during the meeting (if any)"
            ],
            "action_items": [
                {{
                    "description": "Clear description of the action item",
                    "owner": "Person responsible (extract from transcript if mentioned, otherwise null)",
                    "due_date": "Due date or timeframe mentioned (extract if present, otherwise null)"
                }}
            ],
            "agenda_coverage": {{
                "status": "covered|not_covered|no_agenda",
                "covered_items": [
                    {{
                        "item": "agenda item text",
                        "evidence": "specific quote or reference from transcript"
                    }}
                ],
                "uncovered_items": [
                    "agenda items not discussed"
                ]
            }},
            "participants": [
                "Names of people who spoke (extract from transcript)"
            ],
            "key_topics": [
                "Main topics discussed"
            ]
        }}
        
        **EXTRACTION GUIDELINES:**
        1. **Summary**: Focus on concrete details, decisions, and outcomes
        2. **Decisions**: Only include explicit decisions, not discussions
        3. **Action Items**: Extract specific tasks with clear ownership when possible
        4. **Participants**: Extract names mentioned as speakers in the transcript
        5. **Agenda Coverage**: If no agenda provided, set status to "no_agenda"
        6. **Be Specific**: Reference concrete details from the transcript, not generic statements
        
        Ensure the output is valid JSON format.
        """
        
        return prompt
    
    def _parse_agent_response(self, response_content: str) -> Dict:
        """Parse the agent response and extract JSON data"""
        try:
            # Try to find JSON in the response
            start_idx = response_content.find('{')
            end_idx = response_content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_content[start_idx:end_idx]
                data = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['summary', 'decisions', 'action_items']
                for field in required_fields:
                    if field not in data:
                        data[field] = [] if field != 'summary' else ""
                
                # Ensure agenda_coverage exists
                if 'agenda_coverage' not in data:
                    data['agenda_coverage'] = {
                        'status': 'no_agenda',
                        'covered_items': [],
                        'uncovered_items': []
                    }
                
                data['success'] = True
                return data
            else:
                # Fallback: try to extract information manually
                return self._fallback_parsing(response_content)
                
        except json.JSONDecodeError:
            return self._fallback_parsing(response_content)
    
    def _fallback_parsing(self, response_content: str) -> Dict:
        """Fallback parsing if JSON extraction fails"""
        return {
            'success': False,
            'raw_response': response_content,
            'summary': "Error: Could not parse AI response into structured format",
            'decisions': [],
            'action_items': [],
            'agenda_coverage': {
                'status': 'error',
                'covered_items': [],
                'uncovered_items': []
            },
            'participants': [],
            'key_topics': [],
            'error': 'Failed to parse structured response'
        }
    
    def quick_summarize(self, transcript: str) -> str:
        """Quick summary for immediate feedback"""
        if not transcript.strip():
            return "No transcript provided"
        
        if len(transcript) > 10000:
            return "Transcript too long (max 10,000 characters)"
        
        prompt = f"""
        Provide a concise 2-3 sentence summary of this meeting transcript:
        
        {transcript[:2000]}...
        
        Focus on the main topics and any key decisions or outcomes.
        """
        
        try:
            response = self.agent.run(prompt)
            return response.content.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"