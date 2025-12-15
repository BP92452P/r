# --------------------------------------------------
# DISCLAIMER:
# This program is for educational purposes only.
# It does NOT provide real medical advice.
# All illnesses and medicines are fictional.
# --------------------------------------------------

import os

# ---------- FILE LOADING FUNCTION ----------

def load_simple_file(filename):
    data = {}

    try:
        file = open(filename, "r")
    except:
        print("Error: Could not open", filename)
        return data

    for line in file:
        line = line.strip()

        if line == "":
            continue

        parts = line.split("|")

        if len(parts) < 2:
            continue

        key = parts[0].strip().lower()
        values = parts[1:]

        data[key] = values

    file.close()
    return data


# ---------- SYMPTOM SCORING DIAGNOSIS ----------

def diagnose(symptoms):
    illness_symptoms = {
        "flulike": ["fever", "cough", "fatigue", "body aches"],
        "coldlike": ["sneezing", "runny nose", "sore throat"],
        "stomachbug": ["nausea", "vomiting", "stomach pain"]
    }

    scores = {}

    for illness in illness_symptoms:
        score = 0
        for symptom in illness_symptoms[illness]:
            if symptom in symptoms:
                score += 1
        scores[illness] = score

    # Find illness with highest score
    best_illness = "unknown"
    highest_score = 0

    for illness in scores:
        if scores[illness] > highest_score:
            highest_score = scores[illness]
            best_illness = illness

    if highest_score == 0:
        return "unknown"
    else:
        return best_illness


# ---------- MAIN PROGRAM ----------

print("Welcome to the Diagnosis Simulator")
print("----------------------------------")

# Get age
age = int(input("Enter your age: "))

# Get symptoms
symptom_input = input("Enter your symptoms separated by commas: ")
symptoms = symptom_input.lower().split(",")

for i in range(len(symptoms)):
    symptoms[i] = symptoms[i].strip()

# Get base directory (works on any computer)
base_dir = os.path.dirname(__file__)

medicine_file = os.path.join(base_dir, "medicine.txt")
definitions_file = os.path.join(base_dir, "definitions.txt")
schedule_file = os.path.join(base_dir, "schedule.txt")

# Load data files
medicine_data = load_simple_file(medicine_file)
definitions = load_simple_file(definitions_file)
schedules = load_simple_file(schedule_file)

# Diagnose illness
illness = diagnose(symptoms)

print("\nDiagnosis Result")
print("----------------")

if illness == "unknown":
    print("No matching illness found.")
    print("Please consult a real doctor.")
else:
    medicine_info = medicine_data.get(illness)

    if medicine_info is None:
        print("No medicine data available.")
    else:
        medicine_name = medicine_info[0]

        print("Likely illness:", illness.capitalize())
        print("Recommended medicine:", medicine_name)

        # Definition
        if medicine_name.lower() in definitions:
            print("\nMedicine Information:")
            print(definitions[medicine_name.lower()][0])

        # Dosage Schedule
        if medicine_name.lower() in schedules:
            print("\nDosage Schedule:")
            if age < 18:
                print(schedules[medicine_name.lower()][0])
            else:
                print(schedules[medicine_name.lower()][1])
