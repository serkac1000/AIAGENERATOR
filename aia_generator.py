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
        
        main_screen = app_data.get('screens', [{}])[0].get('name', 'Screen1')
        ya_props_content = f"""main={main_screen}
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
assets=../assets
source=../src
build=../build
versioncode=1
versionname=1.0
useslocation=False
aname={app_name}
sizing=Responsive
showlistsasjson=True
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
        
        # Create proper MIT App Inventor SCM structure with minimal required properties
        properties = {
            "$Name": screen_name,
            "$Type": "Form",
            "$Version": "31",
            "AppName": app_name,
            "Title": screen_title,
            "Uuid": self._generate_uuid()
        }
        
        # Add components if any exist
        components = screen_data.get('components', [])
        if components:
            component_list = []
            for component in components:
                component_list.append(self._component_to_dict(component))
            properties["$Components"] = component_list
        
        # Create the full SCM structure exactly as MIT App Inventor expects
        scm_structure = {
            "authURL": ["ai2.appinventor.mit.edu"],
            "YaVersion": "208", 
            "Source": "Form",
            "Properties": properties
        }
        
        # Format exactly as MIT App Inventor expects - no extra formatting
        scm_content = f'#|\n$JSON\n{json.dumps(scm_structure, separators=(",", ":"))}\n|#'
        return scm_content
        
    def _component_to_dict(self, component):
        """Convert component data to dictionary"""
        comp_type = component.get('type', 'Button')
        
        # Set correct version numbers for different component types
        version_map = {
            'Button': '8',
            'Label': '6', 
            'TextBox': '6',
            'Image': '5',
            'HorizontalArrangement': '5',
            'VerticalArrangement': '5'
        }
        
        comp_data = {
            "$Name": component.get('name', 'Component1'),
            "$Type": comp_type,
            "$Version": version_map.get(comp_type, "1"),
            "Uuid": self._generate_uuid()
        }
        
        # Add minimal default properties
        if comp_type == 'Button':
            comp_data.update({
                "Width": "-2",
                "Height": "-2"
            })
        elif comp_type == 'Label':
            comp_data.update({
                "Width": "-2", 
                "Height": "-2"
            })
        
        # Add text property if specified
        if 'text' in component:
            comp_data['Text'] = component['text']
            
        # Add component properties with proper formatting
        properties = component.get('properties', {})
        for prop_name, prop_value in properties.items():
            # Handle color properties properly
            if 'Color' in prop_name and isinstance(prop_value, str) and prop_value.startswith('#'):
                # Convert hex to MIT App Inventor color format
                hex_val = prop_value[1:]
                comp_data[prop_name] = f"&HFF{hex_val.upper()}"
            else:
                comp_data[prop_name] = prop_value
            
        return comp_data
        
    def _generate_bky_content(self, screen_data, app_data):
        """Generate .bky file content (Blockly XML format)"""
        screen_name = screen_data.get('name', 'Screen1')
        
        # Start with proper XML declaration
        bky_content = '<xml xmlns="https://developers.google.com/blockly/xml">\n'
        
        # Add blocks based on app_data blocks
        blocks = app_data.get('blocks', [])
        y_pos = 20
        
        for block in blocks:
            bky_content += self._generate_block_xml(block, y_pos)
            y_pos += 120
            
        # If no blocks specified, add a basic initialization block
        if not blocks:
            bky_content += f'  <block type="component_event" id="{self._generate_uuid()}" x="20" y="20">\n'
            bky_content += f'    <mutation component_type="Form" event_name="Initialize"></mutation>\n'
            bky_content += f'    <field name="component_object">{screen_name}</field>\n'
            bky_content += f'  </block>\n'
        
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
            
        # Determine component type based on component name
        comp_type = "Form"
        if "Button" in component:
            comp_type = "Button"
        elif "Label" in component:
            comp_type = "Label"
        elif "TextBox" in component:
            comp_type = "TextBox"
            
        block_id = self._generate_uuid()
        action_id = self._generate_uuid()
        
        block_xml = f'  <block type="component_event" id="{block_id}" x="20" y="{y_offset}">\n'
        block_xml += f'    <mutation component_type="{comp_type}" event_name="{event_name}"></mutation>\n'
        block_xml += f'    <field name="component_object">{component}</field>\n'
        
        # Add simple action if specified
        if action and action != 'do nothing':
            block_xml += f'    <statement name="DO">\n'
            block_xml += f'      <block type="lexical_variable_set" id="{action_id}">\n'
            block_xml += f'        <field name="VAR">global temp</field>\n'
            block_xml += f'        <value name="VALUE">\n'
            block_xml += f'          <block type="text" id="{self._generate_uuid()}">\n'
            block_xml += f'            <field name="TEXT">{action}</field>\n'
            block_xml += f'          </block>\n'
            block_xml += f'        </value>\n'
            block_xml += f'      </block>\n'
            block_xml += f'    </statement>\n'
            
        block_xml += f'  </block>\n'
        return block_xml
        
    def _generate_uuid(self):
        """Generate a UUID-like string matching MIT App Inventor format"""
        import uuid
        # MIT App Inventor uses standard UUID4 format with dashes removed
        return str(uuid.uuid4()).replace('-', '')
        
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
