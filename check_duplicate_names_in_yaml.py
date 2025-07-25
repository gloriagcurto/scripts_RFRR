import yaml
import sys
from collections import Counter

def check_duplicates(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        print("The YAML file does not contain a list of entries.")
        return

    names = [entry.get("name", "").strip() for entry in data if isinstance(entry, dict) and "name" in entry]
    name_counts = Counter(names)

    duplicates = {name: count for name, count in name_counts.items() if count > 1 and name}
    
    if duplicates:
        print("Duplicate names found:")
        for name, count in duplicates.items():
            print(f" - {name}: {count} times")
    else:
        print("No duplicate names found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_duplicate_names.py members.yaml")
        sys.exit(1)

    yaml_file = sys.argv[1]
    check_duplicates(yaml_file)
