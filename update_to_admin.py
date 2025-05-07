from Forums.main import db, User, app 

def make_user_admin(username):
    with app.app_context():  # Ensure the app context is active
        # Query the user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"User '{username}' not found.")
            return

        user.is_admin = True
        db.session.commit()
        print(f"User '{username}' has been updated to admin.")

if __name__ == "__main__":
    username = input("Enter the username to promote to admin: ")
    make_user_admin(username)