from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_bill_pdf(bill_id, patient_id, consultation_fee, medicine_cost, total, payment_status, bill_date):
    file_name = f"bill_{bill_id}.pdf"

    c = canvas.Canvas(file_name, pagesizes=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200,800, "Clinic Bill Receipt")

    c.setFont("Helvetica", 12)
    c.drawString(80, 750, f"Bill ID : {bill_id}")
    c.drawString(80, 720, f"Patient ID : {patient_id}")
    c.drawString(80, 690, f"Consultation Fee : {consultation_fee}")
    c.drawString(80, 660, f"Medicine Cost : {medicine_cost}")
    c.drawString(80, 630, f"Total : {total}")
    c.drawString(80, 600, f"payment Status : {payment_status}")
    c.drawString(80, 570, f"Bill Date : {bill_date}")

    c.save()

    return file_name
