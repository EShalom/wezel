import os
from sys import platform
import venv

# Write the name of the extra Python Packages for development here
extra_packages = ['dipy==1.3.0', 'fslpy==3.0.0', 'scikit-image', 'scikit-learn', 'SimpleITK', 'itk-elastix', 'ukat', 'mdr-library']

print("Creating Python Virtual Environment...")
venv_dir = os.path.join(os.getcwd(), "venv")
icon_file = os.path.join(os.getcwd(), "Documents" , "images" , "favicon.ico")
icon_png = os.path.join(os.getcwd(), "Documents" , "images" , "uni-sheffield-logo.png")
os.makedirs(venv_dir, exist_ok=True)
venv.create(venv_dir, with_pip=True)

print("Activating the Python Virtual Environment created...")
# Windows
if platform == "win32" or platform == "win64" or os.name == 'nt':
	activation_command = '"' + os.path.join(venv_dir, "Scripts", "activate") + '"'
# MacOS and Linux
else:
	activation_command = '. "' + os.path.join(venv_dir, "bin", "activate") + '"'

print("Installing Python packages in the Virtual Environment...")
os.system(activation_command + ' && pip install -e .')
for pypi in extra_packages:
	os.system(activation_command + ' && pip install ' + pypi)

print("Cleaning up installation files...")
os.system(activation_command + ' && python setup.py clean')

print("Starting compilation...")
os.system(activation_command + ' && pyinstaller --name wezel --clean --onefile --noconsole --additional-hooks-dir=. --noconfirm --splash wezel.jpg exec.py')

print("Cleaning up compilation files...")
# Windows
if platform == "win32" or platform == "win64" or os.name == 'nt':
	os.system('move dist\* .')
	os.system('rmdir build /S /Q')
	os.system('rmdir dist /S /Q')
	os.system('del Weasel.spec')
	print("Deleting the created Python Virtual Environment for the process...")
	os.system('rmdir venv /S /Q')
# MacOS and Linux
else:
	os.system('mv dist/* .')
	os.system('rm -rf build/ dist/')
	os.system('rm Weasel.spec')
	print("Deleting the created Python Virtual Environment for the process...")
	os.system('rm -r venv/')


# If compiled in MacOS, we need to change permissions and add the icon manually.
if platform == "darwin" or os.name == 'posix':
	os.system('sudo chmod 775 Weasel')
	os.system('sips -i ' + str(icon_png))
	os.system('DeRez -only icns ' +  str(icon_png) + ' > icon.rsrc')
	os.system('Rez -append icon.rsrc -o Weasel')
	os.system('SetFile -a C Weasel')
	os.system('rm -f icon.rsrc')

print("Binary file successfully created and saved in the Weasel repository!")