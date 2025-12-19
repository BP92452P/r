import os



def load_file(filename):
    
    """Loads key:value pairs from a file where each line is "key: value". Returns a dictionary."""
    
    data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found. Please make sure it exists in the same folder as this script.")
        exit(1)
    return data


def determine_age_group(age):
    
    """Returns 'child' if age < 13, else 'adult'."""
    
    if age < 13:
        return "child"
    else:
        return "adult"


def determine_sickness(symptoms):
    
    """This scores zhe symptoms to determine zhe most likely illness"""
    
    scores = {
        "Flu": 0,
        "Cold": 0,
        "Allergy": 0,
        "StomachAche": 0,
        "Headache": 0
    }
    

    for symptom in symptoms:
        symptom = symptom.lower()
        if symptom in ["fever", "body ache", "chills"]:
            scores["Flu"] += 1
        if symptom in ["cough", "sore throat", "runny nose"]:
            scores["Cold"] += 1
        if symptom in ["sneezing", "itchy eyes", "runny nose"]:
            scores["Allergy"] += 1
        if symptom in ["nausea", "vomiting", "diarrhea", "stomach pain"]:
            scores["StomachAche"] += 1
        if symptom in ["headache", "migraine", "sensitivity to light"]:
            scores["Headache"] += 1


    # Return sickness with highest score; if the socore is 0 tie, returns Cold
    max_score = max(scores.values())
    if max_score == 0:
        return "Cold"
    sickness_candidates = [k for k, v in scores.items() if v == max_score]
    return sickness_candidates[0]


def get_medicine(sickness):
    
    """Returns medicine recommended for the sickness."""
    
    if sickness == "Flu":
        return "Tylenol"
    elif sickness == "Cold":
        return "CoughSyrup"
    elif sickness == "Allergy":
        return "Antihistamine"
    elif sickness == "StomachAche":
        return "PeptoBismol"
    elif sickness == "Headache":
        return "Ibuprofen"
   
    else:
        return None


def main():
    print(" ")
    print("              Welcome to the Medical Diagnosis Program")
    print("--"*30)
    print(" ")
    print("The symptoms registered are as follows: ")
    print(" ")
    print("Fever, body ache, chills, sore throat, cough, runny nose, sneezing, itchy eyes, nausea, vomiting, diarrhea, stomach pain, headache, migraine, sensitivity to light")
    print(" ")
    print("--"*30)
    print(" ")

    # invalidation loop for ensuring age is valid number
    while True:
        try:
            age = int(input("Enter your age: ").strip())
            if age < 0:
                print("Age cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid whole number for age.")

    age_group = determine_age_group(age)

    symptom_input = input("Enter your symptoms (comma separated): ").strip()
    # splitting symptoms, removing spaces whatnot
    symptoms = [sym.strip().lower() for sym in symptom_input.split(",") if sym.strip()]

    # Determine sickness and medicine
    sickness = determine_sickness(symptoms)
    medicine = get_medicine(sickness)

    # Load files from the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    medicines = load_file(os.path.join(script_dir, "medicine.txt"))
    schedules = load_file(os.path.join(script_dir, "schedule.txt"))
    definitions = load_file(os.path.join(script_dir, "definitions.txt"))

    if medicine not in medicines:
        print(f"Medicine '{medicine}' not found in medicine.txt.")
        exit(1)

    if medicine not in schedules:
        print(f"Medicine '{medicine}' not found in schedule.txt.")
        exit(1)

    if medicine not in definitions:
        print(f"Medicine '{medicine}' not found in definitions.txt.")
        exit(1)

    # Get dosage for age group
    dosage_info = medicines[medicine].split(",")
    dosage_info = [d.strip() for d in dosage_info]
    dosage = dosage_info[0] if age_group == "child" else dosage_info[1]

    # Get schedule for age group
    schedule_info = schedules[medicine].split("|")
    schedule_info = [s.strip() for s in schedule_info]
    schedule = schedule_info[0] if age_group == "child" else schedule_info[1]

    # Get medicine definition
    definition = definitions[medicine]

    # results
    print("\n--- Diagnosis Result ---")
    print(f"Sickness: {sickness}")
    print(f"Recommended Medicine: {medicine}")
    print(f"Dosage: {dosage}")
    print(f"Weekly Schedule: {schedule}")

    print("\nMedicine Information:")
    print(definition)


class Patient:
    def __init__(self, age, symptoms):
        self.age = age
        self.symptoms = symptoms
        self.age_group = determine_age_group(age)
        self.sickness = determine_sickness(symptoms)
        self.medicine = get_medicine(self.sickness)

    def display_summary(self):
        print("\n--- Patient Summary ---")
        print(f"Age: {self.age} ({self.age_group})")
        print(f"Symptoms: {', '.join(self.symptoms)}")
        print(f"Diagnosed Sickness: {self.sickness}")
        print(f"Recommended Medicine: {self.medicine}")


class DiagnosisSystem:
    def __init__(self, script_dir):
        self.medicines = load_file(os.path.join(script_dir, "medicine.txt"))
        self.schedules = load_file(os.path.join(script_dir, "schedule.txt"))
        self.definitions = load_file(os.path.join(script_dir, "definitions.txt"))

    def get_dosage(self, medicine, age_group):
        dosage_info = self.medicines[medicine].split(",")
        dosage_info = [d.strip() for d in dosage_info]
        return dosage_info[0] if age_group == "child" else dosage_info[1]

    def get_schedule(self, medicine, age_group):
        schedule_info = self.schedules[medicine].split("|")
        schedule_info = [s.strip() for s in schedule_info]
        return schedule_info[0] if age_group == "child" else schedule_info[1]

    def get_definition(self, medicine):
        return self.definitions[medicine]


def run_with_classes():
    print("\nExample of our program")
    # pythons run
    age = 4
    symptoms = ["cough", "fever"]

    patient = Patient(age, symptoms)
    patient.display_summary()

    system = DiagnosisSystem(os.path.dirname(os.path.abspath(__file__)))

    if patient.medicine in system.medicines:
        dosage = system.get_dosage(patient.medicine, patient.age_group)
        schedule = system.get_schedule(patient.medicine, patient.age_group)
        definition = system.get_definition(patient.medicine)

        print("\n--- Example results ---")
        print(f"Sickness: {patient.sickness}")
        print(f"Medicine: {patient.medicine}")
        print(f"Dosage: {dosage}")
        print(f"Schedule: {schedule}")
        print(f"Definition: {definition}")
    else:
        print(f"Medicine '{patient.medicine}' not found in files.")
        print("Hi")

if __name__ == "__main__":
     
    run_with_classes()
    
    main()

