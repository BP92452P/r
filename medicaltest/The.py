# The.py
# Computer Science Final Project

# ---------------- FUNCTIONS ---------------- #

def load_file(filename):
    data = {}
    file = open(filename, "r")
    for line in file:
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    file.close()
    return data


def determine_age_group(age):
    if age < 13:
        return "child"
    else:
        return "adult"


def determine_sickness(symptoms):
    scores = {
        "Flu": 0,
        "Cold": 0,
        "Allergy": 0
    }

    for symptom in symptoms:
        if symptom in ["fever", "body ache", "chills"]:
            scores["Flu"] += 1
        if symptom in ["cough", "sore throat", "runny nose"]:
            scores["Cold"] += 1
        if symptom in ["sneezing", "itchy eyes", "runny nose"]:
            scores["Allergy"] += 1

    return max(scores, key=scores.get)


def get_medicine(sickness):
    if sickness == "Flu":
        return "Tylenol"
    elif sickness == "Cold":
        return "CoughSyrup"
    elif sickness == "Allergy":
        return "Antihistamine"


# ---------------- MAIN PROGRAM ---------------- #

print("Welcome to the Medical Diagnosis Program")

age = int(input("Enter your age: "))
age_group = determine_age_group(age)

symptom_input = input("Enter your symptoms (comma separated): ")
symptoms = symptom_input.lower().split(", ")

sickness = determine_sickness(symptoms)
medicine = get_medicine(sickness)

medicines = load_file("medicine.txt")
schedules = load_file("schedule.txt")
definitions = load_file("definitions.txt")

# Dosage
dosage_info = medicines[medicine].split(", ")
dosage = dosage_info[0] if age_group == "child" else dosage_info[1]

# Schedule
schedule_info = schedules[medicine].split(" | ")
schedule = schedule_info[0] if age_group == "child" else schedule_info[1]

# Definition
definition = definitions[medicine]

# ---------------- OUTPUT ---------------- #

print("\n--- Diagnosis Result ---")
print("Sickness:", sickness)
print("Recommended Medicine:", medicine)
print("Dosage:", dosage)
print("Weekly Schedule:", schedule)
print("\nMedicine Information:")
print(definition)
