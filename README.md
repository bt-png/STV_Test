# STV_Test
Development Framework for Individual Calculation Sets

Two ways to develop depending on your local computer access (Local or WebBased):

## Local Development
Utilize Visual Code, PyCharm, or other IDE for Python 3.  
Clone the 'dev' branch to your local file system and setup a new virtual environment  
* One way to setup a new virtual environment is through the command prompt. Open the command prompt and invoke ```C:\>python -m venv C:\GitRepo\STV_Test-dev```  
Install package requirements to your new local virtual environment through ```pip install -r requirements.txt```  
To render the website for use during testing, utilize the terminal command ```streamlit run main.py```  
 
## WebBased Development
Create personal user accounts for Streamlit and GitHub.  
...and so on...

# Developing your Application
Keep it simple. The less you have to 're-create the wheel' the easier it will be to incorporate into the STV hosted web application.  
Update the 'information.md' file for calculation header, instructions, references and notes.
Update the 'main.py' file for user inputs and outputs, including graphing results through 'plot.py'.  
* Stick to updating only the 'run()' definition.
* If you need more structure, create a new module and reference it under 'run()'
Update the 'formulas.py' file to handle all necessary calculations.  
Update the 'tests.py' file to make sure all formulas are providing the correct result.  

# Publishing
Congrats!
Let us know you are finished by submitting the code to a new branch in GitHub or emailing some basic information and we will respond how to move forward.
