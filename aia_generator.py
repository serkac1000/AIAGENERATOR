"""
AIA Generator module for creating MIT App Inventor compatible AIA files
AIA files are ZIP archives containing project structure and metadata
"""

import json
import zipfile
import os
import tempfile
import shutil
from datetime import datetime
import logging

class AIAGenerator:
    def __init__(self):
        self.output_dir = "output"
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def create_aia_file(self, app_data):
        """Create AIA file from app data structure"""
        try:
            # Create temporary directory for AIA contents
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create project structure
                self._create_project_structure(temp_dir, app_data)
                
                # Create ZIP file (AIA format)
                app_name = app_data.get('app_name', 'GeneratedApp')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                aia_filename = f"{app_name}_{timestamp}.aia"
                aia_path = os.path.join(self.output_dir, aia_filename)
                
                self._create_zip_file(temp_dir, aia_path)
                
                logging.info(f"AIA file created: {aia_path}")
                return aia_path
                
        except Exception as e:
            logging.error(f"Failed to create AIA file: {str(e)}")
            raise
            
    def _create_project_structure(self, temp_dir, app_data):
        """Create the internal structure of the AIA file"""
        
        # Create main directories matching MIT App Inventor structure
        src_dir = os.path.join(temp_dir, "src")
        assets_dir = os.path.join(temp_dir, "assets")
        build_dir = os.path.join(temp_dir, "build")
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(build_dir, exist_ok=True)
        
        # Create project.properties file
        self._create_project_properties(temp_dir, app_data)
        
        # Create youngandroidproject directory structure with proper package name
        app_name = app_data.get('app_name', 'GeneratedApp')
        package_name = f"appinventor.ai_user.{app_name}"
        ya_dir = os.path.join(src_dir, "appinventor", "ai_user", app_name)
        os.makedirs(ya_dir, exist_ok=True)
        
        # Create screen files for each screen
        for screen in app_data.get('screens', []):
            self._create_screen_files(ya_dir, screen, app_data)
            
        # Create youngandroidproject.properties
        ya_props_dir = os.path.join(src_dir, "appinventor", "ai_user", app_name)
        ya_props_path = os.path.join(ya_props_dir, "youngandroidproject.properties")
        
        ya_props_content = f"""main={app_data.get('screens', [{}])[0].get('name', 'Screen1')}
name={app_name}
authURL=ai2.appinventor.mit.edu
YaVersion=208
Source=Form
"""
        
        with open(ya_props_path, 'w', encoding='utf-8') as f:
            f.write(ya_props_content)
            
    def _create_project_properties(self, temp_dir, app_data):
        """Create project.properties file"""
        app_name = app_data.get('app_name', 'GeneratedApp')
        main_screen = app_data.get('screens', [{}])[0].get('name', 'Screen1')
        
        properties_content = f"""main=appinventor.ai_user.{app_name}.{main_screen}
name={app_name}
assets=..{os.sep}..{os.sep}assets
source=..{os.sep}..{os.sep}src
build=..{os.sep}..{os.sep}build
"""
        
        properties_path = os.path.join(temp_dir, "project.properties")
        with open(properties_path, 'w', encoding='utf-8') as f:
            f.write(properties_content)
            
    def _create_screen_files(self, ya_dir, screen_data, app_data):
        """Create .scm and .bky files for a screen"""
        screen_name = screen_data.get('name', 'Screen1')
        
        # Create .scm file (screen component structure)
        scm_content = self._generate_scm_content(screen_data, app_data)
        scm_path = os.path.join(ya_dir, f"{screen_name}.scm")
        with open(scm_path, 'w', encoding='utf-8') as f:
            f.write(scm_content)
            
        # Create .bky file (blocks definition)
        bky_content = self._generate_bky_content(screen_data, app_data)
        bky_path = os.path.join(ya_dir, f"{screen_name}.bky")
        with open(bky_path, 'w', encoding='utf-8') as f:
            f.write(bky_content)
            
    def _generate_scm_content(self, screen_data, app_data):
        """Generate .scm file content (Scheme-like format for components)"""
        screen_name = screen_data.get('name', 'Screen1')
        screen_title = screen_data.get('title', screen_name)
        app_name = app_data.get('app_name', 'GeneratedApp')
        
        # Start with screen definition in proper MIT App Inventor format
        scm_lines = [
            f"#|",
            f"$JSON",
            f'{{',
            f'  "authURL": ["ai2.appinventor.mit.edu"],',
            f'  "YaVersion": "208",',
            f'  "Source": "Form",',
            f'  "Properties": {{',
            f'    "$Name": "{screen_name}",',
            f'    "$Type": "Form",',
            f'    "$Version": "27",',
            f'    "AppName": "{app_name}",',
            f'    "Title": "{screen_title}",',
            f'    "Uuid": "{self._generate_uuid()}",',
            f'    "$Components": [',
        ]
        
        # Add components
        components = screen_data.get('components', [])
        
        for i, component in enumerate(components):
            component_json = self._component_to_json(component)
            if i < len(components) - 1:
                scm_lines.append(f'      {component_json},')
            else:
                scm_lines.append(f'      {component_json}')
                
        scm_lines.extend([
            '    ]',
            '  }',
            '}',
            '|#'
        ])
        
        return '\n'.join(scm_lines)
        
    def _component_to_json(self, component):
        """Convert component data to JSON string"""
        comp_data = {
            "$Name": component.get('name', 'Component1'),
            "$Type": component.get('type', 'Button'),
            "$Version": "6",
            "Uuid": self._generate_uuid()
        }
        
        # Add component properties
        properties = component.get('properties', {})
        for prop_name, prop_value in properties.items():
            comp_data[prop_name] = prop_value
            
        # Add text property if specified
        if 'text' in component:
            comp_data['Text'] = component['text']
            
        return json.dumps(comp_data, separators=(',', ': '))
        
    def _generate_bky_content(self, screen_data, app_data):
        """Generate .bky file content (Blockly XML format)"""
        screen_name = screen_data.get('name', 'Screen1')
        
        # Basic XML structure for blocks
        bky_content = f'''<xml xmlns="https://developers.google.com/blockly/xml">
'''
        
        # Add blocks based on app_data blocks
        blocks = app_data.get('blocks', [])
        for i, block in enumerate(blocks):
            bky_content += self._generate_block_xml(block, i * 100)
            
        # If no blocks specified, add a basic initialization block
        if not blocks:
            bky_content += f'''  <block type="component_event" id="basic_block" x="20" y="20">
    <mutation component_type="Form" event_name="Initialize"></mutation>
    <field name="component_object">{screen_name}</field>
    <statement name="DO">
      <block type="text_print" id="print_block">
        <value name="TEXT">
          <block type="text" id="text_block">
            <field name="TEXT">App initialized!</field>
          </block>
        </value>
      </block>
    </statement>
  </block>
'''
        
        bky_content += '</xml>'
        return bky_content
        
    def _generate_block_xml(self, block_data, y_offset):
        """Generate XML for a single block"""
        event = block_data.get('event', 'Screen1.Initialize')
        action = block_data.get('action', 'do nothing')
        
        # Parse event (e.g., "Button1.Click")
        if '.' in event:
            component, event_name = event.split('.', 1)
        else:
            component = 'Screen1'
            event_name = 'Initialize'
            
        block_xml = f'''  <block type="component_event" id="event_{hash(event) % 10000}" x="20" y="{20 + y_offset}">
    <mutation component_type="Button" event_name="{event_name}"></mutation>
    <field name="component_object">{component}</field>
    <statement name="DO">
      <block type="text_print" id="action_{hash(action) % 10000}">
        <value name="TEXT">
          <block type="text" id="text_{hash(action) % 10000}">
            <field name="TEXT">{action}</field>
          </block>
        </value>
      </block>
    </statement>
  </block>
'''
        return block_xml
        
    def _generate_uuid(self):
        """Generate a simple UUID-like string"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
    def _create_zip_file(self, source_dir, output_path):
        """Create ZIP file from directory contents"""
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arc_name)
                        
            logging.info(f"ZIP file created successfully: {output_path}")
            
        except Exception as e:
            logging.error(f"Failed to create ZIP file: {str(e)}")
            raise
