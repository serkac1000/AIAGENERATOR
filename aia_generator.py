
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
import uuid
import random

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

                # Create ZIP file (AIA format) - use .aia extension
                app_name = app_data.get('app_name', 'GeneratedApp')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                random_id = random.randint(100000000000, 999999999999)
                aia_filename = f"{app_name}_{timestamp}_{random_id}.aia"
                aia_path = os.path.join(self.output_dir, aia_filename)

                self._create_zip_file(temp_dir, aia_path)

                # Validate the generated AIA file
                if not self._validate_aia_file(aia_path):
                    raise Exception("⚠️ GENERATED FILE IS NOT A VALID AIA FILE ⚠️\n\nThe generated file cannot be opened in MIT App Inventor because it doesn't match the required format. This usually means the app structure is too complex or uses unsupported features.")

                logging.info(f"AIA file created: {aia_path}")
                return aia_path

        except Exception as e:
            logging.error(f"Failed to create AIA file: {str(e)}")
            raise

    def _validate_aia_file(self, aia_path):
        """Validate that the AIA file has correct structure"""
        try:
            with zipfile.ZipFile(aia_path, 'r') as zip_file:
                file_list = zip_file.namelist()

                # Check for required files in correct locations
                required_files = ['youngandroidproject/project.properties']
                for req_file in required_files:
                    if req_file not in file_list:
                        logging.error(f"Missing required file: {req_file}")
                        return False

                # Check for src directory structure
                has_src = any(f.startswith('src/appinventor/') for f in file_list)
                if not has_src:
                    logging.error("Missing src/appinventor/ directory structure")
                    return False

                # Check for .scm files (required)
                has_scm = any(f.endswith('.scm') for f in file_list)
                if not has_scm:
                    logging.error("Missing .scm files")
                    return False

                # Check for .bky files (required)
                has_bky = any(f.endswith('.bky') for f in file_list)
                if not has_bky:
                    logging.error("Missing .bky files")
                    return False

                return True

        except Exception as e:
            logging.error(f"AIA validation error: {e}")
            return False

    def _create_project_structure(self, temp_dir, app_data):
        """Create the internal structure of the AIA file matching MIT App Inventor exactly"""

        # Create main directories following exact MIT App Inventor structure
        assets_dir = os.path.join(temp_dir, "assets")
        youngandroid_dir = os.path.join(temp_dir, "youngandroidproject")
        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(youngandroid_dir, exist_ok=True)

        # Generate a realistic user identifier
        user_id = f"ai_serkac{random.randint(100, 999)}"
        app_name = app_data.get('app_name', 'GeneratedApp').replace(' ', '').replace('-', '')
        
        # Create proper package structure under src/appinventor/ai_user/AppName/
        src_dir = os.path.join(temp_dir, "src")
        appinventor_dir = os.path.join(src_dir, "appinventor")
        user_dir = os.path.join(appinventor_dir, user_id)
        app_dir = os.path.join(user_dir, app_name)
        os.makedirs(app_dir, exist_ok=True)

        # Create project.properties file in youngandroidproject directory
        self._create_project_properties(youngandroid_dir, app_data, user_id, app_name)

        # Create screen files in the app directory
        screens = app_data.get('screens', [{'name': 'Screen1', 'title': 'Screen1'}])
        for screen in screens:
            self._create_screen_files(app_dir, screen, app_data, user_id, app_name)

    def _create_project_properties(self, youngandroid_dir, app_data, user_id, app_name):
        """Create project.properties file exactly matching MIT App Inventor format"""
        screens = app_data.get('screens', [{'name': 'Screen1'}])
        main_screen = screens[0].get('name', 'Screen1')

        # Use current timestamp for realistic project properties
        timestamp = datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y")

        # Match the exact format from the working reference
        properties_content = f"""#
#{timestamp}
sizing=Responsive
color.primary.dark=&HFF303F9F
color.primary=&HFF3F51B5
color.accent=&HFFFF4081
aname={app_name}
defaultfilescope=App
main=appinventor.{user_id}.{app_name}.{main_screen}
source=../src
actionbar=True
useslocation=False
assets=../assets
build=../build
name={app_name}
showlistsasjson=True
theme=AppTheme.Light.DarkActionBar
versioncode=1
versionname=1.0
"""

        properties_path = os.path.join(youngandroid_dir, "project.properties")
        with open(properties_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(properties_content)

    def _create_screen_files(self, app_dir, screen_data, app_data, user_id, app_name):
        """Create .scm and .bky files for a screen exactly matching MIT format"""
        screen_name = screen_data.get('name', 'Screen1')

        # Create .scm file (screen component structure)
        scm_content = self._generate_scm_content(screen_data, app_data)
        scm_path = os.path.join(app_dir, f"{screen_name}.scm")
        with open(scm_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(scm_content)

        # Create .bky file (blocks definition) - proper XML structure instead of empty file
        bky_content = self._generate_bky_content(screen_data, app_data)
        bky_path = os.path.join(app_dir, f"{screen_name}.bky")
        with open(bky_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(bky_content)

    def _generate_scm_content(self, screen_data, app_data):
        """Generate .scm file content exactly matching working reference format"""
        screen_name = screen_data.get('name', 'Screen1')
        screen_title = screen_data.get('title', screen_name)
        app_name = app_data.get('app_name', 'GeneratedApp').replace(' ', '').replace('-', '')

        # Create components list exactly as in reference
        components = screen_data.get('components', [])
        component_list = []

        # Generate UUIDs exactly like MIT App Inventor - negative integers
        used_uuids = set()
        
        # Generate components with proper structure and unique UUIDs
        for i, component in enumerate(components):
            # Generate unique negative UUID like in reference
            uuid_val = self._generate_unique_uuid(used_uuids)
            used_uuids.add(uuid_val)
            comp_data = self._component_to_dict(component, i+1, uuid_val)
            component_list.append(comp_data)

        # Create the properties structure exactly matching reference
        properties = {
            "$Name": screen_name,
            "$Type": "Form",
            "$Version": "31",
            "ActionBar": True,
            "AppName": app_name,
            "Title": screen_title,
            "Uuid": "0"  # Always "0" for main screen in MIT App Inventor
        }

        if component_list:
            properties["$Components"] = component_list

        # Create the full SCM structure exactly as reference
        scm_structure = {
            "authURL": ["ai2.appinventor.mit.edu"],
            "YaVersion": "232",
            "Source": "Form",
            "Properties": properties
        }

        # Format exactly as MIT App Inventor expects - compact JSON like reference
        json_str = json.dumps(scm_structure, separators=(',', ':'))
        scm_content = f'#|\n$JSON\n{json_str}\n|#'
        return scm_content

    def _generate_bky_content(self, screen_data, app_data):
        """Generate proper .bky file content with minimal valid XML structure"""
        # Create minimal but valid XML structure as per MIT App Inventor requirements
        bky_content = """<xml xmlns="http://www.w3.org/1999/xhtml">
  <yacodeblocks ya-version="232" language-version="31">
  </yacodeblocks>
</xml>"""
        
        # Check if we have button components and add simple click events
        components = screen_data.get('components', [])
        buttons = [comp for comp in components if comp.get('type') == 'Button']
        labels = [comp for comp in components if comp.get('type') == 'Label']
        
        if buttons and labels:
            # Generate simple click events for buttons that update the first label
            events_xml = []
            y_position = 50
            target_label = labels[0].get('name', 'LabelResult')
            
            for i, button in enumerate(buttons):
                button_name = button.get('name', f'Button{i+1}')
                # Create proper MIT App Inventor block structure
                event_xml = f"""    <block type="component_event" id="event_{button_name}" x="50" y="{y_position}">
      <mutation component_type="Button" event_name="Click"></mutation>
      <field name="component_object">{button_name}</field>
      <statement name="DO">
        <block type="component_set_get" id="set_{button_name}">
          <mutation component_type="Label" set_or_get="set" property_name="Text" is_generic="false" instance_name="{target_label}"></mutation>
          <field name="COMPONENT_SELECTOR">{target_label}</field>
          <field name="PROP">Text</field>
          <value name="VALUE">
            <block type="text" id="text_{button_name}">
              <field name="TEXT">{button_name} was clicked!</field>
            </block>
          </value>
        </block>
      </statement>
    </block>"""
                events_xml.append(event_xml)
                y_position += 150
            
            # Create proper XML structure with events
            if events_xml:
                bky_content = f"""<xml xmlns="http://www.w3.org/1999/xhtml">
  <yacodeblocks ya-version="232" language-version="31">
{chr(10).join(events_xml)}
  </yacodeblocks>
</xml>"""
        
        return bky_content

    def _generate_unique_uuid(self, used_uuids):
        """Generate unique negative UUID like MIT App Inventor uses"""
        while True:
            # Generate negative integer UUID like in reference (-291987386, -406306722, etc.)
            uuid_val = str(-random.randint(100000000, 999999999))
            if uuid_val not in used_uuids:
                return uuid_val

    def _component_to_dict(self, component, index, uuid_val):
        """Convert component data to dictionary matching reference format exactly"""
        comp_type = component.get('type', 'Button')
        comp_name = component.get('name', f'{comp_type}{index}')

        # Use exact version numbers from working reference
        version_map = {
            'Button': '7',
            'Label': '6',
            'TextBox': '6',
            'Image': '5',
            'HorizontalArrangement': '5',
            'VerticalArrangement': '5'
        }

        comp_data = {
            "$Name": comp_name,
            "$Type": comp_type,
            "$Version": version_map.get(comp_type, "1"),
            "Uuid": uuid_val
        }

        # Add text property exactly as in reference
        if comp_type in ['Button', 'Label']:
            comp_data['Text'] = f"Text for {comp_name}"

        # Add proper sizing and layout properties for buttons
        if comp_type == 'Button':
            comp_data['Width'] = 'Fill parent'
            comp_data['Height'] = 'Automatic'
            # Add default colors if not specified
            if 'BackgroundColor' not in component.get('properties', {}):
                comp_data['BackgroundColor'] = '&HFF4CAF50'  # Green
            if 'TextColor' not in component.get('properties', {}):
                comp_data['TextColor'] = '&HFFFFFFFF'  # White

        # Add proper sizing for labels
        if comp_type == 'Label':
            comp_data['Width'] = 'Fill parent'
            comp_data['Height'] = 'Automatic'
            comp_data['TextAlignment'] = '1'  # Center alignment
            comp_data['FontSize'] = '20'

        # Add component properties with proper MIT App Inventor formatting
        properties = component.get('properties', {})
        for prop_name, prop_value in properties.items():
            if 'Color' in prop_name and isinstance(prop_value, str) and prop_value.startswith('#'):
                # Convert hex to MIT App Inventor color format exactly
                hex_val = prop_value[1:]
                if len(hex_val) == 6:
                    comp_data[prop_name] = f"&HFF{hex_val.upper()}"
            else:
                comp_data[prop_name] = str(prop_value)

        return comp_data

    def _create_zip_file(self, source_dir, output_path):
        """Create ZIP file with proper compression settings for MIT App Inventor"""
        try:
            # Use no compression like MIT App Inventor exports
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_STORED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, source_dir)
                        # Use forward slashes for ZIP archive paths
                        arc_name = arc_name.replace(os.sep, '/')
                        zipf.write(file_path, arc_name)

            logging.info(f"AIA file created successfully: {output_path}")

        except Exception as e:
            logging.error(f"Failed to create AIA file: {str(e)}")
            raise
