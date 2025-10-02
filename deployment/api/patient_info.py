
def patient_info(id,name,age,phone):
    import yaml

    # Load the YAML file
    with open("deployment/api/pat_info/patient.yaml", "r") as file:
        data = yaml.safe_load(file) or {}

    # ID under which to add the student
    patient_id = id

    # New student details
    new_student = {
        "name": name,
        "age": age,
        "Phone": phone
    }

    # If the ID doesn't exist, create a new list
    if patient_id not in data:
        data[patient_id] = []

    # Append the student if not already in the list
    if new_student not in data[patient_id]:
        data[patient_id].append(new_student)

    
    # ✅ Sort records by USN before dumping
    data_sorted = dict(sorted(data.items(), key=lambda x: x[0]))

    # Write back to the file
    with open("deployment/api/pat_info/patient.yaml", "w") as file:
        yaml.safe_dump(data_sorted, file, sort_keys=False)