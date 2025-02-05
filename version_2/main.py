import re
import csv
import json
from datetime import datetime

def validate_date(date_string):
    pattern = r'^(\d{2})-(\d{2})-(\d{4})$'
    match = re.match(pattern, date_string)
    if not match:
        return False
    
    day, month, year = map(int, match.groups())
    if month < 1 or month > 12:
        return False
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month[1] = 29
    
    if day < 1 or day > days_in_month[month - 1]:
        return False
    
    return True

def validate_phone(phone):
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    return re.match(pattern, phone) is not None

def calculate_age(date_of_birth):
    today = datetime.today()
    birth_date = datetime.strptime(date_of_birth, '%d-%m-%Y')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def read_patients_csv():
    with open('patients.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_patients_csv(patients):
    with open('patients.csv', 'w', newline='') as file:
        fieldnames = ['id', 'first_name', 'last_name', 'date_of_birth', 'age', 'hometown', 'house_number', 'phone_number']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(patients)

def read_patients_json():
    with open('patients.json', 'r') as file:
        return json.load(file)

def write_patients_json(patients):
    with open('patients.json', 'w') as file:
        json.dump(patients, file, indent=4)

def add_patient(storage_type):
    new_patient = {}
    new_patient['id'] = str(len(get_all_patients(storage_type)) + 1)
    new_patient['first_name'] = input("First Name: ")
    new_patient['last_name'] = input("Last Name: ")
    date_of_birth = input("Date of Birth (dd-mm-yyyy): ")
    while not validate_date(date_of_birth):
        print("Invalid date format or date. Please try again.")
        date_of_birth = input("Date of Birth (dd-mm-yyyy): ")
    new_patient['date_of_birth'] = date_of_birth
    new_patient['age'] = calculate_age(date_of_birth)
    new_patient['hometown'] = input("Hometown: ")
    new_patient['house_number'] = input("House Number: ")
    phone_number = input("Phone Number (024-000-0000): ")
    while not validate_phone(phone_number):
        print("Invalid phone number format. Please try again!.")
        phone_number = input("Phone Number (024-000-0000): ")
    new_patient['phone_number'] = phone_number
    
    patients = get_all_patients(storage_type)
    patients.append(new_patient)
    if storage_type == 'csv':
        write_patients_csv(patients)
    else:
        write_patients_json(patients)

def get_all_patients(storage_type):
    try:
        if storage_type == 'csv':
            return read_patients_csv()
        else:
            return read_patients_json()
    except FileNotFoundError:
        print("File not found. Creating new file.")
        return []

def search_patient_by_id(patient_id, storage_type):
    patients = get_all_patients(storage_type)
    for patient in patients:
        if patient['id'] == patient_id:
            return patient
    return None

def update_patient_by_id(patient_id, storage_type):
    patients = get_all_patients(storage_type)
    for patient in patients:
        if patient['id'] == patient_id:
            for key, value in patient.items():
                if key != 'id':
                    new_value = input(f"Enter new {key} or press Enter to keep '{value}': ")
                    if new_value:
                        patient[key] = new_value
            if 'date_of_birth' in patient:
                patient['age'] = calculate_age(patient['date_of_birth'])
            if storage_type == 'csv':
                write_patients_csv(patients)
            else:
                write_patients_json(patients)
            return True
    return False

def delete_patient_by_id(patient_id, storage_type):
    patients = get_all_patients(storage_type)
    for i, patient in enumerate(patients):
        if patient['id'] == patient_id:
            del patients[i]
            if storage_type == 'csv':
                write_patients_csv(patients)
            else:
                write_patients_json(patients)
            return True
    return False

def main():
    storage_type = input("Select storage type (csv/json): ").lower()
    if storage_type not in ['csv', 'json']:
        print("Invalid storage type. Defaulting to CSV.")
        storage_type = 'csv'

    while True:
        print("\n1. Add New Patient")
        print("2. Get All Patients")
        print("3. Search Patient by ID")
        print("4. Update Patient by ID")
        print("5. Delete Patient by ID")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_patient(storage_type)
        elif choice == '2':
            patients = get_all_patients(storage_type)
            for patient in patients:
                print(patient)
        elif choice == '3':
            patient_id = input("Enter patient ID to search: ")
            patient = search_patient_by_id(patient_id, storage_type)
            if patient:
                print(patient)
            else:
                print("Patient not found.")
        elif choice == '4':
            patient_id = input("Enter patient ID to update: ")
            if not update_patient_by_id(patient_id, storage_type):
                print("Patient not found.")
        elif choice == '5':
            patient_id = input("Enter patient ID to delete: ")
            if not delete_patient_by_id(patient_id, storage_type):
                print("Patient not found. Try again")
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()