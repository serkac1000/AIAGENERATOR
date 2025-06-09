"""
AI Agent module for processing prompts and generating app structures
Uses Google AI (Gemini) API for intelligent app generation
"""

import google.generativeai as genai
import json
import base64
import logging
from PIL import Image
import io

class AIAgent:
    def __init__(self, api_key):
        """Initialize AI agent with Google AI API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def test_connection(self):
        """Test if the API key works"""
        try:
            response = self.model.generate_content("Hello")
            return bool(response.text)
        except Exception as e:
            logging.error(f"API connection test failed: {str(e)}")
            return False
            
    def generate_app_structure(self, prompt, image_path=None):
        """Generate MIT App Inventor app structure from prompt and optional image"""
        try:
            # Prepare the content for the AI model
            content_parts = []
            
            # Add the main prompt with specific instructions for MIT App Inventor
            ai_prompt = self._create_detailed_prompt(prompt)
            content_parts.append(ai_prompt)
            
            # Add image if provided
            if image_path:
                try:
                    image_data = self._process_image(image_path)
                    if image_data:
                        content_parts.append(image_data)
                        content_parts.append("Please analyze this image and incorporate any UI design elements, colors, or layout ideas into the app structure.")
                except Exception as e:
                    logging.warning(f"Failed to process image: {str(e)}")
            
            # Generate content using AI
            response = self.model.generate_content(content_parts)
            
            if not response.text:
                raise Exception("Empty response from AI model")
                
            # Parse the AI response to extract app structure
            app_data = self._parse_ai_response(response.text)
            
            return app_data
            
        except Exception as e:
            logging.error(f"Failed to generate app structure: {str(e)}")
            raise
            
    def _create_detailed_prompt(self, user_prompt):
        """Create a detailed prompt for MIT App Inventor app generation"""
        return f"""
You are an expert MIT App Inventor developer. Create a complete app structure based on this description: "{user_prompt}"

Please provide a JSON response with the following structure:

{{
    "app_name": "AppName",
    "description": "Brief description of the app",
    "screens": [
        {{
            "name": "Screen1",
            "title": "Screen Title",
            "components": [
                {{
                    "type": "Button",
                    "name": "Button1",
                    "text": "Click Me",
                    "properties": {{
                        "BackgroundColor": "#FF0000",
                        "TextColor": "#FFFFFF",
                        "Width": "-2",
                        "Height": "-2"
                    }}
                }},
                {{
                    "type": "Label",
                    "name": "Label1",
                    "text": "Hello World",
                    "properties": {{
                        "TextSize": "18",
                        "TextAlignment": "1"
                    }}
                }}
            ],
            "layout": {{
                "arrangement": "VerticalArrangement",
                "alignment": "Center"
            }}
        }}
    ],
    "blocks": [
        {{
            "event": "Button1.Click",
            "action": "set Label1.Text to 'Button clicked!'"
        }}
    ],
    "assets": [],
    "permissions": []
}}

Make sure to:
1. Create meaningful component names and properties
2. Include appropriate blocks for functionality
3. Use proper MIT App Inventor component types (Button, Label, TextBox, Image, etc.)
4. Set reasonable default properties
5. Create logical screen layouts
6. Include necessary permissions if the app uses camera, location, etc.

Response must be valid JSON only, no additional text or explanations.
"""

    def _process_image(self, image_path):
        """Process and prepare image for AI analysis"""
        try:
            # Open and resize image if too large
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large (max 1024x1024 for API efficiency)
                max_size = (1024, 1024)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Convert to bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr = img_byte_arr.getvalue()
                
                # Create image data for Gemini
                return {
                    "mime_type": "image/jpeg",
                    "data": img_byte_arr
                }
                
        except Exception as e:
            logging.error(f"Failed to process image {image_path}: {str(e)}")
            return None
            
    def _parse_ai_response(self, response_text):
        """Parse AI response and extract app structure"""
        try:
            # Clean the response text
            response_text = response_text.strip()
            
            # Find JSON content (sometimes AI adds extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise Exception("No JSON found in AI response")
                
            json_text = response_text[start_idx:end_idx]
            
            # Parse JSON
            app_data = json.loads(json_text)
            
            # Validate required fields
            required_fields = ['app_name', 'screens']
            for field in required_fields:
                if field not in app_data:
                    raise Exception(f"Missing required field: {field}")
                    
            # Set default values for optional fields
            if 'description' not in app_data:
                app_data['description'] = f"Generated app: {app_data['app_name']}"
                
            if 'blocks' not in app_data:
                app_data['blocks'] = []
                
            if 'assets' not in app_data:
                app_data['assets'] = []
                
            if 'permissions' not in app_data:
                app_data['permissions'] = []
                
            return app_data
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON from AI response: {str(e)}")
            logging.error(f"Response text: {response_text}")
            raise Exception("AI returned invalid JSON response")
            
        except Exception as e:
            logging.error(f"Failed to parse AI response: {str(e)}")
            raise
