import sqlite3
from datetime import date, datetime

DB_PATH = "club_members.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop old table and recreate fresh
    cur.execute("DROP TABLE IF EXISTS members")
    cur.execute("""
    CREATE TABLE members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        plan TEXT CHECK(plan IN ('Semester','Year')),
        status TEXT CHECK(status IN ('Active','Expired')) DEFAULT 'Active',
        registration_date TEXT NOT NULL
    )
    """)
    conn.commit()
    return conn, cur

def add_member(cur, conn, name, plan, registration_date):
    if plan not in ("Semester", "Year"):
        print("❌ Invalid plan. Choose 'Semester' or 'Year'.")
        return

    # Validate date format MM/DD/YYYY
    try:
        dt = datetime.strptime(registration_date, "%m/%d/%Y")
        formatted_date = dt.strftime("%m/%d/%Y")
    except ValueError:
        print("❌ Invalid date. Use MM/DD/YYYY (e.g., 11/26/2025).")
        return

    cur.execute(
        "INSERT INTO members (name, plan, status, registration_date) VALUES (?, ?, 'Active', ?)",
        (name.strip(), plan, formatted_date)
    )
    conn.commit()
    print(f"✅ Added {name} ({plan}) on {formatted_date}.")

def show_members(cur):
    cur.execute("SELECT id, name, plan, status, registration_date FROM members ORDER BY id")
    rows = cur.fetchall()
    if not rows:
        print("\n📋 No members yet.")
        return
    print("\n📋 Club Members:")
    for mid, name, plan, status, reg in rows:
        print(f"#{mid} | {name} — {plan} — {status} — Registered {reg}")

def main():
    conn, cur = init_db()
    try:
        while True:
            print("\n--- Club Membership Registration ---")
            choice = input("Enter 'add', 'list', or 'quit': ").strip().lower()

            if choice == "add":
                name = input("Enter member's name: ").strip()
                plan = input("Enter plan (Semester/Year): ").strip().capitalize()

                default_today = date.today().strftime("%m/%d/%Y")
                reg = input(f"Enter registration date (MM/DD/YYYY) or press Enter for {default_today}: ").strip()
                registration_date = reg if reg else default_today

                add_member(cur, conn, name, plan, registration_date)

            elif choice == "list":
                show_members(cur)

            elif choice == "quit":
                print("👋 Exiting. Data saved in club_members.db")
                break

            else:
                print("❌ Invalid option.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
