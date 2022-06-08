import json
import os


def get_list_of_bundles():
    print("Getting list of bundles...")
    bundle_list = []
    for root, dirs, files in os.walk("bundles"):
        for file in files:
            if file.endswith(".json"):
                bundle_list.append(os.path.join(root, file))
    return bundle_list


def load_bundle(bundle_file):
    print(f"Loading bundle {bundle_file}")
    with open(bundle_file) as f:
        loaded_bundle = json.load(f)
    return loaded_bundle


def extract_resources(bundle_file):
    bundle = load_bundle(bundle_file)
    print(f"Extracting resources from {bundle_file}")
    resources = bundle["entry"]
    return resources


def create_resources_ndjson(resources_list):
    print("Creating resources.ndjson...")
    with open("resources.ndjson", "w") as f:
        for resources in resources_list:
            for resource in resources:
                json.dump(resource["resource"], f)
                f.write("\n")


def compress_resources():
    print("Compressing resources...")
    os.system("gzip -9 resources.ndjson")


def main():
    bundle_list = get_list_of_bundles()
    resources_list = []
    for bundle in bundle_list:
        resources = extract_resources(bundle)
        resources_list.append(resources)
    create_resources_ndjson(resources_list)
    compress_resources()
    print("Complete")



if __name__ == "__main__":
    main()
