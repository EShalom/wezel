import os
import sys
import venv

def distribute():
    """Upload new version on PyPI
    
    IMPORTANT! First increment your version number in pyproject.toml:
    - Increment the MAJOR version when you make incompatible API changes.
    - Increment the MINOR version when you add functionality in a backwards compatible manner.
    - Increment the PATCH version when you make backwards compatible bug fixes.

    You need: PyPI username and password
    """

    install()

    os.system(activate() + ' && ' + 'pip install --upgrade build')
    os.system(activate() + ' && ' + 'python -m build')
    os.system(activate() + ' && ' + 'pip install --upgrade twine')
    os.system(activate() + ' && ' + 'twine upload dist/*')

def document():
    """Generate documentation"""

    install()

    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, 'docs')
    if not os.path.isdir(path):
        os.mkdir(path)

    print('Generating documentation..')
    os.system(activate() + ' && ' + 'pdoc --html -f -c sort_identifiers=False --output-dir ' + str(path) + ' dbdicom')

def activate():
    """Active virtual environment"""

    venv_dir = os.path.join(os.getcwd(), ".venv")
    os.makedirs(venv_dir, exist_ok=True)
    venv.create(venv_dir, with_pip=True)
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        return os.path.join(venv_dir, "Scripts", "activate")
    else: # MacOS and Linux
        return '. "' + os.path.join(venv_dir, "bin", "activate")

def install():
    """Install requirements to a virtual environment"""

    print('Creating virtual environment..')
    os.system('py -3 -m venv .venv')

    print('Installing requirements..')
    os.system(activate() + ' && ' + 'py -m pip install -r requirements.txt')


if __name__ == '__main__':

    distribute()