# The.py
# Beginner-friendly symptom matcher + dosing scheduler
# Reads: symptoms.txt, medications.txt (in same directory)
# Outputs: diagnosis, chosen medication, dose for age, schedule, and definition

def normalize_token(s):
    """Lowercase, strip, collapse internal spaces."""
    return " ".join(s.strip().lower().split())

def parse_age(age_text):
    """Parse age to float and validate reasonable human range."""
    try:
        age = float(age_text.strip())
        if age < 0 or age > 150:
            print("[Warning] Age out of supported range (0–150).")
            return None
        return age
    except:
        print("[Warning] Age must be a number.")
        return None

def read_symptoms_file(path):
    """
    Read symptoms.txt
    Format: Diagnosis|symptom1,symptom2,...
    Returns: dict {diagnosis: set(symptoms)}
    """
    mapping = {}
    try:
        f = open(path, "r")
    except:
        print("[Error] Could not open symptoms file:", path)
        return mapping

    line_num = 0
    for raw in f:
        line_num += 1
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) != 2:
            print("[Warning] Malformed line in symptoms file at line", line_num, ":", raw.strip())
            continue
        diagnosis = normalize_token(parts[0])
        keywords_text = parts[1]
        keywords = []
        for k in keywords_text.split(","):
            nk = normalize_token(k)
            if nk != "":
                keywords.append(nk)
        if diagnosis == "" or len(keywords) == 0:
            print("[Warning] Missing diagnosis or keywords at line", line_num)
            continue
        mapping[diagnosis] = set(keywords)
    f.close()
    return mapping

def parse_range_item(item_text):
    """
    Parse a single age-dose item like '0-5=100'
    Returns: (min_age, max_age, dose_mg) or None on error
    """
    item_text = item_text.strip()
    if item_text == "":
        return None
    eq_split = item_text.split("=")
    if len(eq_split) != 2:
        return None
    range_text = eq_split[0].strip()
    dose_text = eq_split[1].strip()
    dash_split = range_text.split("-")
    if len(dash_split) != 2:
        return None
    try:
        min_age = float(dash_split[0].strip())
        max_age = float(dash_split[1].strip())
        dose_mg = float(dose_text)
        return (min_age, max_age, dose_mg)
    except:
        return None

def read_medications_file(path):
    """
    Read medications.txt
    Format: Drug|Diagnosis|Definition|ageRanges|schedule
    ageRanges: '0-5=100;6-12=200;13-64=400;65-150=300'
    schedule: '08:00,20:00'
    Returns: list of dicts
    """
    meds = []
    try:
        f = open(path, "r")
    except:
        print("[Error] Could not open medications file:", path)
        return meds

    line_num = 0
    for raw in f:
        line_num += 1
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) != 5:
            print("[Warning] Malformed line in medications file at line", line_num, ":", raw.strip())
            continue

        drug = normalize_token(parts[0])
        diagnosis = normalize_token(parts[1])
        definition = parts[2].strip()  # Keep case and punctuation for readability
        age_ranges_text = parts[3]
        schedule_text = parts[4]

        # Parse age ranges
        ranges = []
        for item in age_ranges_text.split(";"):
            parsed = parse_range_item(item)
            if parsed is None:
                print("[Warning] Bad age-range item at line", line_num, "->", item.strip())
                continue
            ranges.append(parsed)

        # Parse schedule times
        schedule = []
        for t in schedule_text.split(","):
            nt = t.strip()
            if nt != "":
                schedule.append(nt)

        if drug == "" or diagnosis == "" or definition == "" or len(ranges) == 0 or len(schedule) == 0:
            print("[Warning] Incomplete medication entry at line", line_num)
            continue

        meds.append({
            "drug": drug,
            "diagnosis": diagnosis,
            "definition": definition,
            "ranges": ranges,          # list of (min_age, max_age, dose_mg) tuples
            "schedule": schedule       # list of times like ["08:00","20:00"]
        })

    f.close()
    return meds

def score_diagnosis(user_symptoms, diagnosis_keywords):
    """
    Score overlap between user symptoms (set) and diagnosis keywords (set).
    Returns integer overlap count.
    """
    count = 0
    for s in user_symptoms:
        if s in diagnosis_keywords:
            count += 1
    return count

def find_best_diagnosis(user_symptoms, symptom_map):
    """
    Return (best_diagnosis, score). If none, returns (None, 0).
    """
    best = None
    best_score = 0
    # Deterministic order by diagnosis name for tie-breaking
    diagnoses = list(symptom_map.keys())
    diagnoses.sort()
    for d in diagnoses:
        score = score_diagnosis(user_symptoms, symptom_map[d])
        if score > best_score:
            best = d
            best_score = score
    return (best, best_score)

def select_medication_for_diagnosis(diagnosis, meds):
    """
    Pick the first medication that matches the diagnosis (after sorting by drug name).
    Returns med dict or None.
    """
    candidates = []
    for m in meds:
        if m["diagnosis"] == diagnosis:
            candidates.append(m)
    if len(candidates) == 0:
        return None
    # Sort by drug name for deterministic selection
    candidates.sort(key=lambda x: x["drug"])
    return candidates[0]

def dose_for_age(age, ranges):
    """
    Given age (float) and ranges [(min,max,dose),...], return dose mg or None if no range matches.
    Inclusive bounds.
    """
    # Sort ranges by min_age then max_age for deterministic matching
    ordered = list(ranges)
    ordered.sort(key=lambda r: (r[0], r[1]))
    for (min_a, max_a, dose) in ordered:
        if age >= min_a and age <= max_a:
            return dose
    return None

def format_schedule(schedule):
    """Return a human-readable schedule string."""
    if len(schedule) == 1:
        return "Take at " + schedule[0]
    return "Take at " + ", ".join(schedule[:-1]) + " and " + schedule[-1]

def prompt_user_symptoms():
    """
    Prompt for comma-separated symptoms, normalize into a set of tokens.
    """
    text = input("Enter your symptoms (comma-separated): ").strip()
    tokens = []
    for t in text.split(","):
        nt = normalize_token(t)
        if nt != "":
            tokens.append(nt)
    return set(tokens)

def main():
    print("=== Symptom Matcher & Dosing Planner ===")
    print("Note: This is an educational demo. For medical concerns, consult a professional.\n")

    symptom_map = read_symptoms_file("symptoms.txt")
    meds = read_medications_file("medications.txt")

    if len(symptom_map) == 0:
        print("[Error] No symptom data loaded. Exiting.")
        return
    if len(meds) == 0:
        print("[Error] No medication data loaded. Exiting.")
        return

    user_symptoms = prompt_user_symptoms()
    if len(user_symptoms) == 0:
        print("[Warning] No symptoms entered. Exiting.")
        return

    age_text = input("Enter your age (years): ")
    age = parse_age(age_text)
    if age is None:
        print("[Error] Invalid age. Exiting.")
        return

    best_diag, score = find_best_diagnosis(user_symptoms, symptom_map)
    if best_diag is None or score == 0:
        print("\nNo confident diagnosis found from provided symptoms.")
        print("Try using simpler, common keywords (e.g., 'fever', 'cough', 'headache').")
        return

    med = select_medication_for_diagnosis(best_diag, meds)
    if med is None:
        print("\nDiagnosis:", best_diag.title())
        print("No medication data available for this diagnosis.")
        return

    dose_mg = dose_for_age(age, med["ranges"])
    print("\n=== Result ===")
    print("Diagnosis:", best_diag.title())
    print("Medication:", med["drug"].title())

    if dose_mg is None:
        print("Dose: No age-appropriate dose found in data.")
    else:
        # Using float while printing cleanly
        if dose_mg.is_integer():
            dose_display = str(int(dose_mg))
        else:
            dose_display = str(dose_mg)
        print("Dose per administration:", dose_display, "mg")

    print("Schedule:", format_schedule(med["schedule"]))
    print("\nDefinition:")
    print(med["definition"])

    print("\nReminder: This program is for learning purposes and is not medical advice.")

if __name__ == "__main__":
    main()
