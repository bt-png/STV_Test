# STV_Test
Development Framework for Individual Calculation Sets

Two ways to develop depending on your local computer access (Local or WebBased):

## Local Development
Utilize Visual Code, PyCharm, or other IDE for Python 3.  
Clone the 'dev' branch to your local file system and setup a new virtual environment  
* One way to setup a new virtual environment is through your python interpreter terminal. Open the terminal and invoke ```python -m venv C:\GitRepo\STV_Test-dev``` where
'C:\GitRepo\STV_Test-dev' is the folder containing all the files downloaded.
** The reason to utilize a virtual environment is to control which python packages are loaded as to make sure their are no conflicts when deploying. All packages required
to be installed should be listed within the 'requirements.txt' file.
* Alternately to creating a new virtual environment, you may uninstall all existing packages, and then just install the ones needed for this project. With a python interpreter at the
file path of the cloned branch files, invoke ```pip freeze > uninstall.txt``` to create a text file 'uninstall.txt' of the currently installed packages. Then invoke ```pip uninstall -r requirements.txt -y```
to uninstall those packages. Finally invoke ```pip install -r requirements.txt``` to install only those packages required for this project. To reset to your original installation you can install reading your 'uninstall.txt' file.
Install package requirements to your new local virtual environment through ```pip install -r requirements.txt```  
To render the website for use during testing, utilize the terminal command ```streamlit run main.py```  
 
## WebBased Development
Create personal user accounts for Streamlit and GitHub.  
...and so on...

# Developing your Application
Keep it simple. The less you have to 're-create the wheel' the easier it will be to incorporate into the STV hosted web application.  
We suggest to read the modules and look at the rendered website in parrallel. This helps see how the code gets interpreted. Firstly, start up the defaul website by invoking ```streamlit run main.py```
With your personal website live, and your code open, you can make a small change to the python module, save, and refresh the website. The website should update to show your revision, or may display an error
message. Do this frequently to confirm there are no errors in the modifications you are making.  

Next steps are to update and customize:
* Update the 'information.md' file for calculation header, instructions, references and notes.  
* Update the 'main.py' file for user inputs and outputs, including graphing results through 'plot.py'.  
* Stick to updating only the 'run()' definition.
* If you need more structure, create a new module and reference it under 'run()'
Update the 'formulas.py' file to handle all necessary calculations.  
Update the 'tests.py' file to make sure all formulas are providing the correct result.  

# Publishing
Congrats!
Let us know you are finished by submitting the code to a new branch in GitHub or emailing some basic information and we will respond how to move forward.
