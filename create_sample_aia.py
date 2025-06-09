"""
Create a sample AIA file to test MIT App Inventor compatibility
This generates a properly formatted AIA file that should work with MIT App Inventor
"""

from aia_generator import AIAGenerator
import json

def create_sample_app():
    """Create a sample calculator app for testing"""
    
    sample_app_data = {
        "app_name": "Calculator",
        "description": "Simple calculator app with basic arithmetic operations",
        "screens": [
            {
                "name": "Screen1", 
                "title": "Calculator",
                "components": [
                    {
                        "type": "Label",
                        "name": "DisplayLabel",
                        "text": "0",
                        "properties": {
                            "FontSize": "24",
                            "TextAlignment": "2",
                            "Width": "-2",
                            "Height": "60",
                            "BackgroundColor": "&HFF000000",
                            "TextColor": "&HFFFFFFFF"
                        }
                    },
                    {
                        "type": "Button",
                        "name": "Button1",
                        "text": "1",
                        "properties": {
                            "FontSize": "18",
                            "Width": "60",
                            "Height": "60"
                        }
                    },
                    {
                        "type": "Button", 
                        "name": "Button2",
                        "text": "2",
                        "properties": {
                            "FontSize": "18",
                            "Width": "60", 
                            "Height": "60"
                        }
                    },
                    {
                        "type": "Button",
                        "name": "ButtonPlus",
                        "text": "+",
                        "properties": {
                            "FontSize": "18",
                            "Width": "60",
                            "Height": "60",
                            "BackgroundColor": "&HFFFF8000"
                        }
                    },
                    {
                        "type": "Button",
                        "name": "ButtonEquals",
                        "text": "=",
                        "properties": {
                            "FontSize": "18", 
                            "Width": "60",
                            "Height": "60",
                            "BackgroundColor": "&HFF0080FF"
                        }
                    }
                ]
            }
        ],
        "blocks": [
            {
                "event": "Button1.Click",
                "action": "set DisplayLabel.Text to (get DisplayLabel.Text) + '1'"
            },
            {
                "event": "Button2.Click", 
                "action": "set DisplayLabel.Text to (get DisplayLabel.Text) + '2'"
            },
            {
                "event": "ButtonPlus.Click",
                "action": "set DisplayLabel.Text to (get DisplayLabel.Text) + '+'"
            }
        ],
        "assets": [],
        "permissions": []
    }
    
    return sample_app_data

def main():
    print("Creating sample AIA file for MIT App Inventor testing...")
    
    # Create the generator
    generator = AIAGenerator()
    
    # Generate sample app data
    app_data = create_sample_app()
    
    # Create the AIA file
    try:
        output_path = generator.create_aia_file(app_data)
        print(f"Sample AIA file created: {output_path}")
        print("\nTo test:")
        print("1. Go to http://ai2.appinventor.mit.edu/")
        print("2. Click 'Projects' -> 'Import project (.aia) from my computer'")
        print(f"3. Select the file: {output_path}")
        print("4. The project should import without errors")
        
        return output_path
        
    except Exception as e:
        print(f"Error creating sample AIA: {e}")
        return None

if __name__ == "__main__":
    main()