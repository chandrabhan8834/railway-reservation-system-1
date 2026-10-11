# Railway Reservation System Using DSA

A complete Railway Reservation System project built with Python, Flask, Bootstrap 5, and a MySQL-compatible database layer. The project demonstrates core Data Structures and Algorithms including queue, stack, hash table, sorting, graph traversal, BFS, and DFS in a real-world reservation workflow.

## 1. Installation

1. Open a terminal in the project folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   .\venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 2. MySQL setup

Create a MySQL database and user:

```sql
CREATE DATABASE railway_system;
CREATE USER 'railway_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON railway_system.* TO 'railway_user'@'localhost';
FLUSH PRIVILEGES;
```

Then set environment variables before starting the app:

```bash
set DB_HOST=localhost
set DB_PORT=3306
set DB_USER=railway_user
set DB_PASSWORD=your_password
set DB_NAME=railway_system
set USE_MYSQL=true
```

On Linux/macOS use `export` instead of `set`.

## 3. Database creation

The database schema is stored in `database/schema.sql`.

For MySQL, run:

```bash
mysql -u railway_user -p railway_system < database/schema.sql
```

The app also includes a SQLite fallback so it can run even when MySQL is not available. If MySQL is not configured, the app uses the local `railway.db` file.

## 4. Environment variables

The following variables are supported:

- `SECRET_KEY`: Flask app secret key
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `USE_MYSQL`

## 5. Running Flask

Start the app using:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## 6. Test credentials

Default admin account:

- Email: admin@railway.com
- Password: admin123

Default sample user:

- Email: rahul@example.com
- Password: rahul123

## 7. DSA implementation

This project intentionally implements DSA in the real logic instead of using only comments.

- Queue: Waiting list management for passengers waiting for seats.
- Stack: Cancellation history and undo flow.
- Hash Table: Fast PNR lookup for booking validation and search.
- Sorting: Train result sorting by fare, departure, arrival, or available seats.
- Graph: Railway station connectivity and route finding.
- BFS/DFS: Route traversal and route discovery between stations.

## 8. API endpoints

### Authentication
- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`

### Trains
- `GET /api/trains`
- `GET /api/trains/search`

### Bookings
- `POST /api/book`
- `GET /api/bookings`
- `GET /api/bookings/<pnr>`
- `GET /api/pnr/<pnr>`
- `POST /api/cancel/<pnr>`

### Routes
- `GET /api/routes`
- `POST /api/routes/find`

### Admin
- `POST /api/admin/trains`
- `PUT /api/admin/trains/<id>`
- `DELETE /api/admin/trains/<id>`

## 9. Project structure

```text
railway-reservation/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── railway.db
├── database/
│   ├── schema.sql
│   └── sample_data.sql
├── dsa/
│   ├── queue.py
│   ├── stack.py
│   ├── hash_table.py
│   ├── sorting.py
│   └── graph.py
├── models/
│   ├── user.py
│   ├── train.py
│   └── booking.py
├── routes/
│   ├── auth.py
│   ├── trains.py
│   ├── bookings.py
│   ├── admin.py
│   └── routes.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── search.html
│   ├── results.html
│   ├── booking.html
│   ├── confirmation.html
│   ├── pnr.html
│   ├── bookings.html
│   ├── cancel.html
│   ├── routes.html
│   └── admin/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── tests/
```

## Features summary

- User registration and login
- Train search and sorting
- Seat availability and waiting list
- Ticket booking and PNR generation
- Cancellation and refund logic
- Route finder with BFS/DFS
- Admin dashboard
- Responsive UI design

## Notes

This project is designed to demonstrate practical implementation of web development and DSA concepts for academic use.
