# MIT App Inventor AIA Generator

A desktop AI agent application that generates MIT App Inventor AIA files from text prompts and optional images using Google AI API.

## Features

- **AI-Powered Generation**: Uses Google AI (Gemini) to create app structures from natural language descriptions
- **Image Analysis**: Optional image upload for UI design reference and analysis
- **AIA File Export**: Generates compatible MIT App Inventor AIA files ready for import
- **Desktop Interface**: User-friendly Windows desktop application
- **No Server Required**: Standalone application that works offline (except for AI API calls)

## System Requirements

- Windows 10 or later
- Internet connection (for Google AI API calls)
- Google AI API key (free tier available)

## Installation

### Option 1: Use Pre-built Executable (Recommended)

1. Download and extract the `AIA_Generator_Release.zip` file
2. Run `AIA_Generator.exe`
3. Enter your Google AI API key when prompted

### Option 2: Run from Source Code

1. **Install Python 3.8 or later**
   - Download from [python.org](https://www.python.org/downloads/)
   - **Important**: Check "Add Python to PATH" during installation

2. **Extract the source code**
   - Extract all files to a folder of your choice

3. **Run setup**
   - Double-click `setup.bat` to install required packages
   - Or manually run: `pip install google-generativeai pillow pyinstaller`

4. **Run the application**
   - Double-click `main.py` or run `python main.py` in command prompt

## Getting Google AI API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it into the application when prompted

**Note**: The free tier includes generous usage limits suitable for most users.

## Usage

1. **Enter API Key**
   - Paste your Google AI API key in the designated field
   - Click "Test API" to verify it works

2. **Describe Your App**
   - Enter a detailed description of the app you want to create
   - Be specific about functionality, UI elements, and behavior
   - Example: "Create a simple calculator app with buttons for basic arithmetic operations and a display screen"

3. **Add Design Reference (Optional)**
   - Click "Select Image" to upload a design mockup or reference
   - The AI will analyze the image and incorporate design elements

4. **Generate AIA File**
   - Click "Generate AIA File"
   - Wait for the AI to process your request
   - The generated AIA file will be saved in the `output` folder

5. **Import to MIT App Inventor**
   - Go to [MIT App Inventor](http://ai2.appinventor.mit.edu/)
   - Click "Projects" → "Import project (.aia) from my computer"
   - Select your generated AIA file

## Example Prompts

### Simple Apps
- "Create a basic note-taking app with a text input and save button"
- "Make a tip calculator that calculates tip percentage and total amount"
- "Build a simple quiz app with multiple choice questions"

### Interactive Apps
- "Create a drawing app where users can draw with different colors"
- "Make a random quote generator with a button to get new quotes"
- "Build a simple game where users tap buttons to score points"

### Utility Apps
- "Create a unit converter for length, weight, and temperature"
- "Make a simple expense tracker with categories and totals"
- "Build a countdown timer with start, stop, and reset buttons"

## Troubleshooting

### Application Won't Start
- Ensure Python 3.8+ is installed and added to PATH
- Run `setup.bat` to install required packages
- Check `app.log` file for error details

### API Key Issues
- Verify your API key is correct
- Check your internet connection
- Ensure you haven't exceeded API quota limits
- Try generating a new API key

### Generated AIA Won't Import
- Ensure the generated file has `.aia` extension
- Try generating again with a simpler prompt
- Check that MIT App Inventor is working properly

### Poor Generation Quality
- Provide more detailed and specific prompts
- Include specific component names and behaviors
- Add reference images for better UI design
- Try breaking complex apps into simpler descriptions

## File Structure

```
AIA_Generator_Windows/
├── main.py              # Main application entry point
├── gui.py               # Desktop GUI interface
├── ai_agent.py          # Google AI integration
├── aia_generator.py     # AIA file creation
├── config.py            # Configuration management
├── utils.py             # Utility functions
├── setup.bat            # Windows setup script
├── build.bat            # Build executable script
├── run.bat              # Quick run script
├── requirements.txt     # Python dependencies
├── README.md            # This documentation
├── INSTALL.md           # Installation guide
└── output/              # Generated AIA files folder
```

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the app.log file for error details
3. Ensure all installation steps were completed correctly

## Version

Current version: 1.0.0 - Initial release with core functionality for MIT App Inventor AIA file generation using Google AI.

