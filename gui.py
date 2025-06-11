"""
GUI Module for MIT App Inventor AIA Generator
Handles the desktop interface using Tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from PIL import Image, ImageTk
import logging

from ai_agent import AIAgent
from aia_generator import AIAGenerator
from config import Config

class AIAGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MIT App Inventor AIA Generator")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Initialize components
        self.ai_agent = None
        self.aia_generator = AIAGenerator()
        self.selected_image_path = None
        self.config = Config()
        
        # Setup GUI
        self.setup_gui()
        self.setup_api_key()
        
    def setup_gui(self):
        """Setup the main GUI components"""
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # API Key section
        self.setup_api_section(main_frame, 0)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        
        # Prompt section
        self.setup_prompt_section(main_frame, 2)
        
        # Image section
        self.setup_image_section(main_frame, 3)
        
        # Generate button
        self.setup_generate_section(main_frame, 4)
        
        # Progress section
        self.setup_progress_section(main_frame, 5)
        
        # Output section
        self.setup_output_section(main_frame, 6)
        
    def setup_api_section(self, parent, row):
        """Setup API key configuration section"""
        # API Key label and entry
        ttk.Label(parent, text="Google AI API Key:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        
        self.api_key_var = tk.StringVar()
        api_entry = ttk.Entry(
            parent, textvariable=self.api_key_var, 
            show="*", width=50
        )
        api_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Test API button
        ttk.Button(
            parent, text="Test API", 
            command=self.test_api_key
        ).grid(row=row, column=2, padx=(10, 0), pady=5)
        
    def setup_prompt_section(self, parent, row):
        """Setup prompt input section"""
        ttk.Label(parent, text="App Description Prompt:").grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5
        )
        
        # Create frame for text area and scrollbar
        text_frame = ttk.Frame(parent)
        text_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        text_frame.columnconfigure(0, weight=1)
        
        self.prompt_text = scrolledtext.ScrolledText(
            text_frame, height=6, wrap=tk.WORD
        )
        self.prompt_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Placeholder text
        placeholder = "Describe the app you want to create for MIT App Inventor...\n\nExample: Create a simple calculator app with buttons for basic arithmetic operations (add, subtract, multiply, divide) and a display screen."
        self.prompt_text.insert("1.0", placeholder)
        self.prompt_text.bind("<FocusIn>", self.clear_placeholder)
        
    def setup_image_section(self, parent, row):
        """Setup image upload section"""
        ttk.Label(parent, text="Design Reference Image:").grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5
        )
        
        image_frame = ttk.Frame(parent)
        image_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Image selection button
        ttk.Button(
            image_frame, text="Select Image (Optional)", 
            command=self.select_image
        ).grid(row=0, column=0, sticky=tk.W)
        
        # Selected image label
        self.image_label = ttk.Label(image_frame, text="No image selected")
        self.image_label.grid(row=0, column=1, padx=(10, 0))
        
        # Image preview
        self.image_preview = ttk.Label(image_frame)
        self.image_preview.grid(row=1, column=0, columnspan=2, pady=5)
        
    def setup_generate_section(self, parent, row):
        """Setup generate button section"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        self.generate_button = ttk.Button(
            button_frame, text="Generate AIA File", 
            command=self.generate_aia
        )
        self.generate_button.pack()
        
    def setup_progress_section(self, parent, row):
        """Setup progress bar section"""
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(parent, textvariable=self.progress_var)
        self.progress_label.grid(row=row, column=0, columnspan=3, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            parent, mode='indeterminate'
        )
        self.progress_bar.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
    def setup_output_section(self, parent, row):
        """Setup output log section"""
        ttk.Label(parent, text="Output Log:").grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5
        )
        
        log_frame = ttk.Frame(parent)
        log_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            log_frame, height=8, state=tk.DISABLED
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame row weight for resizing
        parent.rowconfigure(row, weight=1)
        
    def setup_api_key(self):
        """Load saved API key if available"""
        saved_key = self.config.get_api_key()
        if saved_key:
            self.api_key_var.set(saved_key)
            self.ai_agent = AIAgent(saved_key)
            self.log_message("Previously saved API key loaded successfully")
            
    def clear_placeholder(self, event):
        """Clear placeholder text when user focuses on prompt"""
        current_text = self.prompt_text.get("1.0", tk.END).strip()
        if current_text.startswith("Describe the app you want to create"):
            self.prompt_text.delete("1.0", tk.END)
            
    def test_api_key(self):
        """Test the provided API key"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter an API key")
            return
            
        self.log_message("Testing API key...")
        
        def test_api():
            try:
                self.ai_agent = AIAgent(api_key)
                test_result = self.ai_agent.test_connection()
                
                if test_result:
                    # Save API key only after successful validation
                    self.config.save_api_key(api_key)
                    self.root.after(0, lambda: messagebox.showinfo("Success", "API key is valid and saved!"))
                    self.root.after(0, lambda: self.log_message("API key validated and saved successfully"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Invalid API key or connection failed"))
                    self.root.after(0, lambda: self.log_message("API key validation failed"))
                    
            except Exception as e:
                error_msg = f"API test failed: {str(e)}"
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                self.root.after(0, lambda: self.log_message(error_msg))
                
        threading.Thread(target=test_api, daemon=True).start()
        
    def select_image(self):
        """Select an image file for design reference"""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Design Reference Image",
            filetypes=file_types
        )
        
        if filename:
            self.selected_image_path = filename
            self.image_label.config(text=f"Selected: {os.path.basename(filename)}")
            self.show_image_preview(filename)
            self.log_message(f"Image selected: {os.path.basename(filename)}")
            
    def show_image_preview(self, image_path):
        """Show a preview of the selected image"""
        try:
            # Open and resize image for preview
            image = Image.open(image_path)
            image.thumbnail((200, 200), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for Tkinter
            photo = ImageTk.PhotoImage(image)
            self.image_preview.config(image=photo)
            self.image_preview.image = photo  # Keep a reference
            
        except Exception as e:
            self.log_message(f"Failed to preview image: {str(e)}")
            
    def generate_aia(self):
        """Generate AIA file from prompt and optional image"""
        # Validate inputs
        api_key = self.api_key_var.get().strip()
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        
        if not api_key:
            messagebox.showerror("Error", "Please enter and test your API key first")
            return
            
        if not prompt or prompt.startswith("Describe the app you want to create"):
            messagebox.showerror("Error", "Please enter a description for your app")
            return
            
        # Initialize AI agent if not already done
        if not self.ai_agent:
            self.ai_agent = AIAgent(api_key)
        elif self.ai_agent.api_key != api_key:
            self.ai_agent = AIAgent(api_key)
            
        # Start generation in separate thread
        self.generate_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set("Generating AIA file...")
        
        def generate_thread():
            try:
                self.root.after(0, lambda: self.log_message("Starting AIA generation..."))
                
                # Generate app structure using AI
                app_data = self.ai_agent.generate_app_structure(
                    prompt, self.selected_image_path
                )
                
                if not app_data:
                    raise Exception("Failed to generate app structure from AI")
                    
                self.root.after(0, lambda: self.log_message("App structure generated, creating AIA file..."))
                
                # Create AIA file
                output_path = self.aia_generator.create_aia_file(app_data)
                
                self.root.after(0, lambda: self.generation_complete(output_path))
                
            except Exception as e:
                error_msg = f"Generation failed: {str(e)}"
                logging.error(error_msg)
                if "failed validation" in str(e).lower():
                    error_msg = "⚠️ GENERATED FILE IS NOT A VALID AIA FILE ⚠️\n\nThe generated file cannot be opened in MIT App Inventor because it doesn't match the required format.\n\nThis usually means:\n• The app description was too complex\n• Unsupported features were requested\n• File structure doesn't match MIT App Inventor requirements\n\nTry:\n• Simplifying your app description\n• Using basic components only (Button, Label, TextBox)\n• Avoiding complex layouts or advanced features"
                self.root.after(0, lambda: self.generation_failed(error_msg))
                
        threading.Thread(target=generate_thread, daemon=True).start()
        
    def generation_complete(self, output_path):
        """Handle successful generation completion"""
        self.progress_bar.stop()
        self.progress_var.set("Generation completed!")
        self.generate_button.config(state=tk.NORMAL)
        
        self.log_message(f"AIA file created successfully: {output_path}")
        
        # Ask user if they want to open the output folder
        result = messagebox.askyesno(
            "Success", 
            f"AIA file generated successfully!\n\nFile saved to: {output_path}\n\nWould you like to open the output folder?"
        )
        
        if result:
            try:
                os.startfile(os.path.dirname(output_path))
            except Exception as e:
                self.log_message(f"Failed to open folder: {str(e)}")
                
    def generation_failed(self, error_msg):
        """Handle generation failure"""
        self.progress_bar.stop()
        self.progress_var.set("Generation failed")
        self.generate_button.config(state=tk.NORMAL)
        
        self.log_message(error_msg)
        messagebox.showerror("Generation Failed", error_msg)
        
    def log_message(self, message):
        """Add message to output log"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        logging.info(message)
