import yaml
import sys

def count_names(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        print("The YAML file does not contain a list of entries.")
        return

    count = sum(1 for entry in data if isinstance(entry, dict) and "name" in entry)
    print(f"Total entries with a 'name' field: {count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_names_in_yaml.py members.yaml")
        sys.exit(1)

    yaml_file = sys.argv[1]
    count_names(yaml_file)
