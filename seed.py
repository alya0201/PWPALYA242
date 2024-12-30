from app import create_app, db 
from app.models import User

app = create_app()

def seed_data():
    with app.app_context():

        db.drop_all()
        db.create_all()

        users =[
            User(name="John Doe", email="john@example.com"),
            User(name="Jane Smith", email="jane@example.com"),
            User(name="Alice Johnson", email="alice@example.com"),
            User(name="Bob Brown", email="bob@example.com")
        ]

        db.session.bulk_save_objects(users)
        db.session.commit()
        print("Data berhasil ditambahkan")

if __name__ == '__main__':
    seed_data()