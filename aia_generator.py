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

                # Check for required files
                required_files = ['project.properties']
                for req_file in required_files:
                    if req_file not in file_list:
                        logging.error(f"Missing required file: {req_file}")
                        return False

                # Check for src directory structure
                has_src = any(f.startswith('src/') for f in file_list)
                if not has_src:
                    logging.error("Missing src/ directory structure")
                    return False

                # Check for .scm and .bky files
                has_scm = any(f.endswith('.scm') for f in file_list)
                has_bky = any(f.endswith('.bky') for f in file_list)

                if not has_scm or not has_bky:
                    logging.error("Missing .scm or .bky files")
                    return False

                return True

        except Exception as e:
            logging.error(f"AIA validation error: {e}")
            return False

    def _create_project_structure(self, temp_dir, app_data):
        """Create the internal structure of the AIA file"""

        # Create main directories matching MIT App Inventor structure
        src_dir = os.path.join(temp_dir, "src")
        assets_dir = os.path.join(temp_dir, "assets")
        build_dir = os.path.join(temp_dir, "build")
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(build_dir, exist_ok=True)

        # Create project.properties file (root level)
        self._create_project_properties(temp_dir, app_data)

        # Create youngandroidproject directory structure
        app_name = app_data.get('app_name', 'GeneratedApp').replace(' ', '').replace('-', '')
        package_name = f"appinventor.ai_user.{app_name}"

        # Create the full package directory structure
        package_parts = package_name.split('.')
        current_path = src_dir
        for part in package_parts:
            current_path = os.path.join(current_path, part)
            os.makedirs(current_path, exist_ok=True)

        # Create screen files
        screens = app_data.get('screens', [{'name': 'Screen1', 'title': 'Screen1'}])
        for screen in screens:
            self._create_screen_files(current_path, screen, app_data)

    def _create_project_properties(self, temp_dir, app_data):
        """Create project.properties file matching MIT App Inventor format"""
        app_name = app_data.get('app_name', 'GeneratedApp').replace(' ', '').replace('-', '')
        screens = app_data.get('screens', [{'name': 'Screen1'}])
        main_screen = screens[0].get('name', 'Screen1')

        # Use current timestamp for realistic project properties
        timestamp = datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y")

        properties_content = f"""#
#{timestamp}
sizing=Responsive
color.primary.dark=&HFF303F9F
color.primary=&HFF3F51B5
color.accent=&HFFFF4081
aname={app_name}
defaultfilescope=App
main=appinventor.ai_user.{app_name}.{main_screen}
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

        properties_path = os.path.join(temp_dir, "project.properties")
        with open(properties_path, 'w', encoding='utf-8') as f:
            f.write(properties_content)

    def _create_screen_files(self, package_dir, screen_data, app_data):
        """Create .scm and .bky files for a screen"""
        screen_name = screen_data.get('name', 'Screen1')

        # Create .scm file (screen component structure)
        scm_content = self._generate_scm_content(screen_data, app_data)
        scm_path = os.path.join(package_dir, f"{screen_name}.scm")
        with open(scm_path, 'w', encoding='utf-8') as f:
            f.write(scm_content)

        # Create .bky file (blocks definition) - empty for now
        bky_content = self._generate_bky_content(screen_data, app_data)
        bky_path = os.path.join(package_dir, f"{screen_name}.bky")
        with open(bky_path, 'w', encoding='utf-8') as f:
            f.write(bky_content)

    def _generate_scm_content(self, screen_data, app_data):
        """Generate .scm file content matching MIT App Inventor format"""
        screen_name = screen_data.get('name', 'Screen1')
        screen_title = screen_data.get('title', screen_name)
        app_name = app_data.get('app_name', 'GeneratedApp').replace(' ', '').replace('-', '')

        # Create components list
        components = screen_data.get('components', [])
        component_list = []

        for i, component in enumerate(components):
            comp_data = self._component_to_dict(component, i+1)
            component_list.append(comp_data)

        # Create the properties structure
        properties = {
            "$Name": screen_name,
            "$Type": "Form",
            "$Version": "31",
            "ActionBar": "True",
            "AppName": app_name,
            "Title": screen_title,
            "Uuid": "0"
        }

        if component_list:
            properties["$Components"] = component_list

        # Create the full SCM structure exactly as MIT App Inventor expects
        scm_structure = {
            "authURL": ["ai2.appinventor.mit.edu"],
            "YaVersion": "232",
            "Source": "Form",
            "Properties": properties
        }

        # Format exactly as MIT App Inventor expects
        scm_content = f'#|\n$JSON\n{json.dumps(scm_structure, separators=(",", ":"))}\n|#'
        return scm_content

    def _component_to_dict(self, component, index):
        """Convert component data to dictionary for .scm file"""
        comp_type = component.get('type', 'Button')
        comp_name = component.get('name', f'{comp_type}{index}')

        # Set correct version numbers for different component types
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
            "Uuid": str(-(900000000 + index * 1000 + hash(comp_name) % 1000))
        }

        # Add text property if specified
        if 'text' in component and component['text']:
            comp_data['Text'] = f"Text for {comp_name}"

        # Add component properties with proper formatting
        properties = component.get('properties', {})
        for prop_name, prop_value in properties.items():
            if 'Color' in prop_name and isinstance(prop_value, str) and prop_value.startswith('#'):
                # Convert hex to MIT App Inventor color format
                hex_val = prop_value[1:]
                if len(hex_val) == 6:
                    comp_data[prop_name] = f"&HFF{hex_val.upper()}"
            else:
                comp_data[prop_name] = prop_value

        return comp_data

    def _generate_bky_content(self, screen_data, app_data):
        """Generate .bky file content (empty blocks file)"""
        # Generate completely empty blocks file as MIT App Inventor expects
        return ""

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