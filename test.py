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
from tkinter import font

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
user_entry.pack(pady=10)

pass_entry = ctk.CTkEntry(login_box, placeholder_text="Password", show="*")
pass_entry.pack(pady=10)

error_label = ctk.CTkLabel(login_box, text="", text_color="red")
error_label.pack(pady=5)

def login():
    username = user_entry.get().strip()
    password = pass_entry.get().strip()

    if username == "Eunoia" and password == "---":
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
pages = ["dashboard","patients","appointments","inventory","doctors","bills"]
frames = {}

for name in pages:
    f = ctk.CTkFrame(content, fg_color=DARK_BG)
    f.place(relx=0, rely=0, relwidth=1, relheight=1)
    frames[name] = f

def show_frame(name):
    frames[name].tkraise()

# ===== SIDEBAR BUTTONS =====
sidebar.grid_columnconfigure(0, weight=1)

for i in range(len(pages)):
    sidebar.grid_rowconfigure(i, weight=3)

for i, name in enumerate(pages, start=1):
    btn = ctk.CTkButton(
        sidebar,
        text=name.capitalize(),
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
        corner_radius=12,
        fg_color="#1f6aa5"   # 👈 BLUE BACKGROUND
    )
    c.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")

    ctk.CTkLabel(c,text=title,text_color="white",font=("Milker", 15)).pack(pady=(10, 2))
    ctk.CTkLabel(c,text=value,font=("Milker", 22, "bold"),text_color="white").pack(pady=(0, 10))

rev = fetch("SELECT IFNULL(SUM(total),0) FROM bills")[0][0]
pat = fetch("SELECT COUNT(*) FROM patients")[0][0]
pending = fetch("SELECT IFNULL(SUM(total),0) FROM bills WHERE LOWER(payment_status)='pending'")[0][0]
appt = fetch("SELECT COUNT(*) FROM appointments")[0][0]

card(cards,"Revenue",f"₹{rev}",0)
card(cards,"Patients",pat,1)
card(cards,"Pending",f"₹{pending}",2)
card(cards,"Appointments",appt,3)


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




# ===== LAYOUT =====

# LEFT (DONUT COLUMN)
donut_chart(
    "SELECT payment_status,COUNT(*) FROM bills GROUP BY payment_status",
    "PAYMENTS",
    0, 0
)

# RIGHT SIDE

graph(
         """
         SELECT bill_date, SUM(total)
         FROM bills
         GROUP BY bill_date
         ORDER BY bill_date DESC
         LIMIT 5
         """,
         "REVENUE",
         0, 1,
         "line",
         xlabel="Date",
         ylabel="Revenue"
)

graph(
         """
        SELECT visit_date, COUNT(*)
        FROM patients
        GROUP BY visit_date
        ORDER BY visit_date DESC
        LIMIT 5
        """,
         "PATIENTS",
         0, 2,
         xlabel="Date",
         ylabel="Patients"
)

graph(
    "SELECT gender,COUNT(*) FROM patients GROUP BY gender",
    "GENDER",
    1, 1,
    xlabel="Gender",
    ylabel="Count"
)

graph(
         """
         SELECT appointment_date, COUNT(*)
         FROM appointments
         GROUP BY appointment_date
         ORDER BY appointment_date DESC
         LIMIT 5
         """,
         "APPOINTMENTS",
         1, 2,
         xlabel="Date",
         ylabel="Appointments"
)

# RECENT PATIENTS
rp = ctk.CTkFrame(bottom, fg_color=DARK_BG)
rp.grid(row=2, column=1,  padx=10, pady=10, sticky="nsew")

ctk.CTkLabel(rp, text="RECENT PATIENTS", font=("Milker", 16)).pack()

for r in fetch("SELECT name,phone FROM patients ORDER BY patient_id DESC LIMIT 5"):
    ctk.CTkLabel(rp, text=f"{r[0]} | {r[1]}", font=("Milker", 13)).pack(anchor="w")


# ===== LOW STOCK ALERT =====
low = ctk.CTkFrame(bottom, fg_color=DARK_BG)
low.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

ctk.CTkLabel(
    low,
    text="LOW STOCK",
    font=("Milker", 16, "bold"),
    text_color="white"
).pack(pady=(10,5))

# inner container
content = ctk.CTkFrame(low, fg_color="transparent")
content.pack(fill="both", expand=True, padx=15, pady=10)

# 🔥 query for low stock items
low_items = fetch("""
    SELECT item_name, quantity 
    FROM inventory 
    WHERE quantity <= 5
    ORDER BY quantity ASC
""")

if not low_items:
    ctk.CTkLabel(
        content,
        text="All items sufficiently stocked",
        text_color="gray"
    ).pack()
else:
    for item in low_items:
        qty = item[1]

        border_color = "#ff4d4d" if qty < 5 else "#2a2a2a"  # red only for critical

        item_frame = ctk.CTkFrame(
            content,
            fg_color="transparent",
            border_width=2,
            border_color=border_color,
            corner_radius=8
            )
        item_frame.pack(fill="x", pady=4)

        ctk.CTkLabel(
            item_frame,
            text=f"{item[0]}  |  Qty: {qty}",
            font=("Milker", 13),
            text_color="white"
        ).pack(anchor="w", padx=8, pady=4)


 # ================= GENERIC CRUD =================
def crud(frame,fields,add,update,delete):
    entries={}
    form = ctk.CTkFrame(frame, fg_color=DARK_BG)
    form.pack(fill="x",pady=10)

    for f in fields:
        r = ctk.CTkFrame(form, fg_color=DARK_BG)
        r.pack(fill="x",pady=2)
        ctk.CTkLabel(r, text=f, width=120, font=("Milker", 13)).pack(side="left")
        e = ctk.CTkEntry(r, font=("Milker", 14))
        e.pack(fill="x",expand=True)
        entries[f]=e

    btn = ctk.CTkFrame(form, fg_color=DARK_BG)
    btn.pack(pady=10)

    ctk.CTkButton(btn,text="Add", font=("Milker", 15), command=lambda:add(entries)).pack(side="left",padx=5)
    ctk.CTkButton(btn,text="Update", font=("Milker", 15) , command=lambda:update(entries)).pack(side="left",padx=5)
    ctk.CTkButton(btn,text="Delete", font=("Milker", 15), command=lambda:delete(entries)).pack(side="left",padx=5)


def show_list(frame, q, fmt, search_var=None):
    box = ctk.CTkFrame(frame, fg_color=DARK_BG)
    box.pack(fill="both", expand=True)

    def update_list(*args):
        for widget in box.winfo_children():
            widget.destroy()

        data = fetch(q)

        query = search_var.get().lower() if search_var else ""

        for d in data:
            text = fmt(d)

            if query in text.lower():
                ctk.CTkLabel(box, text=text).pack(anchor="w")

    if search_var:
        search_var.trace_add("write", update_list)

    update_list()

# ================= PATIENTS =================
crud(frames["patients"],
     ["ID","Name","Age","Gender","Phone","Address","Symptoms","Visit Date"],
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
    int(e["ID"].get()),
    e["Name"].get(),
    int(e["Age"].get()),
    e["Gender"].get(),
    e["Phone"].get(),
    e["Address"].get(),
    e["Symptoms"].get(),
    format_input_date(e["Visit Date"].get())
),
lambda e: delete_patient(int(e["ID"].get()))
)

search_var = tk.StringVar()

search_entry = ctk.CTkEntry(
    frames["patients"],
    placeholder_text="Search patients...",
    textvariable=search_var,
    width=300
)
search_entry.pack(pady=10)


show_list(
    frames["patients"],
    """SELECT patient_id, name, age, gender, phone, address, symptoms, visit_date
       FROM patients""",
    lambda d: (
        f"ID: {d[0]} | Name: {d[1]} | Age: {d[2]} | "
        f"Gender: {d[3]} | Phone: {d[4]} | Address: {d[5]} | "
        f"Symptoms: {d[6]} | Visit Date: {display_date(d[7])}"
    ),
    search_var
)

# ================= DOCTORS =================
crud(frames["doctors"],
     ["ID", "Name", "Spec", "Phone", "Email", "Avail"],
     lambda e: add_doctor(e["Name"].get(), e["Spec"].get(), e["Phone"].get(), e["Email"].get(), e["Avail"].get()),
     lambda e: update_doctor(int(e["ID"].get()), e["Name"].get(), e["Spec"].get(), e["Phone"].get(), e["Email"].get(), e["Avail"].get()),
     lambda e:delete_doctor(int(e["ID"].get()))
)

doc_search = tk.StringVar()

ctk.CTkEntry(
    frames["doctors"],
    placeholder_text="Search doctors...",
    textvariable=doc_search,
    width=300
).pack(pady=10)

show_list(
    frames["doctors"],
    """SELECT doctor_id, doctor_name, specialization, phone, email, availability
       FROM doctors""",
    lambda d: (
        f"ID: {d[0]} | Name: {d[1]} | Specialty: {d[2]} | "
        f"Phone: {d[3]} | Email: {d[4]} | Availability: {d[5]}"
    ),
    doc_search
)

# ================= INVENTORY =================
crud(frames["inventory"],
     ["ID", "Name", "Cat", "Qty", "Price", "Supp"],
     lambda e: add_item(e["Name"].get(), e["Cat"].get(), int(e["Qty"].get()), float(e["Price"].get()), e["Supp"].get()),
     lambda e: update_item(int(e["ID"].get()), e["Name"].get(), e["Cat"].get(), int(e["Qty"].get()), float(e["Price"].get()), e["Supp"].get()),
     lambda e:delete_item(int(e["ID"].get()))
)

inv_search = tk.StringVar()

ctk.CTkEntry(
    frames["inventory"],
    placeholder_text="Search inventory...",
    textvariable=inv_search,
    width=300
).pack(pady=10)

show_list(
    frames["inventory"],
    """SELECT item_id, item_name, category, quantity, price, supplier
       FROM inventory""",
    lambda d: (
        f"ID: {d[0]} | Name: {d[1]} | Category: {d[2]} | "
        f"Quantity: {d[3]} | Price: ₹{d[4]} | Supplier: {d[5]}"
    ),
    inv_search
)

# ================= APPOINTMENTS =================
crud(frames["appointments"],
     ["ID","PID","Patient Name","Doctor","Date","Time","Status"],
     lambda e:add_appointment(int(e["PID"].get()),e["Patient Name"].get(),e["Doctor"].get(),
                              format_input_date(e["Date"].get()),e["Time"].get(),e["Status"].get()),
     lambda e:update_appointment(int(e["ID"].get()),int(e["PID"].get()),e["Patient Name"].get(),
                                 e["Doctor"].get(),format_input_date(e["Date"].get()),e["Time"].get(),e["Status"].get()),
     lambda e:delete_appointment(int(e["ID"].get()))
)

appt_search = tk.StringVar()

ctk.CTkEntry(
    frames["appointments"],
    placeholder_text="Search appointments...",
    textvariable=appt_search,
    width=300
).pack(pady=10)

show_list(
    frames["appointments"],
    """SELECT appointment_id, patient_id, patient_name, doctor_name,
              appointment_date, appointment_time, status
       FROM appointments""",
    lambda d: (
        f"ID: {d[0]} | Patient ID: {d[1]} | Patient: {d[2]} | "
        f"Doctor: {d[3]} | Date: {display_date(d[4])} | Time: {d[5]} | "
        f"Status: {d[6]}"
    ),
    appt_search
)

# ================= BILLS =================
crud(frames["bills"],
     ["ID", "PID", "Consult", "Medicine", "Total", "Status", "Bill Date"],

     
    lambda e: add_bill(
    int(e["PID"].get()),
    float(e["Consult"].get()),
    float(e["Medicine"].get()),
    e["Status"].get(),
    format_input_date(e["Bill Date"].get())
),
    
    lambda e: update_bill(
    int(e["ID"].get()),
    float(e["Consult"].get()),
    float(e["Medicine"].get()),
    e["Status"].get(),
    format_input_date(e["Bill Date"].get())
),

     lambda e:delete_bill(int(e["ID"].get()))
)

bill_search = tk.StringVar()

ctk.CTkEntry(
    frames["bills"],
    placeholder_text="Search bills...",
    textvariable=bill_search,
    width=300
).pack(pady=10)

show_list(
    frames["bills"],
    """SELECT bill_id, patient_id, consultation_fee, medicine_cost,
              total, payment_status, bill_date
       FROM bills""",
    lambda d: (
        f"Bill ID: {d[0]} | Patient ID: {d[1]} | "
        f"Consultation: ₹{d[2]} | Medicine: ₹{d[3]} | "
        f"Total: ₹{d[4]} | Status: {d[5]} | Date: {display_date(d[6])}"
    ),
    bill_search
)

def generate_bill_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from tkinter import messagebox
    from datetime import datetime
    import os

    bill_id = bill_id_entry.get().strip()

    if not bill_id.isdigit():
        messagebox.showerror(
            "Invalid Bill ID",
            "Enter a valid Bill ID to generate the PDF."
        )
        return

    result = fetch(
        """SELECT bill_id, patient_id, consultation_fee,
                  medicine_cost, total, payment_status, bill_date
           FROM bills
           WHERE bill_id = %s""",
        (int(bill_id),)
    )

    if not result:
        messagebox.showerror("Not Found", "Bill not found.")
        return

    bill = result[0]
    os.makedirs("bills_pdf", exist_ok=True)

    filename = os.path.abspath(
        os.path.join("bills_pdf", f"Bill_{bill[0]}.pdf")
    )

    pdf = canvas.Canvas(filename, pagesize=A4)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 800, "Eunoia Health Management System")

    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 755, f"Bill #{bill[0]}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, f"Patient ID: {bill[1]}")
    pdf.drawString(50, 695, f"Bill Date: {display_date(bill[6])}")
    pdf.drawString(50, 670, f"Payment Status: {bill[5]}")

    pdf.line(50, 645, 545, 645)

    pdf.drawString(50, 615, f"Consultation Fee: Rs. {bill[2]}")
    pdf.drawString(50, 585, f"Medicine Cost: Rs. {bill[3]}")

    pdf.line(50, 560, 545, 560)

    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 530, f"TOTAL: Rs. {bill[4]}")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 80, "Thank you for visiting Eunoia.")

    pdf.save()

    messagebox.showinfo(
        "PDF Generated",
        f"Bill PDF saved at:\n{filename}"
    )


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


# ===== START =====
show_frame("dashboard")
app.mainloop()
