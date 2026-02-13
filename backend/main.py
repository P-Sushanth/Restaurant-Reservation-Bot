from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, time
from pydantic import BaseModel
import sys

from database import Base, engine, get_db
from models import Menu, Table, Reservation
from compression import compress_menu_data
from scheduler import check_daily_availability, get_available_tables
from chatbot import bot

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic Schemas
class ReservationCreate(BaseModel):
    name: str
    phone: str
    guests: int
    date: date
    time: time

class ChatRequest(BaseModel):
    message: str

# Endpoints
@app.get("/menu")
def get_menu(db: Session = Depends(get_db)):
    """
    Returns menu items.
    Demonstrates compression performance in console logs.
    """
    menu_items = db.query(Menu).all()
    # Convert to list of dicts for compression function
    menu_list = [
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "is_veg": item.is_veg,
            "available": item.available,
            "description": item.description
        }
        for item in menu_items
    ]
    
    # Compress just to measure and log
    _, stats = compress_menu_data(menu_list)
    print(f"DEBUG: Menu Compression Stats: {stats}")
    
    return menu_list

@app.get("/menu/compressed")
def get_menu_compressed(db: Session = Depends(get_db)):
    """
    Returns stats about compressed menu data to demonstrate optimization.
    """
    menu_items = db.query(Menu).all()
    menu_list = [
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "is_veg": item.is_veg,
            "available": item.available,
            "description": item.description
        }
        for item in menu_items
    ]
    
    _, stats = compress_menu_data(menu_list)
    return stats

@app.get("/availability")
def check_availability(check_date: date, guests: int, check_time: Optional[time] = None, db: Session = Depends(get_db)):
    """
    Check availability for a specific date (and optional time).
    """
    if check_time:
        tables = get_available_tables(db, check_date, check_time, guests)
        return {"available": len(tables) > 0, "available_tables": len(tables)}
    else:
        slots = check_daily_availability(db, check_date, guests)
        return {"date": check_date, "available_slots": slots}

@app.post("/reserve")
def make_reservation(req: ReservationCreate, db: Session = Depends(get_db)):
    """
    Create a new reservation.
    """
    tables = get_available_tables(db, req.date, req.time, req.guests)
    
    if not tables:
        raise HTTPException(status_code=400, detail="No availability for this time.")
        
    # Assign the first available table
    table = tables[0]
    
    new_reservation = Reservation(
        name=req.name,
        phone=req.phone,
        guests=req.guests,
        date=req.date,
        time=req.time,
        table_id=table.id
    )
    
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    return {"status": "confirmed", "reservation_id": new_reservation.id, "table_id": table.id}

@app.delete("/cancel/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
        
    db.delete(reservation)
    db.commit()
    return {"status": "cancelled"}

@app.post("/chat")
def chat(req: ChatRequest):
    """
    Chatbot endpoint.
    """
    response = bot.get_response(req.message)
    return response

# Middleware for CORS (important for frontend)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
