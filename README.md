# KAKSHYA - A Web Application

### About

Kakshya is a web app with a concept to provide a less expensive online information sharing web application to provide
just the features we need and to provide a same place for the different tasks that we've been using for various tasks.

To elaborate, the covid situation made us do various things, made us locked up in the house for months, introduce a
relatively whole new teaching learning system that changed the way we study. But now, since it's been cooling down and
everything seems to be normal, we are trying to get back to our normal lives, physical classes have been arranged, and
we are getting out more. So in this situation, we thought why not have our own application that provides all the
features we need since we are normalizing with the situation. This is where **Kakshya** comes in.

### Objectives

* Simple easy and accessible UI
* Platform for teachers and students for sharing information
* Provide control over own data

### Tools Used

* Django
* Python
* VSCode
* PyCharm

### How to run this project

You can run this project following steps given below:

###### Step 1:

Make sure python 3.8+ is installed on your system. you can check this with following command in your system terminal.

```shell
$ python --version
```

> In linux or mac systems you might have to type python3 instead of python as command

> If you do not get python 3.8 or you get some error like not recognized, you can install it from
> [python downloads page](https://www.python.org/downloads/).

###### Step 2:

So now you have python installed, you must make sure `virtualenv` is installed you can do so by following command in
your terminal.

`pip install virtualenv` <br>
or<br>
`python -m pip install virtualenv` or `python3 -m pip install virtualenv`

> **Tip**: Use the `python` or `python3` based on the command you used in the *Step 1* to get the python version.

###### Step 3

Let's create the virtualenv now, to know more about virtualenv, refer to
their [docs](https://virtualenv.pypa.io/en/latest/). or you can simply type following command,

```shell 
$ virtualenv venv # This creates your virtual environment with name venv

$ python -m virtualenv venv # if above command doesnot work

# Use python or python3 as per your system
```

###### Step 4
Now, it's time we activate the virtual environment
 - On Windows
```shell
$ .\venv\Scripts\activate 
```
 - On Linux/MacOS
```shell
$ source venv/bin/activate
```

###### Step 5
Now we should install all the dependencies for our project. Follow the command below:
```shell
$ pip install -r requirements.txt
```

> Make sure you are now on the file level where you see both folder `venv` and `manage.py` when you list all the files.
>

###### Step 6
Now the environment variables need to be created. Just copy the `env.example` file and change the content with the credentials as you need and save the copy file as `.env`.

- On Windows powershell or on *nix OS you can use the following command to copy the file.
```shell
$ cp .env.example .env
```
> The above command will copy the file and rename it as `.env` in the same working  directory.

###### Step 7
Time to migrate the databases. Use the following command to migrate database.
```shell
$ python manage.py migrate
```

###### Step 8
Now everything is set up, so, we shall be ready to start the server. Enter the following command in your command line.
```shell
$ python manage.py runserver 
```
> Now the server should be up and will be running on port `8000`, or hit [https://127.0.0.1:8000](https://127.0.0.1:8000)
### Contributors

    - Anjal Bam(THA075BEI006) 