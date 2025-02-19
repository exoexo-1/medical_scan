import csv

# Define the scan types
SCAN_TYPES = ["CT", "MRI", "X-ray", "PET", "Ultrasound", "Microscopy", "Graphics"]

# Initialize counters
total_images = 0
scan_type_counts = {scan: 0 for scan in SCAN_TYPES}
description_count = 0
bottom_line_count = 0

# Read the CSV file
csv_filename = "brain_scan_dataset.csv"  # Change this if your file has a different name
with open(csv_filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        total_images += 1

        # Count scan types (multiple scan types are separated by commas)
        scan_types = row["Scan Type(s)"].split(", ")
        for scan in scan_types:
            if scan in scan_type_counts:
                scan_type_counts[scan] += 1

        # Count images with descriptions
        if row["Scan Description"].strip():
            description_count += 1

        # Count images with bottom line summaries
        if row["Bottom Line"].strip().lower() != "no bottom line":
            bottom_line_count += 1

# Calculate missing values
partial_description_count = total_images - description_count
missing_bottom_line_count = total_images - bottom_line_count

# Print results
print(f"Dataset Statistics\n")
print(f"Total Images: {total_images}\n")

print("Scan Types Distribution:")
for scan, count in scan_type_counts.items():
    print(f"{scan}: {count}")

print("\nDescription Availability:")
print(f"Fully annotated images: {description_count}")
print(f"Partially annotated images: {partial_description_count}\n")

print("Bottom Line Summary Availability:")
print(f"Present in: {bottom_line_count} images")
print(f"Absent in: {missing_bottom_line_count} images")
