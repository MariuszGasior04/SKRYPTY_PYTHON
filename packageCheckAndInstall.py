import sys
import arcpy
import subprocess

def checkAndInstallPackage(packageName):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", packageName])
    except subprocess.CalledProcessError as e:
        arcpy.AddError(f"Nie udało się zainstalować pakietu {packageName}: {e}")
        sys.exit()

if __name__ == '__main__':
    package = arcpy.GetParameterAsText(0)

    checkAndInstallPackage(package)