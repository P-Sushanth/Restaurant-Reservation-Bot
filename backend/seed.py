from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Menu, Table

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Clear existing data
    db.query(Menu).delete()
    db.query(Table).delete()
    
    # Add Tables
    # 5 small tables (2 ppl), 5 medium (4 ppl), 2 large (6 ppl)
    tables = []
    for _ in range(5):
        tables.append(Table(capacity=2))
    for _ in range(5):
        tables.append(Table(capacity=4))
    for _ in range(2):
        tables.append(Table(capacity=6))
        
    db.add_all(tables)
    
    # Add Menu Items
    menu_items = [
        Menu(name="Truffle Pasta", category="Main", price=25, is_veg=True, description="Homemade fettuccine with truffle cream"),
        Menu(name="Grilled Salmon", category="Main", price=30, is_veg=False, description="Atlantic salmon with asparagus"),
        Menu(name="Caesar Salad", category="Starter", price=12, is_veg=False, description="Classic caesar with croutons"),
        Menu(name="Vegetable Curry", category="Main", price=18, is_veg=True, description="Spicy coconut curry with seasonal veg"),
        Menu(name="Chocolate Lava Cake", category="Dessert", price=10, is_veg=True, description="Warm cake with vanilla ice cream"),
        Menu(name="Bruschetta", category="Starter", price=8, is_veg=True, description="Toasted bread with tomatoes and basil"),
    ]
    
    db.add_all(menu_items)
    
    db.commit()
    print("Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_data()
