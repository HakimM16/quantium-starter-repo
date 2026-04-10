import csv
import glob
import os


def process_sales_data(data_dir="data", output_file="output.csv"):
    rows = []

    for filepath in sorted(glob.glob(os.path.join(data_dir, "daily_sales_data_*.csv"))):
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["product"].strip().lower() != "pink morsel":
                    continue
                price = float(row["price"].strip().replace("$", ""))
                quantity = int(row["quantity"].strip())
                sales = price * quantity
                rows.append({
                    "sales": sales,
                    "date": row["date"].strip(),
                    "region": row["region"].strip(),
                })

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sales", "date", "region"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_file}")


if __name__ == "__main__":
    process_sales_data()
