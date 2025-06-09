"""
Utility functions for the AIA Generator application
"""

import os
import logging
import json
import re
from pathlib import Path

def validate_app_name(name):
    """Validate app name for MIT App Inventor compatibility"""
    if not name:
        return False, "App name cannot be empty"
        
    # App Inventor naming rules
    if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', name):
        return False, "App name must start with a letter and contain only letters, numbers, and underscores"
        
    if len(name) > 50:
        return False, "App name must be 50 characters or less"
        
    # Reserved words in App Inventor
    reserved_words = [
        'and', 'or', 'not', 'if', 'then', 'else', 'define', 'lambda',
        'let', 'begin', 'do', 'while', 'for', 'foreach'
    ]
    
    if name.lower() in reserved_words:
        return False, f"'{name}' is a reserved word and cannot be used as app name"
        
    return True, "Valid app name"

def sanitize_component_name(name):
    """Sanitize component name for App Inventor compatibility"""
    if not name:
        return "Component1"
        
    # Remove invalid characters and ensure it starts with a letter
    sanitized = re.sub(r'[^A-Za-z0-9_]', '', name)
    
    if not sanitized or not sanitized[0].isalpha():
        sanitized = "Component" + sanitized
        
    return sanitized[:30]  # Limit length

def validate_component_properties(component_type, properties):
    """Validate component properties for MIT App Inventor"""
    valid_properties = {
        'Button': {
            'BackgroundColor': 'color',
            'Enabled': 'boolean',
            'FontBold': 'boolean',
            'FontItalic': 'boolean',
            'FontSize': 'number',
            'FontTypeface': 'string',
            'Height': 'string',
            'Image': 'string',
            'Shape': 'number',
            'ShowFeedback': 'boolean',
            'Text': 'string',
            'TextAlignment': 'number',
            'TextColor': 'color',
            'Visible': 'boolean',
            'Width': 'string'
        },
        'Label': {
            'BackgroundColor': 'color',
            'FontBold': 'boolean',
            'FontItalic': 'boolean',
            'FontSize': 'number',
            'FontTypeface': 'string',
            'HTMLFormat': 'boolean',
            'Height': 'string',
            'Text': 'string',
            'TextAlignment': 'number',
            'TextColor': 'color',
            'Visible': 'boolean',
            'Width': 'string'
        },
        'TextBox': {
            'BackgroundColor': 'color',
            'Enabled': 'boolean',
            'FontBold': 'boolean',
            'FontItalic': 'boolean',
            'FontSize': 'number',
            'FontTypeface': 'string',
            'Height': 'string',
            'Hint': 'string',
            'MultiLine': 'boolean',
            'NumbersOnly': 'boolean',
            'PasswordTextBox': 'boolean',
            'ReadOnly': 'boolean',
            'Text': 'string',
            'TextAlignment': 'number',
            'TextColor': 'color',
            'Visible': 'boolean',
            'Width': 'string'
        }
    }
    
    valid_props = valid_properties.get(component_type, {})
    validated_props = {}
    
    for prop_name, prop_value in properties.items():
        if prop_name in valid_props:
            # Basic type validation could be added here
            validated_props[prop_name] = prop_value
        else:
            logging.warning(f"Unknown property '{prop_name}' for component type '{component_type}'")
            
    return validated_props

def format_color_value(color):
    """Format color value for App Inventor"""
    if isinstance(color, str):
        # Handle hex colors
        if color.startswith('#'):
            try:
                # Convert hex to App Inventor color format (negative integer)
                hex_color = color[1:]  # Remove #
                rgb_int = int(hex_color, 16)
                # App Inventor uses negative values for colors
                return str(-(rgb_int + 1))
            except ValueError:
                return "&HFF000000"  # Default to black
        # Handle named colors
        color_map = {
            'red': "&HFFFF0000",
            'green': "&HFF00FF00",
            'blue': "&HFF0000FF",
            'white': "&HFFFFFFFF",
            'black': "&HFF000000",
            'yellow': "&HFFFFFF00",
            'cyan': "&HFF00FFFF",
            'magenta': "&HFFFF00FF"
        }
        return color_map.get(color.lower(), "&HFF000000")
    
    return str(color)

def ensure_directory_exists(directory_path):
    """Ensure directory exists, create if necessary"""
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {directory_path}: {str(e)}")
        return False

def get_file_size_mb(file_path):
    """Get file size in megabytes"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception as e:
        logging.error(f"Failed to get file size for {file_path}: {str(e)}")
        return 0

def clean_filename(filename):
    """Clean filename for cross-platform compatibility"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename

def log_system_info():
    """Log system information for debugging"""
    import platform
    import sys
    
    logging.info("System Information:")
    logging.info(f"Platform: {platform.platform()}")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Working directory: {os.getcwd()}")

def format_error_message(error, context=""):
    """Format error message for user display"""
    error_str = str(error)
    
    # Common error translations
    error_translations = {
        "401": "Invalid API key. Please check your Google AI API key.",
        "403": "API access forbidden. Please verify your API key permissions.",
        "429": "API rate limit exceeded. Please try again later.",
        "500": "Google AI service error. Please try again later.",
        "timeout": "Request timeout. Please check your internet connection.",
        "connection": "Connection failed. Please check your internet connection."
    }
    
    for key, message in error_translations.items():
        if key in error_str.lower():
            return f"{message}\n\nTechnical details: {error_str}"
    
    if context:
        return f"Error in {context}: {error_str}"
    
    return error_str
