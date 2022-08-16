# API DOCUMENTATION TO GET DATA SCIENTISTS SALARY

## INSTALLATION

If you want to test it locally just follow the next steps 

If you don't have Docker please install it with the right Operating system on this link : [installation tutorial](https://docs.docker.com/engine/install/)

Once you have installed Docker please check the version to make sure it is running

`docker --version`

You should get something like this : **Docker version 20.10.11, build etc.**

Clone this repo locally with one of the two options below:

- Remote Git repos connection via HTTPS:

`git clone https://github.com/alexisflipo/api_final_project.git`

- Remote Git repos connection via SSH:

`git clone git@github.com:alexisflipo/api_final_project.git`

Once the repository is clone locally go to the repos'root :

`cd api_final_project`

## Test locally with Uvicorn

Then, you need to install the project's python libraries and dependencies. 

*Make sure you have Python3 installed.*

Run `pip install -r requirements.txt`

Now, you can check locally if the api is working by running :

`uvicorn src.app:app --reload`

Then, click on the link provided by the terminal logs. You can now request the API locally


## Test in a production-like environment with Docker

If you want to check if it working  with a production environment you can try it by running these following commands:

`docker build -t fastapidssalary:latest -f Dockerfile .`

Once it is finished just run:

`docker run -p 80:80 fastapidssalary:latest`

Now you can click on the like provided by the terminal logs or access to `http://0.0.0.0:80` in the url bar.

**CONGRATS YOU MADE IT**