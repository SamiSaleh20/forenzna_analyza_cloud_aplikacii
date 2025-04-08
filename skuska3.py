import os
import subprocess
import sys

current_directory = os.getcwd()
extracted_data=os.path.join(current_directory, "onedriveMetadata")
python_executable = sys.executable
onedriveMetadataparsed=os.path.join(current_directory, "onedriveMetadataparsed")
cmd = [
    python_executable, "odl.py", "-o",
    os.path.join(onedriveMetadataparsed,"logs"), "-k",
   extracted_data
]

subprocess.run(cmd)



