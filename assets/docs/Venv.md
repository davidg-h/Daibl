# Steps to get a virtual environment running in VS Code with python

---
-> | [Back](/README.md)
-|-

1. Step: [Install min. Python 3.9](https://www.python.org/downloads/release/python-3913/)

2. Step: Create virtual environment from requirements.txt (vscode)

    ![alternative text](docs_images/Screenshot-venv-from-requirements.png)

3. Step: [Select the virtual environment python.exe as the **python interpreter**](https://code.visualstudio.com/docs/python/environments) (vscode)

    ![alternative text](docs_images/Screenshot-virtualenv.png)

4. Step: Activate the virtual environment and update pip:

    In the terminal:

        ```sh
        pip install pip setuptools wheel --upgrade
        ```

5. Step **Important**: [Before pushing to repository, update the requirements.txt (only if new packages are used in the project)](https://pip.pypa.io/en/stable/cli/pip_freeze/)

    In the terminal:

    ```sh
    pip list # lists all packages
    pip freeze > requirements.txt 
    # alternative: python -m pip freeze > requirements.txt
    ```

<br/>

**If you get an error try this first**: (Error is related to the [ExecutionPolicy](https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows))

Open Powershell.exe as Admin and enter:

```sh
Set-ExecutionPolicy Unrestricted -Force
```

This overwrites the type of execution of scripts

### Deactivation and revert changes

```sh
# Before Reverting the ExecutionPolicy deactivate the virtual environment in the terminal
deactivate # deactivates virtual environment

Set-ExecutionPolicy Restricted -Force

Get-ExecutionPolicy # Check if Restricted is set back as default
```

To check if the virtual environment is active:

```sh
python --version
# out: Python 3.8.10
```

### Install get package/dependencies in virtuel env

```sh
pip install -r requirements.txt
```

## CLI-way

Install a python version like in step 1. Pick one of the options below to create your virtual env
```sh
python -m venv my-venv # Creates virtual env with the name my-venv. Version of venv will depend on system python version

python3.9 -m venv my-venv # Creates venv with python version 3.9 named my-venv

source my-venv/bin/activate # activates the venv
deactivate # to deactivate venv
```

Readings: [Virtual env in jupyter](https://janakiev.com/blog/jupyter-virtual-envs/), [Create venv with different versions](https://stackoverflow.com/questions/70422866/how-to-create-a-venv-with-a-different-python-version)