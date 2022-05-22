import json
import os


def load_bundle(bundle_file):
    """
    Loads a bundle from a file
    """
    with open(bundle_file) as f:
        loaded_bundle = json.load(f)
    return loaded_bundle


def extract_patient_data(bundle_file):
    """
    Extracts the patient data from a bundle
    """
    bundle = load_bundle(bundle_file)
    patient = bundle["entry"][0]["resource"]
    return patient


def get_bundle_files():
    bundle_list = []
    for root, dirs, files in os.walk("bundles"):
        for file in files:
            if file.endswith(".json"):
                bundle_list.append(os.path.join(root, file))
    return bundle_list


def extract_patients():
    bundle_list = get_bundle_files()
    for bundle in bundle_list:
        print(bundle)
        patient = extract_patient_data(bundle)
        with open(
            "patients_json/"
            + str(bundle.split("/")[-1].split(".")[0])
            + "_extracted.json",
            "w",
        ) as f:
            json.dump(patient, f)


def format_patients_into_ndjson():
    for file in os.listdir("patients_json"):
        if file.endswith(".json"):
            with open("patients_json/" + file) as f:
                patient = json.load(f)
            with open("patients_ndjson/" + file.split(".")[0] + ".ndjson", "w") as f:
                json.dump(patient, f)


def merge_patients_ndjson():
    with open("merged_patients/patients.ndjson", "w") as f:
        for file in os.listdir("patients_ndjson"):
            if file.endswith(".ndjson"):
                with open("patients_ndjson/" + file) as f2:
                    f.write(f2.read())
                    f.write("\n")


def compress_patients():
    for file in os.listdir("merged_patients"):
        if file.endswith(".ndjson"):
            os.system("gzip -9 merged_patients/" + file)
    print("Completed")


def create_folders():
    os.system("mkdir merged_patients")
    os.system("mkdir patients_json")
    os.system("mkdir patients_ndjson")


def main():
    create_folders()
    extract_patients()
    format_patients_into_ndjson()
    merge_patients_ndjson()
    compress_patients()


main()
