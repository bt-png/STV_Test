# STV_Test
Development Framework for Individual Calculation Sets

Two ways to develop depending on your local computer access (WebBased or Local):
* For simple testing purposes, the WebBased approach is preferred. Once you have decided you want to be a continued contributer, spending the time to setup a Local environment is worth it.

## WebBased Development
Create personal user account for GitHub and go to the GitHub Codespaces website (https://github.com/codespaces).
Create a new codespace and utilize the repository ```bt-png/STV_Test```
A new browser window should be launched with a python terminal to continue.
* Once finished developing and you save the files locally, remember to go back to the codespaces website and delete the created space.

## Local Development
Utilize Visual Code, PyCharm, or other IDE for Python 3.  
Clone the 'dev' branch to your local file system and setup a new virtual environment  
* One way to setup a new virtual environment is through your python interpreter terminal. Open the terminal and invoke ```python -m venv C:\GitRepo\STV_Test-dev``` where
'C:\GitRepo\STV_Test-dev' is the folder containing all the files downloaded.
* The reason to utilize a virtual environment (web or local) is to control which python packages are loaded as to make sure their are no conflicts when deploying. All packages required
to be installed should be listed within the 'requirements.txt' file.
You can run ```pip freeze``` from the terminal to print out which packages are installed. If there are any loaded, you may uninstall all existing packages, and then just install the ones needed for this project. With a python interpreter at the file path of the cloned branch files, invoke ```pip freeze > uninstall.txt``` to create a text file 'uninstall.txt' of the currently installed packages. Then invoke ```pip uninstall -r uninstall.txt -y``` to uninstall those packages.

## Finish setting up (WebBased or Local)
Finally invoke ```pip install -r requirements.txt``` to install only those packages required for this project. 
Their are two sample Virtual CalcPads available for you to start with, ```SingleCalc.py``` and ```MultiCalc.py```
To render the website for use during testing, utilize the terminal command ```streamlit run SingleCalc.py```  or ```streamlit run MultiCalc.py```  
 
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
* Utilize markdown language to render mathmatical equiations within the 'markdown' definition. Reference 'https://www.upyesp.org/posts/makrdown-vscode-math-notation/' for some syntax.  
Update the 'tests.py' file to make sure all formulas are providing the correct result.  

# Publishing
Congrats!
Let us know you are finished by submitting the code to a new branch in GitHub or emailing some basic information and we will respond how to move forward.
