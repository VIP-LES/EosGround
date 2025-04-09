# EosGround

---
## About
Eos is the software platform for Georgia Tech's "Lightning from the Edge of Space" high-altitude ballooning project under the VIP program.  This module defines the ground software.  


## Installation

### Docker
1. Install Docker Desktop
2. Clone to repo: `git clone https://github.com/VIP-LES/EosGround.git`
3. Navigate to the repo: `cd EosGround`
4. run `docker-compose up -d` to start the containers

<!-- PYTHONPATH="/Users/regmi/Desktop/EosGround" python3 EosGround/radioDriver.py <-- worked for me (need to change the path) -->

## Launch info
- Run `pip install -r EosGround/requirements.txt` to install the dependencies for the radioDriver.py script
- Run the radioDriver.py script
- Start the containers
- View the logs for the pipeline container to see if there is data being picked up

<!-- ### Python
1. Install python >= 3.10 and add to PATH
2. Clone the repo: `git clone https://github.com/VIP-LES/EosGround.git`
3. Initialize virtual env: `python -m venv venv` (PyCharm can also do this for you)
4. Every time you want to enter the venv, run `source ./venv/bin/activate` (Note: If you have PyCharm initialize the venv, then the path might look like `./venv/Scripts/activate`)
5. Install dependencies: `pip install -r requirements.txt` 

Note: to exit the venv, run `deactivate`
### Database
1. Install PostgreSQL 15 and pgAdmin 4
2. When prompted to set the password for user 'postgres', set to 'password'
3. From the repository root, run `python -m EosGround.database.db_setup` to create the database

Note: on Mac sometimes the postgres server acts up, try `sudo service postgres restart` -->

## Development

### General
- Do not commit directly to main.  You must create an issue, make a branch, make a PR, and get it reviewed and approved.
- If you make a PR for the first time, add yourself to `CONTRIBUTORS.md` in your PR.

<!-- ### Adding Python Dependencies
- Run `pip install -r EosGround/requirements.txt` to install the dependencies for the radioDriver.py script -->
<!-- - In your terminal in your venv, run `pip install <your dependency>`
- Run `pip freeze` and compare the result to `requirements.txt`.  Add any new lines from the `pip freeze` output to the requirements.txt file
- You should now be able to `import <your dependency>` in your EosPayload python files
- To bump the EosLib version, run `pip install --upgrade --force-reinstall git+https://github.com/VIP-LES/EosLib@vX.Y.Z#egg=EosLib` (replace `X.Y.Z` with the version number) -->

### Data Pipelines
See docs [here](./docs/data_pipelines.md)

<!-- ## Running the OpenMCT Webserver
- To run the Django backend: navigate to the postgresDB folder and run `python manage.py runserver`
- In a new terminal, navigate to the ground-station-openmct folder and run `npm install` and then `npm start` -->