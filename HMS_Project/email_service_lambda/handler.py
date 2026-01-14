import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_EMAIL = "YOUR_REAL_MAIL"
SMTP_APP_PASSWORD = "YOUR_APP_PASSWORD"


def build_ics_event(summary, description, start_dt, end_dt):
    """
    start_dt & end_dt format: "2026-01-16T10:00:00"
    We will set timezone to Asia/Kolkata so Gmail shows correct time.
    """

    start_dt = start_dt.replace("-", "").replace(":", "")
    end_dt = end_dt.replace("-", "").replace(":", "")

    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Mini HMS//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VTIMEZONE
TZID:Asia/Kolkata
BEGIN:STANDARD
DTSTART:19700101T000000
TZOFFSETFROM:+0530
TZOFFSETTO:+0530
TZNAME:IST
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
SUMMARY:{summary}
DESCRIPTION:{description}
DTSTART;TZID=Asia/Kolkata:{start_dt}
DTEND;TZID=Asia/Kolkata:{end_dt}
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR
"""
    return ics


def send_email(event, context):
    try:
        body = json.loads(event["body"])

        action = body.get("action")
        to_email = body.get("to_email")
        username = body.get("username", "User")

        doctor_name = body.get("doctor_name", "")
        slot_time = body.get("slot_time", "")

        # ✅ new calendar fields
        start_dt = body.get("start_dt", "")
        end_dt = body.get("end_dt", "")

        # ✅ NEW: who is receiving
        receiver = body.get("receiver", "patient")  # patient / doctor

        if not to_email or not action:
            return {"statusCode": 400, "body": json.dumps({"error": "action and to_email are required"})}

        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email

        # ✅ WELCOME MAIL
        if action == "SIGNUP_WELCOME":
            msg["Subject"] = "Welcome to Mini HMS ✅"
            message = f"""Hello {username},

Welcome to Mini Hospital Management System ✅

Regards,
Mini HMS Team"""
            msg.attach(MIMEText(message, "plain"))

        # ✅ BOOKING CONFIRMATION + ICS
        elif action == "BOOKING_CONFIRMATION":
            msg["Subject"] = "Appointment Confirmed ✅"

            message = f"""Hello {username},

Your appointment is confirmed ✅
Doctor: {doctor_name}
Slot: {slot_time}

✅ Calendar invite is attached.

Regards,
Mini HMS Team"""
            msg.attach(MIMEText(message, "plain"))

            if start_dt and end_dt:

                # ✅ Patient calendar title
                if receiver == "patient":
                    summary = f"Appointment with Dr. {doctor_name}"
                    description = f"Doctor: {doctor_name}"

                # ✅ Doctor calendar title
                else:
                    summary = f"Appointment with Patient {username}"
                    description = f"Patient: {username}"

                ics_content = build_ics_event(summary, description, start_dt, end_dt)

                ics_part = MIMEText(ics_content, "calendar;method=REQUEST")
                ics_part.add_header("Content-Disposition", "attachment; filename=appointment.ics")
                msg.attach(ics_part)

        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid action"})}

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_EMAIL, [to_email], msg.as_string())

        return {"statusCode": 200, "body": json.dumps({"success": True, "message": "Email sent ✅"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"success": False, "error": str(e)})}
