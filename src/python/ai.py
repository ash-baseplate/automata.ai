"""
AI-powered automata analyzer module.

This module provides functionality to analyze images of automata diagrams
using Mistral AI's vision capabilities to extract states, symbols, and transitions.
"""

import base64
from mistralai import Mistral
import os

class AutomataAnalyzer:
    """
    A class for analyzing automata diagrams using AI vision models.
    
    This class uses Mistral AI's vision capabilities to extract information
    from images of automata diagrams, including states, symbols, and transitions.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the AutomataAnalyzer.
        
        Args:
            api_key (str, optional): Mistral API key. If not provided, 
                                     attempts to get from environment.
        """
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        self.client = Mistral(api_key=self.api_key) if self.api_key else None
        self.system_instructions = """
        1)States: Identify all states and rename them sequentially as q0, q1, q2, ..., regardless of their original labels.
        2)Input Symbols: Detect all distinct symbols used in transitions.
        3)Start State: Identify the unique start state.
        4)Accepting States: Identify all accepting states.
        5)Transitions: Extract all valid transitions in the format: fromState symbol toState
            Ensure every transition present in the NFA is captured.
            No transitions should be missing, duplicated, or altered.
            
        Your response must strictly follow this structure without additional explanations, symbols, or formatting artifacts (e.g., quotes, extra spaces, or newlines):
        Enter number of states: <num_states>  
        Enter states: <list_of_states>  
        Enter number of symbols: <num_symbols>  
        Enter symbols (separate by space): <symbols>  
        Enter start state: <start_state>  
        Enter number of accepting states: <num_accepting_states>  
        Enter accepting states: <accepting_states>  
        Enter number of transitions: <num_transitions>  
        Enter transition (fromState symbol toState): <fromState> <symbol> <toState>  

        The number of states, symbols, and transitions must be correctly counted.
        The output must not contain any extra text, explanations, or formatting beyond what is specified.
        """

    def encode_image(self, uploaded_file):
        """
        Encode uploaded file to base64.
        
        Args:
            uploaded_file: The uploaded file object from Streamlit
            
        Returns:
            str: Base64 encoded image string
            
        Raises:
            ValueError: If image encoding fails
        """
        try:
            return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Image encoding failed: {e}")

    def analyze(self, image_data):
        """
        Analyze image using Mistral's API.
        
        Args:
            image_data (str): Base64 encoded image data
            
        Returns:
            str: Cleaned analysis result
            
        Raises:
            ValueError: If Mistral client is not initialized
        """
        if not self.client:
            raise ValueError("Mistral API client not initialized")
            
        messages = [
            {
                "role": "system",
                "content": self.system_instructions
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze the image"},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data}"}
                ]
            }
        ]
        
        response = self.client.chat.complete(
            model="pixtral-12b-2409",
            messages=messages
        )
        raw_output = response.choices[0].message.content
        return self.clean_output(raw_output)

    def clean_output(self, raw_text):
        """
        Clean and format the AI output.
        
        Args:
            raw_text (str): Raw output from the AI
            
        Returns:
            str: Cleaned and formatted output
        """
        # Remove markdown code blocks
        cleaned = raw_text.replace('```', '')
        
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # Add your additional cleaning steps here
        
        return cleaned