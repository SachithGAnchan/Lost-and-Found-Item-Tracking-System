import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session
import mysql.connector

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor(dictionary=True)

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'user')",
            (name, email, password)
        )
        db.commit()
        return redirect("/login")

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]
            session["role"] = user["role"]   # ⭐ IMPORTANT LINE
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------- HOME / DASHBOARD ----------
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

# ---------- LOST ITEM PAGE ----------
@app.route("/lost")
def lost_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("report_lost.html")

# ---------- REPORT LOST ITEM ----------
@app.route("/report-lost", methods=["POST"])
def report_lost():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    category = request.form["category"]
    description = request.form["description"]
    location = request.form["location"]
    lost_date = request.form["item_date"]

    cursor.execute(
        """
        INSERT INTO lost_items
        (title, category, description, location, lost_date, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (title, category, description, location, lost_date, session["user_id"])
    )
    db.commit()

    return "Lost item reported successfully!" 

# ---------- REPORT FOUND ITEM ----------
@app.route("/report-found", methods=["POST"])
def report_found():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    category = request.form["category"]
    description = request.form["description"]
    location = request.form["location"]
    found_date = request.form["item_date"]

    cursor.execute(
        """
        INSERT INTO found_items
        (title, category, description, location, found_date, reported_by)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (title, category, description, location, found_date, session["user_id"])
    )
    db.commit()

    return "Found item reported successfully!"

#-----------found------------#
@app.route("/found")
def found_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("report_found.html")

@app.route("/admin")
def admin_panel():
    if "user_id" not in session or session.get("role") != "admin":
        return "Unauthorized"

    cursor.execute("""
        SELECT * FROM found_items
        WHERE matched_lost_id IS NULL
    """)
    found_items = cursor.fetchall()

    return render_template("admin.html", found_items=found_items)

@app.route("/admin/match/<int:found_id>")
def match_found(found_id):
    if "user_id" not in session or session.get("role") != "admin":
        return "Unauthorized"
    
    cursor.execute("SELECT * FROM found_items WHERE found_id=%s", (found_id,))
    found = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM lost_items
        WHERE category=%s AND location=%s AND status='Open'
    """, (found["category"], found["location"]))

    lost_items = cursor.fetchall()

    return render_template("match.html", found=found, lost_items=lost_items)

@app.route("/admin/approve/<int:found_id>/<int:lost_id>")
def approve_match(found_id, lost_id):
    if "user_id" not in session or session.get("role") != "admin":
        return "Unauthorized"
    cursor.execute(
        "UPDATE found_items SET matched_lost_id=%s WHERE found_id=%s",
        (lost_id, found_id)
    )

    cursor.execute(
        "UPDATE lost_items SET status='Returned' WHERE lost_id=%s",
        (lost_id,)
    )

    db.commit()
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)