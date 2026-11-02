"""Smart Hospital Management System
Demonstrates: abstract classes, encapsulation, inheritance, polymorphism,
lists, loops, functions and exception handling.
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. Abstract class
# ---------------------------------------------------------------------------
class HospitalService(ABC):
    """Every hospital service user must be able to process a payment."""

    @abstractmethod
    def process_payment(self, amount):
        pass


# ---------------------------------------------------------------------------
# 2. Patient
# ---------------------------------------------------------------------------
class Patient(HospitalService):
    def __init__(self, name, patient_id, phone, age, balance):
        self.name = name
        self.patient_id = patient_id
        self.phone = phone
        self.age = age
        self.__balance = balance  # private

    def display_details(self):
        print(f"  ID: {self.patient_id} | Name: {self.name} | Phone: {self.phone} "
              f"| Age: {self.age} | Balance: Ksh {self.__balance:,.2f}")

    def check_balance(self):
        return self.__balance

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Invalid deposit amount. It must be greater than 0.")
            return False
        self.__balance += amount
        print(f"Deposited Ksh {amount:,.2f}. New balance: Ksh {self.__balance:,.2f}")
        return True

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Invalid withdrawal amount. It must be greater than 0.")
            return False
        if amount > self.__balance:
            print(f"Insufficient funds. Balance: Ksh {self.__balance:,.2f}")
            return False
        self.__balance -= amount
        print(f"Withdrew Ksh {amount:,.2f}. New balance: Ksh {self.__balance:,.2f}")
        return True

    def _charge(self, amount, service_fee):
        """Shared payment logic; subclasses supply their own service fee."""
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Invalid payment amount. It must be greater than 0.")
            return False
        total = amount + service_fee
        if total > self.__balance:
            print(f"Payment failed. Total due Ksh {total:,.2f} "
                  f"(Ksh {amount:,.2f} + Ksh {service_fee} service fee), "
                  f"balance Ksh {self.__balance:,.2f}.")
            return False
        self.__balance -= total
        print(f"Payment successful. Paid Ksh {total:,.2f} "
              f"(Ksh {amount:,.2f} + Ksh {service_fee} service fee). "
              f"New balance: Ksh {self.__balance:,.2f}")
        return True


# ---------------------------------------------------------------------------
# 3. Doctor
# ---------------------------------------------------------------------------
class Doctor:
    def __init__(self, name, doctor_id, specialization, consultation_fee):
        self.name = name
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.consultation_fee = consultation_fee

    def display_info(self):
        print(f"  ID: {self.doctor_id} | Dr. {self.name} | "
              f"{self.specialization} | Fee: Ksh {self.consultation_fee:,.2f}")


# ---------------------------------------------------------------------------
# 4. Inheritance: Outpatient and Inpatient
# ---------------------------------------------------------------------------
class Outpatient(Patient):
    SERVICE_FEE = 100

    def patient_type(self):
        print("Outpatient Patient")

    def process_payment(self, amount):
        return self._charge(amount, self.SERVICE_FEE)


class Inpatient(Patient):
    SERVICE_FEE = 200

    def patient_type(self):
        print("Inpatient Patient")

    def process_payment(self, amount):
        return self._charge(amount, self.SERVICE_FEE)


# ---------------------------------------------------------------------------
# 5. Appointment
# ---------------------------------------------------------------------------
class Appointment:
    def __init__(self, appointment_id, patient, doctor, date, time):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Pending"

    def display_details(self):
        print(f"  Appt #{self.appointment_id} | Patient: {self.patient.name} "
              f"({self.patient.patient_id}) | Dr. {self.doctor.name} "
              f"({self.doctor.specialization}) | {self.date} {self.time} "
              f"| Status: {self.status}")

    def confirm(self):
        if self.status == "Cancelled":
            print("A cancelled appointment cannot be confirmed.")
            return False
        self.status = "Confirmed"
        print(f"Appointment #{self.appointment_id} confirmed.")
        return True

    def cancel(self):
        if self.status == "Cancelled":
            print("Appointment is already cancelled.")
            return False
        self.status = "Cancelled"
        print(f"Appointment #{self.appointment_id} cancelled.")
        return True


# ---------------------------------------------------------------------------
# 6. Record lists
# ---------------------------------------------------------------------------
patients = []
doctors = []
appointments = []


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------
def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_number(prompt, cast=float, minimum=None):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            value = cast(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        return value


# ---------------------------------------------------------------------------
# Lookups (use for loops)
# ---------------------------------------------------------------------------
def find_patient(patient_id):
    for p in patients:
        if p.patient_id == patient_id:
            return p
    return None


def find_doctor(doctor_id):
    for d in doctors:
        if d.doctor_id == doctor_id:
            return d
    return None


def find_appointment(appointment_id):
    for a in appointments:
        if a.appointment_id == appointment_id:
            return a
    return None


# ---------------------------------------------------------------------------
# 8. Functions
# ---------------------------------------------------------------------------
def register_patient():
    print("\n--- Register Patient ---")
    patient_id = read_text("Patient ID: ")
    if find_patient(patient_id):
        print(f"A patient with ID {patient_id} already exists.")
        return
    name = read_text("Full name: ")
    phone = read_text("Phone number: ")
    age = read_number("Age: ", int, 0)
    balance = read_number("Opening account balance (Ksh): ", float, 0)

    print("Patient type: 1. Outpatient  2. Inpatient")
    choice = input("Choose (1/2): ").strip()
    if choice == "1":
        patient = Outpatient(name, patient_id, phone, age, balance)
    elif choice == "2":
        patient = Inpatient(name, patient_id, phone, age, balance)
    else:
        print("Invalid patient type. Registration cancelled.")
        return

    patients.append(patient)
    print(f"Patient {name} registered successfully as ", end="")
    patient.patient_type()


def register_doctor():
    print("\n--- Register Doctor ---")
    doctor_id = read_text("Doctor ID: ")
    if find_doctor(doctor_id):
        print(f"A doctor with ID {doctor_id} already exists.")
        return
    name = read_text("Doctor's name: ")
    specialization = read_text("Specialization: ")
    fee = read_number("Consultation fee (Ksh): ", float, 0)
    doctors.append(Doctor(name, doctor_id, specialization, fee))
    print(f"Dr. {name} registered successfully.")


def book_appointment():
    print("\n--- Book Appointment ---")
    patient = find_patient(read_text("Patient ID: "))
    if patient is None:
        print("Patient not found. Please register the patient first.")
        return
    doctor = find_doctor(read_text("Doctor ID: "))
    if doctor is None:
        print("Doctor not found. Please register the doctor first.")
        return
    date = read_text("Appointment date (e.g. 2026-11-10): ")
    time = read_text("Appointment time (e.g. 10:30): ")

    for a in appointments:
        if (a.doctor is doctor and a.date == date and a.time == time
                and a.status != "Cancelled"):
            print("That doctor already has an appointment at this date and time.")
            return

    appt_id = max((a.appointment_id for a in appointments), default=0) + 1
    appointment = Appointment(appt_id, patient, doctor, date, time)
    appointments.append(appointment)
    appointment.confirm()


def display_patients():
    print("\n--- Registered Patients ---")
    if not patients:
        print("No patients registered yet.")
        return
    for p in patients:
        p.display_details()
        print("    Type: ", end="")
        p.patient_type()


def display_doctors():
    print("\n--- Registered Doctors ---")
    if not doctors:
        print("No doctors registered yet.")
        return
    for d in doctors:
        d.display_info()


def display_appointments():
    print("\n--- Appointments ---")
    if not appointments:
        print("No appointments booked yet.")
        return
    for a in appointments:
        a.display_details()


def search_patient():
    print("\n--- Search Patient ---")
    patient_id = read_text("Enter patient ID: ")
    for p in patients:
        if p.patient_id == patient_id:
            print("Patient found:")
            p.display_details()
            return p
    print(f"No patient found with ID {patient_id}.")
    return None


def deposit_money():
    print("\n--- Deposit Money ---")
    patient = find_patient(read_text("Patient ID: "))
    if patient is None:
        print("Patient not found.")
        return
    patient.deposit(read_number("Amount to deposit (Ksh): ", float))


def withdraw_money():
    print("\n--- Withdraw Money ---")
    patient = find_patient(read_text("Patient ID: "))
    if patient is None:
        print("Patient not found.")
        return
    patient.withdraw(read_number("Amount to withdraw (Ksh): ", float))


def process_patient_payment():
    print("\n--- Process Patient Payment ---")
    patient = find_patient(read_text("Patient ID: "))
    if patient is None:
        print("Patient not found.")
        return
    doctor_id = input("Doctor ID to use their consultation fee "
                      "(press Enter to type an amount instead): ").strip()
    if doctor_id:
        doctor = find_doctor(doctor_id)
        if doctor is None:
            print("Doctor not found.")
            return
        amount = doctor.consultation_fee
    else:
        amount = read_number("Consultation amount (Ksh): ", float)
    patient.process_payment(amount)


def check_patient_balance():
    print("\n--- Check Balance ---")
    patient = find_patient(read_text("Patient ID: "))
    if patient is None:
        print("Patient not found.")
        return
    print(f"{patient.name}'s balance: Ksh {patient.check_balance():,.2f}")


def cancel_appointment():
    print("\n--- Cancel Appointment ---")
    appt_id = read_number("Appointment number: ", int, 1)
    appointment = find_appointment(appt_id)
    if appointment is None:
        print("Appointment not found.")
        return
    appointment.cancel()


# ---------------------------------------------------------------------------
# 9. Polymorphism demonstration
# ---------------------------------------------------------------------------
def demonstrate_polymorphism():
    print("\n=== Polymorphism Demo ===")
    demo_patients = [
        Outpatient("Demo Outpatient", "DEMO-1", "0700000001", 30, 1000),
        Inpatient("Demo Inpatient", "DEMO-2", "0700000002", 45, 1000),
    ]
    for p in demo_patients:      # same calls, different behaviour
        p.patient_type()
        p.process_payment(500)
    print("=========================")


# ---------------------------------------------------------------------------
# 10. Main menu
# ---------------------------------------------------------------------------
MENU = """
========================================
SMART HOSPITAL MANAGEMENT
========================================
1. Register Patient
2. Register Doctor
3. Display All Patients
4. Display All Doctors
5. Book Appointment
6. Display All Appointments
7. Search Patient
8. Deposit Money
9. Withdraw Money
10. Process Patient Payment
11. Check Patient Balance
12. Cancel Appointment
13. Exit
"""

ACTIONS = {
    "1": register_patient,
    "2": register_doctor,
    "3": display_patients,
    "4": display_doctors,
    "5": book_appointment,
    "6": display_appointments,
    "7": search_patient,
    "8": deposit_money,
    "9": withdraw_money,
    "10": process_patient_payment,
    "11": check_patient_balance,
    "12": cancel_appointment,
}


def main():
    demonstrate_polymorphism()
    running = True
    while running:
        print(MENU)
        try:
            choice = input("Enter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if choice in ACTIONS:
            try:
                ACTIONS[choice]()
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled.")
        elif choice == "13":
            print("Thank you for using Smart Hospital Management. Goodbye!")
            running = False
        else:
            print("Invalid choice. Please enter a number from 1 to 13.")


if __name__ == "__main__":
    main()