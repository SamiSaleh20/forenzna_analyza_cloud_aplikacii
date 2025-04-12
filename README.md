this code is supposed to make forenscis analysis of cloud storages Onedrive GoogleDrive and Dropbox more easier.
Using kape it takes files and then made the important files for forenscis analyse into csv files and also made a brief overview "vysledok.txt" where are some basic informations about the cloud storages in system.

Before starting the code this steps must be made:
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
