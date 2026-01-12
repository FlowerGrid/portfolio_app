"""
Create User CLI tool
To Run:
- 
"""
import click

def init_cli(app):
    @app.cli.command('create-user')
    @click.option('--admin', is_flag=True, help='Create user as admin')
    def create_user(admin):
        # Import necessary modules
        from .db import db_session
        from .models import User
        
        is_admin = False
        
        if admin:
            existing_admin = db_session.query(User).filter_by(is_admin=True).first()
            if existing_admin:
                print("Admin user already exists. Aborting.")
                return
            else:
                is_admin = True
        
        print('Provide user credentials. To QUIT type "q".')
        creds = prompt_user_creds()
        if creds is None:
            print('User creation cancelled.')
            return
        
        add_user_to_db(*creds, db_session, User, is_admin)

    
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


def add_user_to_db(username, email, password, db_session, User, is_admin):

    user = User(
        username=username.lower(),
        email=email.lower(),
        security_question='question',
        is_admin=is_admin
        )
    user.set_password(password)
    user.set_security_answer('answer')

    db_session.add(user)
    db_session.commit()


