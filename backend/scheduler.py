from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from models import Reservation, Table
from sqlalchemy import and_, func

def get_available_tables(db: Session, check_date: date, check_time: time, guests: int):
    """
    Finds tables that are available at the given date and time for the specific number of guests.
    Assumes a reservation lasts 1.5 hours (90 minutes).
    """
    # Define reservation duration
    duration = timedelta(minutes=90)
    check_datetime = datetime.combine(check_date, check_time)
    end_datetime = check_datetime + duration
    
    # 1. Find tables with enough capacity
    candidate_tables = db.query(Table).filter(Table.capacity >= guests).all()
    if not candidate_tables:
        return []
    
    candidate_table_ids = [t.id for t in candidate_tables]
    
    # 2. Find conflicting reservations
    # A conflict exists if a reservation starts before our end time AND ends after our start time
    # Reservation start = r.time
    # Reservation end = r.time + 90 mins
    
    # Since SQLite stores time as text or simplified format, direct comparison might be tricky depending on driver.
    # However, SQLAlchemy's standard types usually handle this. 
    # For safety with time calculations, we filter in python or do simple overlapping checks.
    # Simple overlap: (StartA < EndB) and (EndA > StartB)
    
    conflicting_reservations = db.query(Reservation).filter(
        Reservation.date == check_date,
        Reservation.table_id.in_(candidate_table_ids)
    ).all()
    
    occupied_table_ids = set()
    
    for res in conflicting_reservations:
        res_start = datetime.combine(res.date, res.time)
        res_end = res_start + duration
        
        if check_datetime < res_end and end_datetime > res_start:
            occupied_table_ids.add(res.table_id)
            
    # 3. Filter available tables
    available_tables = [t for t in candidate_tables if t.id not in occupied_table_ids]
    
    # Sort by capacity to offer best fit first (smallest sufficient table)
    available_tables.sort(key=lambda t: t.capacity)
    
    return available_tables

def generate_time_slots(start_time: time, end_time: time, interval_minutes: int = 30):
    """Generate a list of time slots."""
    slots = []
    current = datetime.combine(date.today(), start_time)
    end = datetime.combine(date.today(), end_time)
    
    while current <= end:
        slots.append(current.time())
        current += timedelta(minutes=interval_minutes)
        
    return slots

def check_daily_availability(db: Session, check_date: date, guests: int):
    """
    Returns a list of available time slots for a given date.
    Operating hours: 12:00 PM to 10:00 PM
    """
    start_time = time(12, 0)
    end_time = time(22, 0)
    all_slots = generate_time_slots(start_time, end_time)
    
    available_slots = []
    for slot in all_slots:
        tables = get_available_tables(db, check_date, slot, guests)
        if tables:
            available_slots.append(slot)
            
    return available_slots
