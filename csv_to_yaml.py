import csv
import yaml
import sys
import os

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

def main(input_csv, output_yaml, dry_run=False):
    # Load existing YAML data
    if os.path.exists(output_yaml):
        with open(output_yaml, 'r', encoding='utf-8') as yf:
            existing_entries = yaml.safe_load(yf) or []
    else:
        existing_entries = []

    # Track normalized names
    existing_names = {entry.get("name", "").strip().lower() for entry in existing_entries}
    skipped_names = []
    added_entries = []

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get("Prénom_Nom", "").strip()
            name_lower = name.lower()
            if name and name_lower not in existing_names:
                new_entry = build_yaml_entry(row)
                added_entries.append(new_entry)
                existing_names.add(name_lower)
            else:
                skipped_names.append(name)

    # Write YAML unless dry run
    if not dry_run:
        with open(output_yaml, 'w', encoding='utf-8') as yamlfile:
            yaml.dump(existing_entries + added_entries, yamlfile, allow_unicode=True, sort_keys=False)

    # Output summary
    if added_entries:
        print(f"{'[DRY RUN] ' if dry_run else ''}Added entries:")
        for e in added_entries:
            print(f" + {e['name']}")

    if skipped_names:
        print(f"{'[DRY RUN] ' if dry_run else ''}Skipped (already in YAML):")
        for name in skipped_names:
            print(f" - {name}")

    if not added_entries and not skipped_names:
        print("No valid rows found in CSV.")

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage: python csv_to_yaml.py input.csv members.yaml [--dry-run]")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_yaml = sys.argv[2]
    dry_run_flag = "--dry-run" in sys.argv

    main(input_csv, output_yaml, dry_run=dry_run_flag)
