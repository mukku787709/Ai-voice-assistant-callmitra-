import sqlite3, datetime as dt
from .config import OPEN_HOUR, CLOSE_HOUR
con = sqlite3.connect("appointments.db", check_same_thread=False)
con.execute("""CREATE TABLE IF NOT EXISTS appointments(
 id INTEGER PRIMARY KEY, phone TEXT, name TEXT, service TEXT, date TEXT, hour INT,
 status TEXT DEFAULT 'booked', UNIQUE(date, hour, status))""")

def free_slots(date: str) -> list[int]:
    taken = {r[0] for r in con.execute(
        "SELECT hour FROM appointments WHERE date=? AND status='booked'", (date,))}
    now = dt.datetime.now()
    return [h for h in range(OPEN_HOUR, CLOSE_HOUR + 1) if h not in taken
            and not (date == now.strftime("%Y-%m-%d") and h <= now.hour)]

def book(phone, name, service, date, hour) -> bool:
    if hour not in free_slots(date):
        return False
    con.execute("INSERT INTO appointments(phone,name,service,date,hour) VALUES(?,?,?,?,?)",
                (phone, name, service, date, hour))
    con.commit()
    return True

def mine(phone):
    return con.execute("SELECT id,service,date,hour FROM appointments WHERE phone=? AND status='booked' ORDER BY date,hour",
                       (phone,)).fetchall()

def cancel(phone, appt_id) -> bool:
    cur = con.execute("UPDATE appointments SET status='cancelled' WHERE id=? AND phone=? AND status='booked'",
                      (appt_id, phone))
    con.commit()
    return cur.rowcount > 0
