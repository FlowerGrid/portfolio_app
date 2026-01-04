# What I learned along the way
## Dev vs Production setup
* app.config['WHATEVER'] is the place to set things up.
    * Order matters. Make sure not to call on something that hasn't been defined yet
* The solution to saving images was to use app.extensions
    * First, create_app() does a conditional check to determine the environment name (local or production). Then it defines the name of the image storage backend, the image storage container (google bucket or local uploads folder), and defines which image storage class to use.
    * I was able to create 2 storage classes, one for local and one for production (in this case, Google Cloud Storage) using the same structure (name and arguments) for the save method
    * I used a host agnostic name for the image storage container so I don't accidently call for gcs while using something else like Azure. 
    * Using a different image hosting service should be as simple as building a new class for that host. 
    * Because gcs and cloud run are in the same project, my app already has permission to access my gcs bucket. I will need to do all the appropriate api stuff if I host the app somewhere else, or store images, elsewhere, or both.
    * I also needed to make a route for images stored locally so jinja sees a url, not just a filepath.
    * I shouldn't have to change anything about the app to be able to branch off and build new features/fix bugs in a local environment. Same for when merging new features/bug fixes into main.
* Pointing to the database was simple as the only time I ever call for the database url, I'm calling it from the einvironment variable anyway. So my local environment simply needs to include the the database url in the .env file. 