"""
Directory path configuration for the project.
Works seamlessly across local, GitHub, and Google Colab environments.
"""
import os
import sys

def get_data_path(project_dir, filename):
    """
    Get the path to a data file, working across different environments.
    
    Parameters:
    -----------
    filename : str
        Name of the file in the data/ directory

    project_dir : str
        Name of the project directory (e.g., 'agec-xxx')
    
    Returns:
    --------
    str : Full path to the data file
    """
    # Check if running in Google Colab
    try:
        import google.colab
        in_colab = True
    except ImportError:
        in_colab = False
    
    if in_colab:
        # Colab: assume data is in current directory after wget
        return filename
    else:
        # Local: check for custom root directory in environment variable
        root_dir = os.getenv('PROJECT_ROOT')
        
        if root_dir:
            # Custom root directory set
            data_dir = os.path.join(root_dir, project_dir, 'data')
        else:
            # Default: relative path from script location
            # Assumes script is in scripts/ and data is in data/
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)  # Go up one level
            data_dir = os.path.join(project_root, 'data')
        
        return os.path.join(data_dir, filename)

def setup_colab_data(repo_url, filenames):
    """
    Download data files for Google Colab environment.
    
    Parameters:
    -----------
    repo_url : str
        GitHub raw content URL (e.g., 'https://raw.githubusercontent.com/user/repo/main')
    filenames : list
        List of filenames to download from data/ directory
    """
    try:
        import google.colab
        import subprocess
        
        for filename in filenames:
            file_url = f"{repo_url}/data/{filename}"
            subprocess.run(['wget', '-q', file_url], check=True)
            print(f"Downloaded: {filename}")
    except ImportError:
        print("Not in Colab environment - skipping download")