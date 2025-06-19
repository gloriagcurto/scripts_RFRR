import csv
import yaml
import sys

def build_yaml_entry(row):
    entry = {
        "name": row.get("Prénom_Nom", "").strip(),
        "lab": " ".join(filter(None, [
            row.get("Laboratoire", "").strip(),
            row.get("Tutelle1", "").strip(),
            row.get("Tutelle2", "").strip()
        ])),
        "city": row.get("Ville", "").strip()
    }

    # Ajout conditionnel des champs si non vides
    url = row.get("url", "").strip()
    if url:
        entry["url"] = url

    image = row.get("image", "").strip()
    if image:
        entry["image"] = image

    if row.get("Coord", "").strip().lower() == "true":
        entry["coord"] = True

    if row.get("Copil", "").strip().lower() == "true":
        entry["steering"] = True

    return entry

def main(input_csv, output_yaml):
    entries = []

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entry = build_yaml_entry(row)
            entries.append(entry)

    with open(output_yaml, 'w', encoding='utf-8') as yamlfile:
        yaml.dump(entries, yamlfile, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_yaml.py input.csv output.yaml")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_yaml = sys.argv[2]
    main(input_csv, output_yaml)
