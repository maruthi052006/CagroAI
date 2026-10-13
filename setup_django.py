import os
import subprocess
import shutil
import sys

project_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project"
os.chdir(project_dir)

# Ensure pip dependencies are installed. We assume django-admin is available.
def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

if not os.path.exists("agri_dt_backend"):
    run("python -m django startproject config agri_dt_backend")
    # Rename config folder to config (Wait, startproject config agri_dt_backend creates agri_dt_backend/config, but we want config to be the project module)

    # Let's adjust directory structure:
    # agri_dt_backend/
    #   manage.py
    #   config/
    #   apps/
    
    os.chdir("agri_dt_backend")
    os.makedirs("apps", exist_ok=True)
    
    apps_list = ["core", "accounts", "data_layer", "agents", "coordination", "simulation", "alerts", "messaging", "api", "zones"]
    for app in apps_list:
        if not os.path.exists(f"apps/{app}"):
            run(f"python manage.py startapp {app}")
            shutil.move(app, "apps/")
            
            # Update apps.py to include 'apps.' prefix in name
            app_path = f"apps/{app}/apps.py"
            with open(app_path, "r") as f:
                content = f.read()
            content = content.replace(f"name = '{app}'", f"name = 'apps.{app}'")
            with open(app_path, "w") as f:
                f.write(content)
                
    print("Scaffolding complete.")
else:
    print("Project agri_dt_backend already exists.")
