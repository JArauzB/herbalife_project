import os
import importlib
import sys

def import_all_modules_in_current_folder(file=""):
    # Get the current folder path
    current_folder = os.getcwd() + "\classes"

    # Add the current folder to sys.path if not already present
    if current_folder not in sys.path:
        sys.path.append(current_folder)

    imported_modules = {}
    # Iterate over all files in the current directory
    for filename in os.listdir(current_folder):
        # Check if the file is a Python file and not the current script
        if filename.endswith('.py') and filename != os.path.basename(__file__):
            # Remove the '.py' extension from the filename to get the module name
            module_name = filename[:-3]
            
            if file == "" or file == module_name:
                try:
                    # Dynamically import the module using importlib
                    module = importlib.import_module(module_name)
                    imported_modules[module_name] = module  # Store the imported module
                    print(f"Successfully imported {module_name}")
                except Exception as e:
                    print(f"Failed to import {module_name}: {e}")
    
    return imported_modules
