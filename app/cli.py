"""
Create User CLI tool
"""

def init_cli(app):
    @app.cli.command('create-user')
    def create_user():
        print('Provide user credentials. To QUIT type "q".')

        # Import necessary modules
        from .db import db_session
        from .models import User

        creds = prompt_user_creds()
        if creds is None:
            print('User creation cancelled.')
            return
        
        add_user_to_db(*creds, db_session, User)

    
    @app.cli.command('db-rollback')
    def db_rollback_handler():
        from .db import db_session

        try:
            db_session.rollback()
            print("Database session rolled back successfully.")
        except Exception as e:
            print(f"Failed to rollback session: {e}")


def prompt_user_creds():
    while True:
        username = input('Username: ')
        if username.lower() =='q':
            return
        
        email = input('Email: ')
        if email.lower() =='q':
            return
        password = input('Password: ')
        if password.lower() =='q':
            return
        
        re_password = input('Re-enter Password: ')
        if re_password.lower() == 'q':
            return

        if password == re_password:
            return (username, email, password)
        else: 
            print('Passwords did not match. Try again\n')


def add_user_to_db(username, email, password, db_session, User):
    user = User(
        username=username.lower(),
        email=email.lower(),
        security_question='question',
        )
    user.set_password(password)
    user.set_security_answer('answer')

    db_session.add(user)
    db_session.commit()


