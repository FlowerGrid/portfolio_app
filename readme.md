# Flask App Template
## Setup
1. Create a virtual environment for the project
    * run these commands in the terminal from the project root directory
        - python3 -m venv venv
        - source venv/bin/activat
2. Install requrements from requirements.txt
    * Run in terminal from project's root directory
        - pip install -r requirements.txt
3. Set up your environment variables
    * Needs:
        - SECRET_KEY - string: Flask secret key. Some long random string
        - ENV_NAME - string: either 'development', 'production', or 'testing'
        - DATABASE_URL - string: The url to your database. this gets loaded into app.config as the single source of truth
4. Setup Database
    * Use whichever you like, SQLAlchemy should be able to handle it. 
        * I'm sticking with postgres for local and production so they're the same. SQLite requires batchmode which makes migrations a little messy
    * Save your database url in the environment variables as `DATABASE_URL`.
        * Flask will read this and store it in the app's config as `SQLALCHEMY_DATABASE_URI` for connecting to the database.
    * To set up the schema for the database run
    `alembic revision --autogenerate -m "initial schema"` 
    in the terminal
    * to apply migrations and populate your database run 
    `alembic upgrade head`
    in the terminal

5. Set up image hosting
    * IMAGE_STORAGE_CONTAINER - hosting environment variable
    * For local development, images are stored in static/uploads
    * This app was designed to be hosted on google cloud run using google cloud storage for image hosting.
    * Cloud run and google cloud storage are part of the same project so all the permissions already exist and the api request is really simple

## Production Initialization
1. Set up database
    * TODO
    * Cloud run-job
2. Seed user
    * TODO
    * Cloud run-Job
3. Navigate to your-app-url.com/admin/wizard-lash to login
4. Start populating your app with content
5. Hurray! 🥳

## Usage
### models.py 
this is where, you guessed it, database models live. Feel free to modify these however your app needs. The teplate starts with 2 main tables, project and blog, as well as 2 supplimentary tables that store tags for projects and blog posts.
### db_helpers.py
These helper functions gather form data and store it in the database, and pulls data from the database to display. If you make a new model, you'll need to write a new function here to get the data to display
### admin/forms.py
This is where you build the forms gathering the data that goes into the database. 
### /storage
This is where the different storage tactics live. Each tactic is a class with a single method "save()" which the app reads for storing uploads based on the ENV_NAME in your environment variables. The default for production is gcs. For now there are classes for local storage (development) and storing images on google cloud storage. If you save images somewhere else you'll need to add that logic here as a class with a method called "save()".
## Customization
### Header/Footer content
The header and footer are in the base.html template.
<br>Here you can
* Add/remove/Edit nav links
* Edit Your tagline H2
* Edit Site's catch phrase
* Add whatever information you want to the footer (please don't remove my design credits)

To edit the logo, You'll need to upload the image under settings in admin.
### Style
You can edit your custom brand colors right at the top of main/static/css file.