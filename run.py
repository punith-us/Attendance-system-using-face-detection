import subprocess

# Define the path 
bash_script = './run_recognise_script.sh'

# Run the Bash script using subprocess
try:
    subprocess.run(['bash', bash_script], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running Bash script: {e}")