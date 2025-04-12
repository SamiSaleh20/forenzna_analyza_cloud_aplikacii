This tool automates forensic analysis of cloud storage services OneDrive,Google Drive and Dropbox by using KAPE.  
It collects relevant files and generates:
CSV reports with key forensic data.
 A summary file: `vysledok.txt`, providing a brief overview of detected cloud storage activity on the system.

Before running the script, complete the following steps:
1.download kape
2.download the PECmd from kape separatly on eric zimmerman tools https://download.ericzimmermanstools.com/net6/PECmd.zip (other version if your pc is not compatible)
3.on kape change the editor for onedrive target "OneDrive_Metadata" RecreateDirectories parameter from true to false

The code needs 4 paths to start:
1.path to kape.exe
2.path to PECmd(apllication)
3.path to what you want it to take data from (C:\ if you want analyse your pc)
4.path to folder where the outputs will be located
Example of the code starting:
python main.py "kape.exe" "PECmd" "C:\" "outputs"
