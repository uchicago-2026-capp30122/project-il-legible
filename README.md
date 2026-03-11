# Project IL-legible
See the website in action at https://www.project-il-legible.com/

## About
Project IL-legible attempts to analyze and understand the intersection of bill sponsorship and financial contributions to legislatures of the Illinois State General Assembly. We pull and join data from different data sources to accomplish this, in addition to reporting on the more interesting findings that we've been able to uncover. Our primary goal is to make Illinois legislation data more accessible and readable for a wider audience.

Team Members: 
- Brock Sauvage <bsauvage@uchicago.edu>
- Elie Nowlis <enowlis@uchicago.edu>
- Max Manalang <manalang@uchicago.edu>
- Luke Friedman <lukef@uchicago.edu>

Data Sources:
- Open States (https://open.pluralpolicy.com/data/)
- Illinois Sunshine (https://illinoissunshine.org/)

A screenshot of a page on the website and a quick video walk-through are included below.

![alt text](images/image.png)

Project video: [a link to your project video] TO DO

## Instructions

### Web Framework

For this project, we'll be using the Flask web framework. This tool allows us to keep and maintain and lightweight database, spin up a web server, serve HTML/CSS files to a browser, and more. Read more about it [here](https://flask.palletsprojects.com/en/stable/#user-s-guide).

There are a few steps to take to get the app up and running on your machine. Once completed, you'll be able to work with the project.

### Adding Bulk Data

You will first need to manually add bulk data from Open States. Go to https://open.pluralpolicy.com/data/session-csv/, find the relevant data set for the IL session you're looking for, download, and unpack it. This project uses the **`Illinois 102nd Regular Session`** and **`Illinois 103rd Regular Session`** files.

The result should be a set of `.csv` files under a directory structure that looks like `IL/[# session]`. Each session directory should contain all of the associated `.csv` files. At this point, you may merge these files with the `data_pull_and_clean\pull_open_states\bulk_data` directory in the repo - just make sure the directory structure is maintained, since the `get_bulk_data.py` "data get" methods rely on this.


### Initializing the Database

Since we don't check the database into version control, you'll need to intiialize (create) and seed the database - populating it with all of the relevant data we'll be using in our app. To initialize, run this from the command line in the root directory of the project:

`uv run flask db init`
`uv run flask db upgrade`

Once this has ran, you should see a `app.db` file in the `instance` folder of the project.

### Seeding the Database

To get data in your database, first ensure you have the bulk data files for Open States in the correct directories, and then run:

`bash create_datasets.sh` (or whatever command you use to execute a shell script)

This process should take a few minutes, and it will create `final_data/bills.csv` and `final_data.sponsors.csv`. Once you have these, you are ready to seed the database. Make sure you have intiialized the DB using the command above, and then run:

`uv run flask dbc seed`

The database should now have data. If you find yourself needing to reseed the database, you can drop and recreate the tables before rerunning the seed command:

`uv run flask dbc drop-tables`
`uv run flask dbc create-tables`

### Exploring the Database

During development, it will be necessary to explore the data and test out queries before running them in the server-side handlers. An easy way to do that is as follows:

`uv run flask shell`

The above command will start a Python shell with a create app context - which allows you to access the app object and database as if it were running live. Now, you can run queries on the models like this:

```
>>> query = sa.select(Sponsor)
>>> db.session.scalars(query).first()
```

Please refer to SQLAlchemy documentation for specific methods and syntax for querying tables within the database.

### Running the Web App

After the database has been created and seeded with data, we can finally spin up the web server to run our app:

`uv run flask run --debug`

Then, navigate to `localhost:5000` in order to view the site.

## Environment Variables

If you'd like to use a non-SQLite database, you may create a `.env` file in the root directory and include `DATA_BASEURL` with an associated path to a DB instance. Please refer to Flask documentation for specific formatting. If you omit the `.env` file or the DATABASE_URL then a SQLite database instance will be created within the `instance` directory.


