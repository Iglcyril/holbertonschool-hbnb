from app import create_app, db

app = create_app()

with app.app_context():
    print("Suppression des tables existantes...")
    db.drop_all()
    
    print("Création des tables...")
    db.create_all()
    
    print("✅ Tables créées avec succès !")
