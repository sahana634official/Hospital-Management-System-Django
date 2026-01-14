import requests

LAMBDA_URL = "http://localhost:3000/dev/send-email"


# ✅ Welcome mail (Signup)
def send_welcome_email(to_email, username):
    payload = {
        "action": "SIGNUP_WELCOME",
        "to_email": to_email,
        "username": username
    }

    try:
        res = requests.post(LAMBDA_URL, json=payload, timeout=10)
        print("✅ Welcome Mail Sent:", res.text)
    except Exception as e:
        print("❌ Welcome Email Error:", e)


# ✅ Booking confirmation mail (Patient)
def send_booking_email_patient(patient_user, doctor_user, slot):
    payload = {
        "action": "BOOKING_CONFIRMATION",
        "receiver": "patient",   # ✅ IMPORTANT ✅
        "to_email": patient_user.email,
        "username": patient_user.username,
        "doctor_name": doctor_user.username,
        "slot_time": f"{slot.date} {slot.start_time} - {slot.end_time}",

        # ✅ For calendar card in Gmail (.ics invite)
        "start_dt": f"{slot.date}T{slot.start_time}",
        "end_dt": f"{slot.date}T{slot.end_time}",
    }

    try:
        res = requests.post(LAMBDA_URL, json=payload, timeout=10)
        print("✅ Patient Booking Mail Sent:", res.text)
    except Exception as e:
        print("❌ Booking Email Error:", e)


# ✅ Booking confirmation mail (Doctor)
def send_booking_email_doctor(patient_user, doctor_user, slot):
    payload = {
        "action": "BOOKING_CONFIRMATION",
        "receiver": "doctor",   # ✅ IMPORTANT ✅
        "to_email": doctor_user.email,
        "username": patient_user.username,   # ✅ patient's name (doctor should see patient)
        "doctor_name": doctor_user.username,
        "slot_time": f"{slot.date} {slot.start_time} - {slot.end_time}",

        # ✅ For calendar card in Gmail (.ics invite)
        "start_dt": f"{slot.date}T{slot.start_time}",
        "end_dt": f"{slot.date}T{slot.end_time}",
    }

    try:
        res = requests.post(LAMBDA_URL, json=payload, timeout=10)
        print("✅ Doctor Booking Mail Sent:", res.text)
    except Exception as e:
        print("❌ Doctor Booking Email Error:", e)
