# Sentiment-and-Highlights
Sentiment analysis using logistic regression and highlighting important parts of a review. Performed on Django.

*Rename the project to easclepius after cloning*

To run this project you need to create a virtual environment where all libraries, Django and python should be installed. let the virtual environment be named 'venv' here.
After creating the virtual environment activate by:
source ~/.venv/bin/activate

Now you neeed to change the current working directory to the project's directory and run the command:
'python manage.py runserver'

After running the command a local host address will be generated (for eg: http://127.0.0.1:8000/), you need to type:
http://127.0.0.1:8000/hospital in a web browser.

Django with python3 is required along with the following libraries:
nltk
scipy
numpy
scikit-learn
BeautifulSoup

Some paths need to be changed in the hospital/machine.py file
/home/helios/Desktop/easclepius/easclepius/stopwords.txt  can be modified as  
/'location where the project is'/easclepius/easclepius/stopwords.txt

/home/helios/Desktop/easclepius/easclepius/wim  can be modified as
/'location where the project is'/easclepius/easclepius/wim

/home/helios/Desktop/easclepius/easclepius/finalized_model.sav  can be modified as
/'location where the project is'/easclepius/easclepius/finalized_model.sav

Some data is already loaded into the project.
More data can be added.
The logistic trained regression model is saved in a .sav file. 
