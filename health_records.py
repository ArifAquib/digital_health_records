from blockchain import Blockchain

# Initialize the blockchain
blockchain = Blockchain()
blockchain.load_from_file()

def add_health_record(patient_name, record):
    """
    Adds a health record for a patient to the blockchain.
    """
    data = f"Patient: {patient_name}, Record: {record}"
    blockchain.add_block(data)
    blockchain.save_to_file()
    return "Health record successfully added to the blockchain!"

def get_patient_records(patient_name):
    """
    Retrieves all records for a specific patient.
    """
    records = []
    for block in blockchain.chain:
        if block.data.startswith(f"Patient: {patient_name}"):
            records.append(block.data.replace(f"Patient: {patient_name}, ", ""))
    return records

def get_all_patients():
    """
    Retrieves a list of unique patient names.
    """
    patients = set()
    for block in blockchain.chain:
        if "Patient:" in block.data:
            patient_name = block.data.split(",")[0].replace("Patient: ", "")
            patients.add(patient_name)
    return sorted(patients)
