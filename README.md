# project-il-legible


## Web Framework

For this project, we'll be using the Flask web framework. This tool allows us to keep and maintain and lightweight database, spin up a web server, serve HTML/CSS files to a browser, and more. Read more about it [here](https://flask.palletsprojects.com/en/stable/#user-s-guide).

There are a few steps to take to get the app up and running on your machine. Once completed, you'll be able to work with the project.

### Initializing the Database

Since we don't check the database into version control, you'll need to intiialize (create) and seed the database - populating it with all of the relevant data we'll be using in our app. To initialize, run this from the command line in the root directory of the project:

`uv run flask --app flaskr init-db`

Once this has ran, you should see a `flaskr.sqlite` file in the `instance` folder of the project.

### Seeding the Database

`TO-DO: write this section`

### Running the Web App

After the database has been created and seeded with data, we can finally spin up the web server to run our app:

`uv run flask --app flaskr run --debug`

## Environment Variables

This project makes use of several APIs that require API keys for endpoint requests. Many of these will require API keys which are not to be checked into version control for security reasons. Instead, we will be using an envrionment file - a file that keeps track of the API keys, sensitive info, and specific configuration settings for your local program. Following these steps, you may set up your own environment file with custom variables defined:

1. Run `touch .env` in the same directory as your `uv.lock` 
2. Run `echo UV_ENV_FILE=.env` to tell where UV where to look for the environment file.
3. Populate the .env file with key-value pairs delimited with an equal sign, e.g. `MY_KEY="123"`

Please ensure that the `.env` file is included in the `.gitignore` and that it IS NOT checked into version control.

## Data Exploration

The APIs for Open States and Illinois Sunshine have some significant rate limit barriers in place that would make the aggregate analysis of things like bills and sponsors VERY slow and painstaking. Instead, we are leveraging bulk data (CSVs) to accomplish this analysis. An `exploration` module has been created that will pull data from the `bulk_data` directory into Pandas data frames. You may add additional functions to this module if you have the need to explore different datasets. To actually interact with these functions, you can edit the `Exploration.ipynb` file in the root directory, or create your own (please exclude from version control).

### Adding Bulk Data

If you'd like to add bulk data for Open States, you'll need to do this manually (for now.) Go to https://open.pluralpolicy.com/data/, find the relevant data set for the IL session you're looking for, download, and unpack it. The result should be a set of .csv files under a directory structure that looks like `IL/[# session]`. At this point, you may merge these files with the `exploration/bulk_data` directory in the repo - just make sure the directory structure is maintained, since the `explore.py` "data get" methods rely on this.

### Setting up Jupyter in VS Code

1. Run `uv sync` in the root directory to ensure that the ipykernel package is installed.
2. Install the Jupyter VS Code extension (this will let you work with notebooks natively in VS Code)
3. If you change `explore.py`, you'll need to restart the Jupyter kernel by clicking the "Restart" button in the VS Code interface.
4. As usual, any packages you'd like to import into the Jupyter notebook will need to be added to the virutal environment with `uv add`.



