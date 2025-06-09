"""
Configuration module for storing and retrieving application settings
"""

import os
import json
import logging
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".aia_generator")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.ensure_config_dir()
        
    def ensure_config_dir(self):
        """Ensure configuration directory exists"""
        try:
            Path(self.config_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.warning(f"Failed to create config directory: {str(e)}")
            
    def save_api_key(self, api_key):
        """Save API key to configuration file"""
        try:
            config_data = self.load_config()
            config_data['google_api_key'] = api_key
            self.save_config(config_data)
            logging.info("API key saved to configuration")
        except Exception as e:
            logging.error(f"Failed to save API key: {str(e)}")
            
    def get_api_key(self):
        """Get saved API key from configuration"""
        try:
            config_data = self.load_config()
            return config_data.get('google_api_key', '')
        except Exception as e:
            logging.error(f"Failed to load API key: {str(e)}")
            return ''
            
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Failed to load config: {str(e)}")
            return {}
            
    def save_config(self, config_data):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save config: {str(e)}")
            
    def get_output_directory(self):
        """Get output directory for generated files"""
        config_data = self.load_config()
        return config_data.get('output_directory', 'output')
        
    def set_output_directory(self, directory):
        """Set output directory for generated files"""
        config_data = self.load_config()
        config_data['output_directory'] = directory
        self.save_config(config_data)
