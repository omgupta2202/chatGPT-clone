import os
import shutil

BASE_DIR = r"c:\Users\omgup\Desktop\chatGPT-clone"
IGNORED_DIRS = {'.git', 'venv', '__pycache__', 'env'}

# Text replacements to perform
REPLACEMENTS = [
    ('lumina_app', 'lumina_app'),
    ('lumina_ai', 'lumina_ai')
]

def process_files():
    for root, dirs, files in os.walk(BASE_DIR):
        # Prevent going into ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            # Only process python, html, txt, and md files
            if file.endswith(('.py', '.html', '.txt', '.md', '.json', '.txt')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    for old, new in REPLACEMENTS:
                        new_content = new_content.replace(old, new)
                        
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated content in {filepath}")
                except Exception as e:
                    print(f"Failed to process {filepath}: {e}")

def rename_directories():
    # 1. Rename templates folder inside the app
    old_templates = os.path.join(BASE_DIR, 'lumina_app', 'templates', 'lumina_app')
    new_templates = os.path.join(BASE_DIR, 'lumina_app', 'templates', 'lumina_app')
    if os.path.exists(old_templates):
        os.rename(old_templates, new_templates)
        print(f"Renamed {old_templates} to {new_templates}")

    # 2. Rename the app folder
    old_app = os.path.join(BASE_DIR, 'lumina_app')
    new_app = os.path.join(BASE_DIR, 'lumina_app')
    if os.path.exists(old_app):
        os.rename(old_app, new_app)
        print(f"Renamed {old_app} to {new_app}")
        
    # 3. Rename the project folder
    old_proj = os.path.join(BASE_DIR, 'lumina_ai')
    new_proj = os.path.join(BASE_DIR, 'lumina_ai')
    if os.path.exists(old_proj):
        os.rename(old_proj, new_proj)
        print(f"Renamed {old_proj} to {new_proj}")

if __name__ == '__main__':
    print("Starting refactor...")
    process_files()
    rename_directories()
    print("Refactor complete.")
