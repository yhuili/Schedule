Event Schedule
========
    
    
*This is an event schedule LBS*


Basic requirement:
* Python 2.7
  
  

In order to run this application, create an virtualenv for your project:

if you are on MacOSX or Linux, you can use
    
    $ sudo easy_install virtualenv
or
    
    $ sudo pip install virtualenv

if you are on Ubuntu, try
    
    $ sudo apt-get python-virtualenv
    
    
Once you have virtualenv installed, you can create a project folder and your own environment, a env folder within:
    
    $ mkdir projectname
    $ cd myproject
    $ virtualenv env
   
   
whenever you want to work on the project, you only have to activate the corresponding environment.
    
    $ . env/bin/activate

Next, set up your application with commands, also install mysql-connector-python for MySQL connection:

    $ pip install -r requirement.txt
    $ pip install -r require.txt
    $ python manage.py create_tables

Start the development server with:
    
    $ python manage.py runserver

Open your web browser with http://localhost:5000/
