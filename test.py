from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter as ctk
from db import connect_db
from datetime import date
import matplotlib.cm as cm
from patient import add_patient, update_patient, delete_patient
from doctor import add_doctor, update_doctor, delete_doctor
from inventory import add_item, update_item, delete_item
from appointments import add_appointment, update_appointment, delete_appointment
from billing import add_bill, update_bill, delete_bill
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import HRFlowable
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from PIL import Image

import tkinter as tk
from tkinter import font, ttk
import calendar as pycalendar

milker_font_tk = ("Milker", 14)

from matplotlib import font_manager

milker_font = font_manager.FontProperties(
    fname=r"C:\Users\HK\Desktop\The Eunoia Project\Milker.otf"
)

DARK_BG = "#1e1e1e"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1500x900")
app.title("Eunoia Health Management System")

# Shared dark styling for every ttk data table. Configure once, before tables are created.
table_style = ttk.Style()
table_style.theme_use("clam")
table_style.configure(
    "Eunoia.Treeview",
    background="#242424",
    foreground="white",
    fieldbackground="#242424",
    rowheight=30,
    borderwidth=0,
    font=("Arial", 10)
)
table_style.configure(
    "Eunoia.Treeview.Heading",
    background="#1f6aa5",
    foreground="white",
    relief="flat",
    font=("Arial", 10, "bold")
)
table_style.map(
    "Eunoia.Treeview",
    background=[("selected", "#35556b")],
    foreground=[("selected", "white")]
)
table_style.map(
    "Eunoia.Treeview.Heading",
    background=[("active", "#2f7db8")]
)


# ===== LOGIN SCREEN =====
login_frame = ctk.CTkFrame(app, fg_color=DARK_BG)
login_frame.pack(fill="both", expand=True)

login_box = ctk.CTkFrame(
    login_frame,
    width=350,
    height=450,
    corner_radius=15,
    fg_color="#2a2a2a"
)

login_box.place(relx=0.5, rely=0.5, anchor="center")
login_box.pack_propagate(False)   # 👈 IMPORTANT (prevents shrinking)
# Logo (optional)
logo_img = ctk.CTkImage(
    light_image=Image.open(r"C:\Users\HK\Desktop\The Eunoia Project\logo.png"),
    size=(140, 110)
)
ctk.CTkLabel(login_box, image=logo_img, text="").pack(pady=(20,15))

ctk.CTkLabel(
    login_box,
    text="LOGIN",
    font=("Milker", 22, "bold")
).pack(pady=(5,15))

user_entry = ctk.CTkEntry(login_box, placeholder_text="Username")
user_entry.pack(fill="x", padx=55, pady=10)

# Password field with an eye button to toggle visibility.
password_row = ctk.CTkFrame(login_box, fg_color="transparent")
password_row.pack(fill="x", padx=55, pady=10)

pass_entry = ctk.CTkEntry(password_row, placeholder_text="Password", show="*")
pass_entry.pack(side="left", fill="x", expand=True)

password_visible = False

def toggle_password_visibility():
    global password_visible
    password_visible = not password_visible
    pass_entry.configure(show="" if password_visible else "*")
    password_eye_button.configure(text="🙈" if password_visible else "👁")

password_eye_button = ctk.CTkButton(
    password_row,
    text="👁",
    width=36,
    height=32,
    corner_radius=8,
    fg_color="transparent",
    hover_color="#3a3a3a",
    text_color="white",
    command=toggle_password_visibility
)
password_eye_button.pack(side="left", padx=(5, 0))

error_label = ctk.CTkLabel(login_box, text="", text_color="red")
error_label.pack(pady=5)

def login():
    username = user_entry.get().strip()
    password = pass_entry.get().strip()

    if username == "Eunoia" and password == "Tohubohu007":
        login_frame.pack_forget()
        app_main.pack(fill="both", expand=True)
    else:
        error_label.configure(text="Invalid username or password")

ctk.CTkButton(login_box, text="Login", command=login, width=150).pack(pady=10)


# ===== SIDEBAR =====
# ===== MAIN APP CONTAINER =====
app_main = ctk.CTkFrame(app, fg_color=DARK_BG)
app_main.pack(fill="both", expand=True)

app_main.pack_forget()

# ===== SIDEBAR =====
sidebar = ctk.CTkFrame(app_main, width=220, fg_color=DARK_BG)
sidebar.pack(side="left", fill="y")

# ===== MAIN AREA =====
main = ctk.CTkFrame(app_main, fg_color=DARK_BG)
main.pack(side="left", fill="both", expand=True)

logo_img = ctk.CTkImage(
    light_image=Image.open(r"C:\Users\HK\Desktop\The Eunoia Project\logo.png"),  # 👈 your path
    size=(180, 120)   # 👈 adjust size
)

ctk.CTkLabel(
    sidebar,
    image=logo_img,
    text=""
).grid(row=0, column=0, pady=(20,20))


# ===== HEADER =====
header = ctk.CTkFrame(main, height=60, fg_color=DARK_BG)
header.pack(fill="x")

ctk.CTkLabel(
    header,
    text="EUNOIA HEALTH MANAGEMENT SYSTEM",
    font=("Moralana", 22, "bold"),
    text_color="white"
).pack(pady=10)

# ===== CONTENT AREA (THIS IS IMPORTANT) =====
content = ctk.CTkFrame(main, fg_color=DARK_BG)
content.pack(fill="both", expand=True)

ctk.CTkFrame(content, height=2, fg_color="#2a2a2a").pack(fill="x")

# ===== FRAMES =====
pages = ["dashboard", "patients", "appointments", "inventory", "doctors", "bills"]
frames = {}

for name in pages:
    f = ctk.CTkFrame(content, fg_color=DARK_BG)
    f.place(relx=0, rely=0, relwidth=1, relheight=1)
    frames[name] = f


def show_frame(name):
    frames[name].tkraise()

# Patients is one sidebar section with two internal pages.
patient_tabs = ctk.CTkTabview(
    frames["patients"],
    fg_color=DARK_BG,
    segmented_button_fg_color="#292929",
    segmented_button_selected_color="#1f6aa5",
    segmented_button_selected_hover_color="#2f7db8",
    segmented_button_unselected_color="#292929",
    segmented_button_unselected_hover_color="#3a3a3a",
    text_color="white"
)
patient_tabs.pack(fill="both", expand=True, padx=10, pady=10)
patient_registration_tab = patient_tabs.add("Register Patient")
patient_list_tab = patient_tabs.add("Patient List")

# ===== SIDEBAR BUTTONS =====
sidebar.grid_columnconfigure(0, weight=1)

for i in range(len(pages)):
    sidebar.grid_rowconfigure(i, weight=3)

for i, name in enumerate(pages, start=1):
    btn = ctk.CTkButton(
        sidebar,
        text={"patients": "Patients"}.get(name, name.capitalize()),
        command=lambda n=name: show_frame(n),
        font=("Milker", 16),

        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#333333",

        height=55
    )
    btn.grid(row=i, column=0, sticky="nsew", padx=10, pady=7)
    
# ===== DB =====
def fetch(q, params=None):
    conn = connect_db()
    c = conn.cursor()
    try:
        if params is None:
            c.execute(q)
        else:
            c.execute(q, params)
        data = c.fetchall()
        return data
    finally:
        c.close()
        conn.close()

from datetime import datetime

def format_input_date(d):
    """Convert user-entered DD/MM/YYYY to MySQL YYYY-MM-DD."""
    try:
        return datetime.strptime(d.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date. Enter the date as DD/MM/YYYY, e.g. 19/10/2026.")

def display_date(value):
    """Convert a MySQL date (or date string) to DD/MM/YYYY for display."""
    if value is None or value == "":
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return str(value)

# ================= DASHBOARD =================
dash = frames["dashboard"]

cards = ctk.CTkFrame(dash, fg_color=DARK_BG)
cards.pack(fill="x", pady=5)
cards.grid_columnconfigure((0,1,2,3), weight=1)

def card(parent, title, value, col):
    c = ctk.CTkFrame(
        parent,
        corner_radius=16,
        fg_color="#1f6aa5",
        border_width=1,
        border_color="#35556b"
    )
    c.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")

    ctk.CTkLabel(
        c, text=title, text_color="white",
        font=("Milker", 15)
    ).pack(pady=(10, 2))

    ctk.CTkLabel(
        c, text=value, font=("Milker", 22, "bold"),
        text_color="white"
    ).pack(pady=(0, 10))

    return c

dashboard_cards = []

def refresh_dashboard():
    for widget in dashboard_cards:
        widget.destroy()
    dashboard_cards.clear()

    rev = fetch("SELECT IFNULL(SUM(total),0) FROM bills")[0][0]
    pat = fetch("SELECT COUNT(*) FROM patients")[0][0]
    pending = fetch(
        "SELECT IFNULL(SUM(total),0) FROM bills "
        "WHERE LOWER(payment_status)='pending'"
    )[0][0]
    appt = fetch("SELECT COUNT(*) FROM appointments")[0][0]

    dashboard_cards.extend([
        card(cards, "TOTAL REVENUE", f"₹{float(rev or 0):,.2f}", 0),
        card(cards, "TOTAL PATIENTS", f"{pat:,}", 1),
        card(cards, "PENDING PAYMENTS", f"₹{float(pending or 0):,.2f}", 2),
        card(cards, "APPOINTMENTS", f"{appt:,}", 3),
    ])

refresh_dashboard()



# ===== GRAPH AREA =====
bottom = ctk.CTkFrame(dash, fg_color=DARK_BG)
bottom.pack(fill="both", expand=True)

# grid setup
for i in range(3):
    bottom.grid_columnconfigure(i, weight=1)
    bottom.grid_rowconfigure(i, weight=1)

def graph(q, title, row, col, kind="bar", xlabel="", ylabel=""):
    f = ctk.CTkFrame(bottom, fg_color=DARK_BG)
    f.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    fig = plt.Figure(figsize=(3.6,2.6), facecolor=DARK_BG)
    ax = fig.add_subplot(111)   # ✅ CREATE AX FIRST

    ax.set_facecolor(DARK_BG)

    data = fetch(q)
    data = list(reversed(data))   # 👈 fixes order after DESC

    from datetime import datetime

    def format_date(d):
        try:
            return datetime.strptime(str(d), "%Y-%m-%d").strftime("%d/%m")
        except:
            return str(d)

    x = [format_date(i[0]) for i in data]
    y = [i[1] for i in data]

    if kind == "line":
        ax.plot(
            x, y,
            color="white",
            linewidth=4,     # thicker
            alpha=0.6        # subtle
            )

        ax.plot(
            x, y,
            color="#2f6ea5",
            linewidth=2,
            marker="o"
            )
    else:
        ax.bar(
            x, y,
            color="#2f6ea5",
            edgecolor="white",   # 👈 THIS adds border
            linewidth=1.5        # 👈 thickness
            )

    # ✅ TITLE
    fp = milker_font.copy()
    fp.set_size(14)
    fp.set_weight("bold")
    ax.set_title(title, color="white", fontproperties=fp, pad=12)

    # ✅ AXIS LABELS (NOW SAFE)
    ax.set_xlabel(xlabel, color="white", fontsize=10)
    ax.set_ylabel(ylabel, color="white", fontsize=10)

    # ✅ TICKS
    ax.tick_params(axis='x', colors='white', rotation=0, labelsize=10)
    ax.tick_params(axis='y', colors='white', labelsize=10)

    # ✅ GRID
    ax.grid(True, linestyle='--', linewidth=0.5, color="#3a3a3a")

    for spine in ax.spines.values():
        spine.set_visible(False)

    # ✅ SPACING
    fig.subplots_adjust(
        top=0.85,
        bottom=0.35,
        left=0.20,
        right=0.95
    )

    canvas = FigureCanvasTkAgg(fig, master=f)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def donut_chart(q, title, row, col):
    f = ctk.CTkFrame(bottom, fg_color=DARK_BG)
    f.grid(
        row=row, column=col, rowspan=3,
        padx=10, pady=10, sticky="nsew"
    )

    fig = plt.Figure(figsize=(4.5, 3), facecolor=DARK_BG)
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.82)

    data = fetch(q)
    labels = [str(d[0]) for d in data]
    sizes = [float(d[1] or 0) for d in data]

    # Ignore zero or negative values for the pie chart.
    chart_data = [
        (label, size)
        for label, size in zip(labels, sizes)
        if size > 0
    ]

    if not chart_data:
        ax.text(
            0.5, 0.5,
            "No payment data yet",
            ha="center",
            va="center",
            color="white",
            fontsize=12,
            transform=ax.transAxes
        )
        ax.set_title(title, color="white", pad=20)
        ax.set_axis_off()

    else:
        labels = [item[0] for item in chart_data]
        sizes = [item[1] for item in chart_data]

        color_values = [0.4, 0.6, 0.8, 0.9, 0.5]
        colors = cm.Blues(
            [color_values[i % len(color_values)]
             for i in range(len(sizes))]
        )

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=None,
            autopct="%1.0f%%",
            pctdistance=0.75,
            startangle=90,
            colors=colors,
            explode=[0.03] * len(sizes),
            wedgeprops=dict(
                width=0.4,
                edgecolor="white",
                linewidth=2
            )
        )

        for text in autotexts:
            text.set_color("white")
            text.set_fontsize(12)
            text.set_weight("bold")

        fp = milker_font.copy()
        fp.set_size(28)
        fp.set_weight("bold")

        ax.set_title(
            title,
            color="white",
            fontproperties=fp,
            pad=25
        )
        ax.set_aspect("equal")

    canvas = FigureCanvasTkAgg(fig, master=f)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)




# ===== DASHBOARD CHARTS AND PANELS =====
def refresh_dashboard_graphs():
    # Rebuild the chart area from current database values.
    for widget in bottom.winfo_children():
        widget.destroy()

    donut_chart(
        """SELECT CASE
                    WHEN LOWER(payment_status) IN ('completed', 'paid') THEN 'Completed'
                    WHEN LOWER(payment_status) = 'pending' THEN 'Pending'
                END AS payment_status, COUNT(*)
            FROM bills
            WHERE LOWER(payment_status) IN ('completed', 'paid', 'pending')
            GROUP BY CASE
                    WHEN LOWER(payment_status) IN ('completed', 'paid') THEN 'Completed'
                    WHEN LOWER(payment_status) = 'pending' THEN 'Pending'
                END
            ORDER BY payment_status""",
        "PAYMENTS", 0, 0
    )

    graph(
        """SELECT bill_date, SUM(total) FROM bills
           GROUP BY bill_date ORDER BY bill_date DESC LIMIT 5""",
        "REVENUE", 0, 1, "line", xlabel="Date", ylabel="Revenue"
    )

    graph(
        """SELECT visit_date, COUNT(*) FROM patients
           GROUP BY visit_date ORDER BY visit_date DESC LIMIT 5""",
        "PATIENTS", 0, 2, xlabel="Date", ylabel="Patients"
    )

    graph(
        "SELECT gender, COUNT(*) FROM patients GROUP BY gender",
        "GENDER", 1, 1, xlabel="Gender", ylabel="Count"
    )

    graph(
        """SELECT appointment_date, COUNT(*) FROM appointments
           GROUP BY appointment_date
           ORDER BY appointment_date DESC LIMIT 5""",
        "APPOINTMENTS", 1, 2, xlabel="Date", ylabel="Appointments"
    )

    # Recent patients panel
    rp = ctk.CTkFrame(bottom, fg_color=DARK_BG)
    rp.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
    ctk.CTkLabel(rp, text="RECENT PATIENTS", font=("Milker", 16)).pack()
    recent_patients = fetch(
        "SELECT name, phone FROM patients ORDER BY patient_id DESC LIMIT 5"
    )
    if recent_patients:
        for patient in recent_patients:
            ctk.CTkLabel(
                rp, text=f"{patient[0]} | {patient[1]}",
                font=("Milker", 13)
            ).pack(anchor="w")
    else:
        ctk.CTkLabel(rp, text="No patients yet", text_color="gray").pack(anchor="w")

    # Low-stock panel
    low = ctk.CTkFrame(bottom, fg_color=DARK_BG)
    low.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
    ctk.CTkLabel(
        low, text="LOW STOCK", font=("Milker", 16, "bold"),
        text_color="white"
    ).pack(pady=(10, 5))
    content = ctk.CTkFrame(low, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=15, pady=10)

    low_items = fetch("""SELECT item_name, quantity FROM inventory
                         WHERE quantity <= 5 ORDER BY quantity ASC""")
    if not low_items:
        ctk.CTkLabel(
            content, text="All items sufficiently stocked", text_color="gray"
        ).pack()
    else:
        for item_name, quantity in low_items:
            border_color = "#ff4d4d" if quantity < 5 else "#2a2a2a"
            item_frame = ctk.CTkFrame(
                content, fg_color="transparent", border_width=2,
                border_color=border_color, corner_radius=8
            )
            item_frame.pack(fill="x", pady=4)
            ctk.CTkLabel(
                item_frame, text=f"{item_name} | Qty: {quantity}",
                font=("Milker", 13), text_color="white"
            ).pack(anchor="w", padx=8, pady=4)


# Initial dashboard charts/panels
refresh_dashboard_graphs()


# ================= GENERIC CRUD =================

patient_id_combos = []

def get_patient_choices():
    """Return IDs for registered patients only, keeping linked records consistent."""
    return [str(row[0]) for row in fetch(
        "SELECT patient_id FROM patients ORDER BY patient_id DESC"
    )]

def refresh_patient_choices():
    choices = [""] + get_patient_choices()
    for combo in patient_id_combos:
        try:
            current = combo.get()
            combo.configure(values=choices)
            if current not in choices:
                combo.set("")
        except Exception:
            pass

def crud(frame, fields, add, update, delete, show_add=True, patient_id_selector=False):
    entries = {}

    form = ctk.CTkFrame(frame, fg_color=DARK_BG)
    form.pack(fill="x", pady=10)

    for field in fields:
        row = ctk.CTkFrame(form, fg_color=DARK_BG)
        row.pack(fill="x", pady=2)

        display_field = "Patient ID" if field.strip().upper() == "PID" else field
        ctk.CTkLabel(
            row, text=display_field, width=120, font=("Milker", 13)
        ).pack(side="left")

        if field.strip().lower() == "gender":
            # A compact two-option toggle instead of free-form gender text.
            entry = ctk.CTkSegmentedButton(
                row,
                values=["Male", "Female"],
                font=("Milker", 14),
                selected_color="#1f6aa5",
                selected_hover_color="#2f7db8",
                unselected_color="#343638",
                unselected_hover_color="#45484a",
                text_color="white",
                corner_radius=8,
                height=34
            )
            entry.pack(fill="x", expand=True)
            entry.set("Male")
        elif "phone" in field.strip().lower():
            # Same live validation as Patient Registration: digits only, max 10.
            phone_validation = (
                form.register(
                    lambda proposed: proposed == "" or (
                        proposed.isdigit() and len(proposed) <= 10
                    )
                ),
                "%P"
            )
            entry = ctk.CTkEntry(
                row,
                font=("Milker", 14),
                height=34,
                validate="key",
                validatecommand=phone_validation
            )
            entry.pack(fill="x", expand=True)
        elif field.strip().lower() == "status" and frame is frames.get("bills"):
            # Payment status is restricted to the two supported billing states.
            entry = ctk.CTkComboBox(
                row,
                values=["Completed", "Pending"],
                state="readonly",
                font=("Milker", 14),
                height=34
            )
            entry.pack(fill="x", expand=True)
            entry.set("Completed")
        elif field.strip().lower() == "pid" or (
            patient_id_selector and field.strip().lower() == "patient id"
        ):
            # Patient List, appointments, and bills use the same patients.patient_id values.
            entry = ctk.CTkComboBox(
                row,
                values=[""] + get_patient_choices(),
                state="readonly",
                font=("Milker", 14),
                height=34,
                command=lambda _value: sync_patient_name()
            )
            entry.pack(fill="x", expand=True)
            entry.set("")
            patient_id_combos.append(entry)
        else:
            entry = ctk.CTkEntry(row, font=("Milker", 14))
            entry.pack(fill="x", expand=True)

        entries[field] = entry

        # Phone fields accept digits only and are capped at 10 digits.
        if "phone" in field.lower():
            def enforce_phone(event, phone_entry=entry):
                current = phone_entry.get()
                digits_only = "".join(ch for ch in current if ch.isdigit())[:10]
                if current != digits_only:
                    cursor = phone_entry.index("insert")
                    phone_entry.delete(0, "end")
                    phone_entry.insert(0, digits_only)
                    phone_entry.icursor(min(cursor, len(digits_only)))

            entry.bind("<KeyRelease>", enforce_phone)

    def sync_patient_name(_value=None):
        pid_widget = entries.get("PID")
        name_widget = entries.get("Patient Name")
        if pid_widget is None or name_widget is None:
            return
        patient_id = pid_widget.get().strip()
        if not patient_id:
            name_widget.configure(state="normal")
            name_widget.delete(0, "end")
            name_widget.configure(state="disabled")
            return
        rows = fetch("SELECT name FROM patients WHERE patient_id = %s", (int(patient_id),))
        name_widget.configure(state="normal")
        name_widget.delete(0, "end")
        if rows:
            name_widget.insert(0, rows[0][0] or "")
        name_widget.configure(state="disabled")

    if "PID" in entries and "Patient Name" in entries:
        entries["Patient Name"].configure(state="disabled")
        entries["PID"].configure(command=sync_patient_name)

    button_frame = ctk.CTkFrame(form, fg_color=DARK_BG)
    button_frame.pack(pady=10)

    # Resolve the primary-key field regardless of its visible label
    # (for example, "Inventory ID", "Doctor ID", or simply "ID").
    def get_record_id_entry():
        if "ID" in entries:
            return entries["ID"]
        for field_name, field_entry in entries.items():
            if field_name.strip().lower().endswith(" id"):
                return field_entry
        return None

    # Each CRUD action can refresh the current page's data afterward.
    def run_action(action):
        from tkinter import messagebox
        try:
            is_delete = action is delete

            # Ask before permanently deleting a record.
            if is_delete and not messagebox.askyesno(
                "Confirm deletion",
                "Delete this record permanently? This action cannot be undone."
            ):
                return

            if is_delete:
                id_entry = get_record_id_entry()
                if id_entry is None or not id_entry.get().strip().isdigit() or int(id_entry.get()) < 1:
                    messagebox.showwarning("Invalid ID", "Enter a valid record ID before deleting.")
                    if id_entry:
                        id_entry.focus_set()
                    return
            else:
                # Required fields; ID is only needed for updates, and Bill Total is calculated by the database logic.
                optional_on_add = {"id", "total"}
                for field, entry in entries.items():
                    value = entry.get().strip()
                    field_key = field.strip().lower()
                    if field_key in optional_on_add:
                        continue
                    if not value:
                        messagebox.showwarning("Missing information", f"Please fill in: {field}.")
                        entry.focus_set()
                        return

                # Bill payment status must be one of the two allowed values.
                if frame is frames.get("bills") and "Status" in entries:
                    payment_status = entries["Status"].get().strip().title()
                    if payment_status not in {"Completed", "Pending"}:
                        messagebox.showwarning(
                            "Invalid payment status",
                            "Payment status must be Completed or Pending."
                        )
                        entries["Status"].focus_set()
                        return

                # Update operations require a valid record ID.
                if action is update:
                    id_entry = get_record_id_entry()
                    if id_entry is None or not id_entry.get().strip().isdigit() or int(id_entry.get()) < 1:
                        messagebox.showwarning("Invalid ID", "Enter a valid record ID before updating.")
                        if id_entry:
                            id_entry.focus_set()
                        return

                # Validate numeric fields before converting them to int/float.
                integer_fields = {"id", "pid", "age", "qty", "quantity"}
                decimal_fields = {"price", "consultation", "consult", "medicine", "total"}
                for field, entry in entries.items():
                    key = field.strip().lower()
                    value = entry.get().strip()
                    if key in integer_fields and value:
                        if not value.isdigit():
                            messagebox.showwarning("Invalid number", f"{field} must be a whole number.")
                            entry.focus_set()
                            return
                        if int(value) < 1 and key not in {"qty", "quantity"}:
                            messagebox.showwarning("Invalid number", f"{field} must be greater than zero.")
                            entry.focus_set()
                            return
                    elif key in decimal_fields and value:
                        try:
                            number = float(value)
                            if number < 0:
                                raise ValueError
                        except ValueError:
                            messagebox.showwarning("Invalid amount", f"{field} must be a valid non-negative amount.")
                            entry.focus_set()
                            return

                    if "phone" in key and not (len(value) == 10 and value.isdigit()):
                        messagebox.showwarning(
                            "Invalid phone number",
                            "Enter a valid 10-digit phone number using digits only."
                        )
                        entry.focus_set()
                        return

                    if "email" in key and ("@" not in value or "." not in value.split("@")[-1]):
                        messagebox.showwarning("Invalid email", "Enter a valid email address.")
                        entry.focus_set()
                        return

                    if "date" in key:
                        try:
                            datetime.strptime(value, "%d/%m/%Y")
                        except ValueError:
                            messagebox.showwarning("Invalid date", f"Enter {field} as DD/MM/YYYY.")
                            entry.focus_set()
                            return

                # Warn if the selected doctor already has an appointment at that date and time.
                if frame in (frames.get("appointments"), globals().get("appointments_list_tab")):
                    appt_date = format_input_date(entries["Date"].get())
                    appt_time = entries["Time"].get().strip()
                    doctor_name = entries["Doctor"].get().strip()
                    conflict_sql = (
                        "SELECT COUNT(*) FROM appointments "
                        "WHERE appointment_date = %s AND appointment_time = %s "
                        "AND LOWER(doctor_name) = LOWER(%s) "
                        "AND LOWER(COALESCE(status, '')) NOT IN ('cancelled', 'canceled')"
                    )
                    conflict_params = [appt_date, appt_time, doctor_name]
                    if action is update:
                        conflict_sql += " AND appointment_id <> %s"
                        conflict_params.append(int(entries["ID"].get()))
                    if fetch(conflict_sql, tuple(conflict_params))[0][0] > 0:
                        messagebox.showwarning(
                            "Appointment conflict",
                            "This doctor already has an appointment at that date and time. Choose another time."
                        )
                        entries["Time"].focus_set()
                        return

            result = action(entries)

            if result:
                refresh_callback = getattr(frame, "_refresh_list", None)

                if refresh_callback:
                    refresh_callback()

                if (frame is frames.get("patients") or frame is globals().get("patient_list_tab")) and "refresh_patient_choices" in globals():
                    refresh_patient_choices()

                if "refresh_dashboard" in globals():
                    refresh_dashboard()

                if "refresh_dashboard_graphs" in globals():
                    refresh_dashboard_graphs()

                if frame in (frames.get("appointments"), globals().get("appointments_list_tab")) and "render_appointment_calendar" in globals():
                    render_appointment_calendar()

                # Clear the form after a successful operation
                for field, entry in entries.items():
                    if field == "Patient Name":
                        entry.configure(state="normal")
                        entry.delete(0, "end")
                        entry.configure(state="disabled")
                    elif field == "PID":
                        entry.set("")
                    elif field.strip().lower() == "gender":
                        entry.set("Male")
                    elif field.strip().lower() == "status" and frame is frames.get("bills"):
                        entry.set("Completed")
                    else:
                        entry.delete(0, "end")

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                "Error",
                f"Operation failed:\n{e}"
            )



    if show_add:
        ctk.CTkButton(
            button_frame, text="Add",
            font=("Milker", 15),
            command=lambda: run_action(add)
        ).pack(side="left", padx=5)

    ctk.CTkButton(
        button_frame, text="Update",
        font=("Milker", 15),
        command=lambda: run_action(update)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        button_frame, text="Delete",
        font=("Milker", 15),
        command=lambda: run_action(delete)
    ).pack(side="left", padx=5)




def show_list(frame, q, fmt, search_var=None):
    """Legacy compact list renderer, retained for any non-table lists."""
    box = ctk.CTkFrame(frame, fg_color=DARK_BG)
    box.pack(fill="both", expand=True)

    def update_list(*args):
        for widget in box.winfo_children():
            widget.destroy()
        data = fetch(q)
        query_text = search_var.get().strip().casefold() if search_var else ""
        for record in data:
            text = fmt(record)
            if not query_text or query_text in text.casefold():
                ctk.CTkLabel(
                    box, text=text, text_color="white", anchor="w",
                    justify="left", wraplength=1050
                ).pack(fill="x", anchor="w", padx=10, pady=3)

    if search_var:
        search_var.trace_add("write", update_list)
    update_list()
    frame._refresh_list = update_list
    return update_list


def create_data_table(parent, columns, query, search_var, widths, date_columns=(), money_columns=(), order_by=None):
    """Create a dark, searchable Treeview table and attach its refresh callback to the parent."""
    table_frame = ctk.CTkFrame(parent, fg_color=DARK_BG)
    table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Eunoia.Treeview")
    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=widths.get(column, 130), minwidth=55, anchor="w",
                     stretch=column in {"Name", "Patient Name", "Address", "Symptoms", "Email", "Supplier"})

    vertical_scroll = ctk.CTkScrollbar(
        table_frame, orientation="vertical", command=table.yview,
        fg_color="#1e1e1e", button_color="#454545", button_hover_color="#606060"
    )
    horizontal_scroll = ctk.CTkScrollbar(
        table_frame, orientation="horizontal", command=table.xview,
        fg_color="#1e1e1e", button_color="#454545", button_hover_color="#606060"
    )
    table.configure(yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set)
    table.grid(row=0, column=0, sticky="nsew")
    vertical_scroll.grid(row=0, column=1, sticky="ns")
    horizontal_scroll.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    def display_value(index, value):
        if value is None:
            return ""
        if index in date_columns:
            return display_date(value)
        if index in money_columns:
            try:
                return f"₹{float(value):,.2f}"
            except (TypeError, ValueError):
                return str(value)
        return str(value)

    def refresh_table(*args):
        table.delete(*table.get_children())
        sql = query.strip().rstrip(";")
        if order_by and "order by" not in sql.casefold():
            sql += " ORDER BY " + order_by
        records = fetch(sql)
        needle = search_var.get().strip().casefold() if search_var else ""
        for record in records:
            values = tuple(display_value(i, value) for i, value in enumerate(record))
            if needle and needle not in " ".join(values).casefold():
                continue
            table.insert("", "end", values=values)

    if search_var:
        search_var.trace_add("write", refresh_table)
    refresh_table()
    parent._refresh_list = refresh_table
    return table



# ================= PATIENTS =================
crud(patient_list_tab,
     ["Patient ID","Name","Age","Gender","Phone","Address","Symptoms","Visit Date"],
     lambda e: add_patient(
    e["Name"].get(),
    int(e["Age"].get()),
    e["Gender"].get(),
    e["Phone"].get(),
    e["Address"].get(),
    e["Symptoms"].get(),
    format_input_date(e["Visit Date"].get())
),
lambda e: update_patient(
    int(e["Patient ID"].get()),
    e["Name"].get(),
    int(e["Age"].get()),
    e["Gender"].get(),
    e["Phone"].get(),
    e["Address"].get(),
    e["Symptoms"].get(),
    format_input_date(e["Visit Date"].get())
),
lambda e: delete_patient(int(e["Patient ID"].get())),
show_add=False,
patient_id_selector=True
)

search_var = tk.StringVar()

search_entry = ctk.CTkEntry(
    patient_list_tab,
    placeholder_text="Search patients...",
    textvariable=search_var,
    width=300
)
search_entry.pack(pady=10)


# ===== PATIENT RECORDS TABLE =====
# A real table is easier to scan than a long stack of labels.
patient_table_frame = ctk.CTkFrame(patient_list_tab, fg_color=DARK_BG)
patient_table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

patient_columns = (
    "Patient ID", "Name", "Age", "Gender", "Phone",
    "Address", "Symptoms", "Visit Date"
)

patient_table_style = ttk.Style()
patient_table_style.configure(
    "Patients.Treeview",
    background="#242424",
    foreground="white",
    fieldbackground="#242424",
    rowheight=30,
    borderwidth=0,
    font=("Arial", 10)
)
patient_table_style.configure(
    "Patients.Treeview.Heading",
    background="#1f6aa5",
    foreground="white",
    relief="flat",
    font=("Arial", 10, "bold")
)
patient_table_style.map(
    "Patients.Treeview",
    background=[("selected", "#35556b")],
    foreground=[("selected", "white")]
)
patient_table_style.map(
    "Patients.Treeview.Heading",
    background=[("active", "#2f7db8")]
)

patient_table = ttk.Treeview(
    patient_table_frame,
    columns=patient_columns,
    show="headings",
    style="Patients.Treeview"
)

patient_column_widths = {
    "Patient ID": 80, "Name": 150, "Age": 55, "Gender": 85,
    "Phone": 115, "Address": 200, "Symptoms": 220, "Visit Date": 100
}
for column in patient_columns:
    patient_table.heading(column, text=column)
    patient_table.column(
        column,
        width=patient_column_widths.get(column, 100),
        minwidth=45,
        anchor="w",
        stretch=(column in ("Name", "Address", "Symptoms"))
    )

patient_vertical_scroll = ctk.CTkScrollbar(
    patient_table_frame, orientation="vertical", command=patient_table.yview,
    fg_color="#1e1e1e", button_color="#454545", button_hover_color="#606060"
)
patient_horizontal_scroll = ctk.CTkScrollbar(
    patient_table_frame, orientation="horizontal", command=patient_table.xview,
    fg_color="#1e1e1e", button_color="#454545", button_hover_color="#606060"
)
patient_table.configure(
    yscrollcommand=patient_vertical_scroll.set,
    xscrollcommand=patient_horizontal_scroll.set
)

patient_table.grid(row=0, column=0, sticky="nsew")
patient_vertical_scroll.grid(row=0, column=1, sticky="ns")
patient_horizontal_scroll.grid(row=1, column=0, sticky="ew")
patient_table_frame.grid_rowconfigure(0, weight=1)
patient_table_frame.grid_columnconfigure(0, weight=1)

def refresh_patient_table(*args):
    patient_table.delete(*patient_table.get_children())
    search_text = search_var.get().strip().casefold()

    rows = fetch(
        """SELECT patient_id, name, age, gender, phone, address, symptoms, visit_date
           FROM patients
           ORDER BY patient_id DESC"""
    )

    for row in rows:
        # row[0] is patients.patient_id, the canonical ID used by appointment
        # and bill PID dropdowns (both query this same database column).
        display_values = (
            row[0], row[1] or "", row[2] if row[2] is not None else "",
            row[3] or "", row[4] or "", row[5] or "", row[6] or "",
            display_date(row[7])
        )
        if search_text and search_text not in " ".join(
            str(value) for value in display_values
        ).casefold():
            continue
        patient_table.insert("", "end", values=display_values)

search_var.trace_add("write", refresh_patient_table)
refresh_patient_table()
patient_list_tab._refresh_list = refresh_patient_table

# ================= PATIENT REGISTRATION SUBPAGE =================
# Register the patient once here before creating appointments or bills for them.
registration_page = patient_registration_tab
ctk.CTkLabel(
    registration_page,
    text="PATIENT REGISTRATION",
    font=("Milker", 24, "bold"),
    text_color="white"
).pack(pady=(28, 6))

registration_card = ctk.CTkFrame(
    registration_page, fg_color="#242424", corner_radius=14,
    border_width=1, border_color="#3a3a3a"
)
registration_card.pack(fill="x", padx=70, pady=10)
registration_card.grid_columnconfigure((0, 1), weight=1)

registration_entries = {}

# Patient ID is entered manually rather than generated by the registration form.
id_cell = ctk.CTkFrame(registration_card, fg_color="transparent")
id_cell.grid(row=0, column=0, sticky="ew", padx=16, pady=10)
ctk.CTkLabel(
    id_cell, text="Patient ID", font=("Arial", 12, "bold"),
    text_color="#d8d8d8"
).pack(anchor="w", pady=(0, 5))
registration_id_entry = ctk.CTkEntry(
    id_cell, placeholder_text="Enter patient ID",
    height=38, font=("Arial", 13)
)
registration_id_entry.pack(fill="x")
registration_entries["ID"] = registration_id_entry

registration_fields = [
    ("Name", "Full name"),
    ("Age", "Age in years"),
    ("Phone", "10-digit phone number"),
    ("Address", "Residential address"),
    ("Symptoms", "Reason for visit / symptoms"),
    ("Visit Date", "DD/MM/YYYY")
]

def validate_registration_phone(proposed_value):
    # Permit only digits, up to 10 characters, while the user is typing.
    return proposed_value == "" or (
        proposed_value.isdigit() and len(proposed_value) <= 10
    )

phone_validation = (registration_card.register(validate_registration_phone), "%P")

for index, (field, placeholder) in enumerate(registration_fields, start=1):
    r, c = divmod(index, 2)
    cell = ctk.CTkFrame(registration_card, fg_color="transparent")
    cell.grid(row=r, column=c, sticky="ew", padx=16, pady=10)
    ctk.CTkLabel(cell, text=field, font=("Arial", 12, "bold"), text_color="#d8d8d8").pack(anchor="w", pady=(0, 5))
    if field == "Phone":
        entry = ctk.CTkEntry(
            cell, placeholder_text=placeholder, height=38, font=("Arial", 13),
            validate="key", validatecommand=phone_validation
        )
    else:
        entry = ctk.CTkEntry(cell, placeholder_text=placeholder, height=38, font=("Arial", 13))
    entry.pack(fill="x")
    registration_entries[field] = entry

# Gender uses the same two-choice segmented control as the patient management form.
gender_cell = ctk.CTkFrame(registration_card, fg_color="transparent")
gender_cell.grid(row=3, column=1, sticky="ew", padx=16, pady=10)
ctk.CTkLabel(gender_cell, text="Gender", font=("Arial", 12, "bold"), text_color="#d8d8d8").pack(anchor="w", pady=(0, 5))
registration_gender = ctk.CTkSegmentedButton(
    gender_cell, values=["Male", "Female"], height=38,
    selected_color="#1f6aa5", selected_hover_color="#2f7db8",
    unselected_color="#343638", unselected_hover_color="#45484a",
    text_color="white", font=("Arial", 13)
)
registration_gender.pack(fill="x")
registration_gender.set("Male")
registration_entries["Gender"] = registration_gender
registration_entries["Visit Date"].insert(0, date.today().strftime("%d/%m/%Y"))

registration_status = ctk.CTkLabel(registration_page, text="", font=("Arial", 12), text_color="#78c99a")
registration_status.pack(pady=(4, 0))

def register_patient_from_form():
    from tkinter import messagebox
    values = {key: widget.get().strip() for key, widget in registration_entries.items()}
    required = ("ID", "Name", "Age", "Gender", "Phone", "Address", "Symptoms", "Visit Date")
    for field in required:
        if not values.get(field):
            messagebox.showwarning("Missing information", f"Please fill in: {field}.")
            if field in registration_entries:
                registration_entries[field].focus_set()
            return
    if not values["Age"].isdigit() or int(values["Age"]) < 1 or int(values["Age"]) > 120:
        messagebox.showwarning("Invalid age", "Enter an age between 1 and 120.")
        registration_entries["Age"].focus_set()
        return
    if len(values["Phone"]) != 10 or not values["Phone"].isdigit():
        messagebox.showwarning(
            "Invalid phone number",
            "Enter a valid 10-digit phone number using digits only."
        )
        registration_entries["Phone"].focus_set()
        return
    try:
        visit_date = format_input_date(values["Visit Date"])
        if not values["ID"].isdigit() or int(values["ID"]) < 1:
            messagebox.showwarning("Invalid Patient ID", "Enter a positive numeric Patient ID.")
            registration_id_entry.focus_set()
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO patients
                   (patient_id, name, age, gender, phone, address, symptoms, visit_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    int(values["ID"]), values["Name"], int(values["Age"]),
                    values["Gender"], values["Phone"], values["Address"],
                    values["Symptoms"], visit_date
                )
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()
        refresh_patient_table()
        refresh_patient_choices()
        refresh_dashboard()
        refresh_dashboard_graphs()
        registration_status.configure(
            text=f"Registered {values['Name']} with Patient ID {values['ID']}. Select this ID when creating appointments or bills."
        )
        for field, widget in registration_entries.items():
            if field == "Gender":
                widget.set("Male")
            else:
                widget.delete(0, "end")
        registration_entries["Visit Date"].insert(0, date.today().strftime("%d/%m/%Y"))
    except Exception as exc:
        messagebox.showerror("Registration failed", f"Could not register patient:\n{exc}")

ctk.CTkButton(
    registration_page, text="Register Patient", height=42, width=220,
    font=("Milker", 16), fg_color="#1f6aa5", hover_color="#2f7db8",
    command=register_patient_from_form
).pack(pady=16)

# ================= DOCTORS =================
crud(frames["doctors"],
     ["Doctor ID", "Name", "Speciality", "Phone", "Email", "Availability"],
     lambda e: add_doctor(e["Name"].get(), e["Speciality"].get(), e["Phone"].get(), e["Email"].get(), e["Availability"].get()),
     lambda e: update_doctor(int(e["Doctor ID"].get()), e["Name"].get(), e["Speciality"].get(), e["Phone"].get(), e["Email"].get(), e["Availability"].get()),
     lambda e:delete_doctor(int(e["Doctor ID"].get()))
)

doc_search = tk.StringVar()

ctk.CTkEntry(
    frames["doctors"],
    placeholder_text="Search doctors...",
    textvariable=doc_search,
    width=300
).pack(pady=10)

create_data_table(
    frames["doctors"],
    ("ID", "Name", "Specialty", "Phone", "Email", "Availability"),
    "SELECT doctor_id, doctor_name, specialization, phone, email, availability FROM doctors ORDER BY doctor_id DESC",
    doc_search,
    {"ID": 60, "Name": 180, "Specialty": 160, "Phone": 130, "Email": 240, "Availability": 180}
)

# ================= INVENTORY =================
crud(frames["inventory"],
     ["Inventory ID", "Name", "Category", "Quantity", "Price", "Supplier"],
     lambda e: add_item(e["Name"].get(), e["Category"].get(), int(e["Quantity"].get()), float(e["Price"].get()), e["Supplier"].get()),
     lambda e: update_item(int(e["Inventory ID"].get()), e["Name"].get(), e["Category"].get(), int(e["Quantity"].get()), float(e["Price"].get()), e["Supplier"].get()),
     lambda e:delete_item(int(e["Inventory ID"].get()))
)

inv_search = tk.StringVar()

ctk.CTkEntry(
    frames["inventory"],
    placeholder_text="Search inventory...",
    textvariable=inv_search,
    width=300
).pack(pady=10)

create_data_table(
    frames["inventory"],
    ("ID", "Name", "Category", "Quantity", "Price", "Supplier"),
    "SELECT item_id, item_name, category, quantity, price, supplier FROM inventory ORDER BY item_id DESC",
    inv_search,
    {"ID": 60, "Name": 200, "Category": 150, "Quantity": 100, "Price": 130, "Supplier": 220},
    money_columns=(4,)
)

# ================= APPOINTMENTS =================
# Separate the appointment list/form and calendar into their own inner tabs.
appt_tabs = ctk.CTkTabview(frames["appointments"], fg_color=DARK_BG)
appt_tabs.pack(fill="both", expand=True, padx=8, pady=8)
appt_tabs.add("Appointments List")
appt_tabs.add("Calendar")
appt_tabs.set("Appointments List")
appointments_list_tab = appt_tabs.tab("Appointments List")
appointments_calendar_tab = appt_tabs.tab("Calendar")

crud(appointments_list_tab,
     ["Appointment ID", "PID", "Patient Name", "Doctor", "Date", "Time", "Status"],
     lambda e: add_appointment(int(e["PID"].get()), e["Patient Name"].get(), e["Doctor"].get(),
                               format_input_date(e["Date"].get()), e["Time"].get(), e["Status"].get()),
     lambda e: update_appointment(int(e["Appointment ID"].get()), int(e["PID"].get()), e["Patient Name"].get(),
                                  e["Doctor"].get(), format_input_date(e["Date"].get()), e["Time"].get(), e["Status"].get()),
     lambda e: delete_appointment(int(e["Appointment ID"].get()))
)

appt_search = tk.StringVar()

# ===== APPOINTMENT CALENDAR =====
# Built with Python's standard calendar module; no extra package required.
calendar_state = {"year": date.today().year, "month": date.today().month}
calendar_panel = ctk.CTkFrame(appointments_calendar_tab, fg_color="#242424", corner_radius=10)
calendar_panel.pack(fill="both", expand=True, padx=12, pady=12)
calendar_header = ctk.CTkFrame(calendar_panel, fg_color="transparent")
calendar_header.pack(fill="x", padx=14, pady=(14, 8))
calendar_grid = ctk.CTkFrame(calendar_panel, fg_color="transparent")
calendar_grid.pack(fill="both", expand=True, padx=14, pady=(4, 14))


def change_calendar_month(delta):
    month = calendar_state["month"] + delta
    year = calendar_state["year"]
    if month < 1:
        month, year = 12, year - 1
    elif month > 12:
        month, year = 1, year + 1
    calendar_state.update(year=year, month=month)
    render_appointment_calendar()


def select_calendar_date(day):
    selected = date(calendar_state["year"], calendar_state["month"], day)
    appt_search.set(selected.strftime("%d/%m/%Y"))
    appt_tabs.set("Appointments List")


def render_appointment_calendar():
    for widget in calendar_header.winfo_children():
        widget.destroy()
    for widget in calendar_grid.winfo_children():
        widget.destroy()

    year, month = calendar_state["year"], calendar_state["month"]
    ctk.CTkButton(
        calendar_header, text="‹", width=36, height=28,
        command=lambda: change_calendar_month(-1)
    ).pack(side="left")
    ctk.CTkLabel(
        calendar_header, text=f"APPOINTMENT CALENDAR  •  {pycalendar.month_name[month]} {year}",
        font=("Arial", 15, "bold")
    ).pack(side="left", expand=True, padx=8)
    ctk.CTkButton(
        calendar_header, text="›", width=36, height=28,
        command=lambda: change_calendar_month(1)
    ).pack(side="right")
    ctk.CTkButton(
        calendar_header, text="Clear filter", width=90, height=28,
        command=lambda: appt_search.set("")
    ).pack(side="right", padx=(6, 0))

    counts = {}
    month_start = f"{year:04d}-{month:02d}-01"
    next_month = f"{year + 1:04d}-01-01" if month == 12 else f"{year:04d}-{month + 1:02d}-01"
    rows = fetch(
        "SELECT appointment_date, COUNT(*) FROM appointments "
        "WHERE appointment_date >= %s AND appointment_date < %s "
        "GROUP BY appointment_date",
        (month_start, next_month)
    )
    for appointment_date, count in rows:
        counts[str(appointment_date)[:10]] = count

    # Let the seven columns and up to six week rows expand to use the full tab.
    for col in range(7):
        calendar_grid.grid_columnconfigure(col, weight=1, uniform="calendar_columns")
    for row in range(7):
        calendar_grid.grid_rowconfigure(row, weight=1, uniform="calendar_rows")

    for col, weekday in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
        ctk.CTkLabel(
            calendar_grid, text=weekday, font=("Arial", 15, "bold")
        ).grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

    today = date.today()
    for row_index, week in enumerate(pycalendar.monthcalendar(year, month), start=1):
        for col_index, day in enumerate(week):
            if day == 0:
                ctk.CTkLabel(calendar_grid, text="").grid(
                    row=row_index, column=col_index, padx=5, pady=5, sticky="nsew"
                )
                continue
            date_key = f"{year:04d}-{month:02d}-{day:02d}"
            count = counts.get(date_key, 0)
            label = f"{day}" + (f"  • {count}" if count else "")
            is_today = (year, month, day) == (today.year, today.month, today.day)
            ctk.CTkButton(
                calendar_grid, text=label, height=58,
                font=("Arial", 16, "bold"),
                fg_color="#287a57" if is_today else ("#1f6aa5" if count else "#343434"),
                hover_color="#3b8c6a" if is_today else "#46515c",
                command=lambda selected_day=day: select_calendar_date(selected_day)
            ).grid(row=row_index, column=col_index, padx=5, pady=5, sticky="nsew")


render_appointment_calendar()

ctk.CTkEntry(
    appointments_list_tab,
    placeholder_text="Search appointments or select a date from the Calendar tab...",
    textvariable=appt_search,
    width=300
).pack(pady=6)

create_data_table(
    appointments_list_tab,
    ("ID", "Patient ID", "Patient Name", "Doctor", "Date", "Time", "Status"),
    "SELECT appointment_id, patient_id, patient_name, doctor_name, appointment_date, appointment_time, status FROM appointments",
    appt_search, 
    {"ID": 60, "Patient ID": 95, "Patient Name": 190, "Doctor": 190, "Date": 120, "Time": 110, "Status": 140},
    date_columns=(4,),
    order_by="appointment_date ASC, appointment_time ASC"
)

# ================= BILLS =================
crud(frames["bills"],
     ["Bill ID", "PID", "Consultation", "Medicine", "Total", "Status", "Bill Date"],

     
    lambda e: add_bill(
    int(e["PID"].get()),
    float(e["Consultation"].get()),
    float(e["Medicine"].get()),
    e["Status"].get(),
    format_input_date(e["Bill Date"].get())
),
    
    lambda e: update_bill(
    int(e["Bill ID"].get()),
    float(e["Consultation"].get()),
    float(e["Medicine"].get()),
    e["Status"].get(),
    format_input_date(e["Bill Date"].get())
),

     lambda e:delete_bill(int(e["Bill ID"].get()))
)

bill_search = tk.StringVar()

ctk.CTkEntry(
    frames["bills"],
    placeholder_text="Search bills...",
    textvariable=bill_search,
    width=300
).pack(pady=10)

create_data_table(
    frames["bills"],
    ("Bill ID", "Patient ID", "Consultation Fee", "Medicine Cost", "Total", "Payment Status", "Bill Date"),
    "SELECT bill_id, patient_id, consultation_fee, medicine_cost, total, payment_status, bill_date FROM bills",
    bill_search,
    {"Bill ID": 75, "Patient ID": 95, "Consultation Fee": 150, "Medicine Cost": 145, "Total": 130, "Payment Status": 150, "Bill Date": 120},
    date_columns=(6,),
    money_columns=(2, 3, 4),
    order_by="bill_id DESC"
)

def generate_bill_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
        Image as RLImage
    )
    from reportlab.lib import colors
    from tkinter import messagebox
    import os

    bill_id = bill_id_entry.get().strip()
    if not bill_id.isdigit() or int(bill_id) < 1:
        messagebox.showerror("Invalid Bill ID", "Enter a valid positive Bill ID to generate the PDF.")
        bill_id_entry.focus_set()
        return

    result = fetch(
        """SELECT b.bill_id, b.patient_id, b.consultation_fee, b.medicine_cost,
                  b.total, b.payment_status, b.bill_date, p.name, p.phone
           FROM bills b
           LEFT JOIN patients p ON p.patient_id = b.patient_id
           WHERE b.bill_id = %s""",
        (int(bill_id),)
    )
    if not result:
        messagebox.showerror("Not Found", "Bill not found.")
        return

    bill = result[0]
    os.makedirs("bills_pdf", exist_ok=True)
    filename = os.path.abspath(os.path.join("bills_pdf", f"Bill_{bill[0]}.pdf"))

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=48, leftMargin=48,
        topMargin=42, bottomMargin=48
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="EunoiaTitle", parent=styles["Title"],
        fontName="Helvetica-Bold", fontSize=21, leading=26,
        textColor=colors.HexColor("#1F6AA5"), alignment=TA_CENTER,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name="SmallMuted", parent=styles["Normal"],
        fontSize=9, textColor=colors.HexColor("#555555"), leading=13
    ))
    styles.add(ParagraphStyle(
        name="RightAlign", parent=styles["Normal"], alignment=TA_RIGHT
    ))

    story = [
        Paragraph("EUNOIA HEALTH MANAGEMENT SYSTEM", styles["EunoiaTitle"]),
        Paragraph("PATIENT BILL / INVOICE", ParagraphStyle(
            "InvoiceSubtitle", parent=styles["Normal"], alignment=TA_CENTER,
            fontSize=11, textColor=colors.HexColor("#555555"), spaceAfter=18
        )),
        HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1F6AA5")),
        Spacer(1, 16)
    ]

    from xml.sax.saxutils import escape
    patient_name = escape(str(bill[7] or "Not available"))
    patient_phone = escape(str(bill[8] or "Not available"))
    details = [
        [Paragraph("<b>Bill number</b>", styles["Normal"]), str(bill[0]),
         Paragraph("<b>Bill date</b>", styles["Normal"]), display_date(bill[6])],
        [Paragraph("<b>Patient</b>", styles["Normal"]), patient_name,
         Paragraph("<b>Patient ID</b>", styles["Normal"]), str(bill[1])],
        [Paragraph("<b>Phone</b>", styles["Normal"]), patient_phone,
         Paragraph("<b>Payment status</b>", styles["Normal"]), str(bill[5] or "Pending").title()]
    ]
    details_table = Table(details, colWidths=[88, 155, 105, 105])
    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F7FA")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DEE7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.extend([details_table, Spacer(1, 24)])

    money_rows = [
        ["Description", "Amount (INR)"],
        ["Consultation fee", f"INR {float(bill[2] or 0):,.2f}"],
        ["Medicine cost", f"INR {float(bill[3] or 0):,.2f}"],
        [Paragraph("<b>TOTAL</b>", styles["Normal"]),
         Paragraph(f"<b>INR {float(bill[4] or 0):,.2f}</b>", styles["RightAlign"])],
    ]
    money_table = Table(money_rows, colWidths=[330, 123], hAlign="LEFT")
    money_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F6AA5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#EAF1F6")),
        ("LINEABOVE", (0, -1), (-1, -1), 1.2, colors.HexColor("#1F6AA5")),
        ("GRID", (0, 0), (-1, -2), 0.4, colors.HexColor("#D5DEE7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.extend([
        money_table,
        Spacer(1, 30),
        Paragraph("Thank you for visiting Eunoia.", ParagraphStyle(
            "Thanks", parent=styles["Normal"], alignment=TA_CENTER,
            fontSize=12, textColor=colors.HexColor("#1F6AA5"), spaceAfter=8
        )),
        Spacer(1, 16)
    ])

    # Place the Eunoia logo in the open space at the bottom of the invoice.
    try:
        logo_path = r"C:\Users\HK\Desktop\The Eunoia Project\logo.png"
        if os.path.isfile(logo_path):
            logo = RLImage(logo_path, width=132, height=88, kind="proportional")
            logo.hAlign = "CENTER"
            story.append(logo)
    except Exception:
        pass

    try:
        doc.build(story)
    except Exception as exc:
        messagebox.showerror("PDF Error", f"Could not generate the invoice:\n{exc}")
        return

    messagebox.showinfo("PDF Generated", f"Invoice saved at:\n{filename}")


bill_id_entry = ctk.CTkEntry(
    frames["bills"],
    placeholder_text="Enter Bill ID",
    width=200
)
bill_id_entry.pack(pady=8)

ctk.CTkButton(
    frames["bills"],
    text="Generate Bill PDF",
    command=generate_bill_pdf
).pack(pady=8)


# Refresh all patient-ID selectors once the UI is assembled.
refresh_patient_choices()

# ===== START =====
show_frame("dashboard")
app.mainloop()
