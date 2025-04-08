import subprocess
import os
current_directory = os.getcwd()#cesta k projektu
kape_path = r"C:\Users\sami\OneDrive - UPJŠ\Pracovná plocha\kape\KAPE\kape.exe"
cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "onedriveMetadata"), "--tflush",
       "--target", "OneDrive_Metadata"]
subprocess.run(cmd)