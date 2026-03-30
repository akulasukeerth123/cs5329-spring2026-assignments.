import csv
import random
import argparse

def generate_dataset(rows, output):
    with open(output, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["title", "views", "likes", "comment_count"])

        for i in range(rows):
            writer.writerow([
                f"Video {i}",
                random.randint(1000, 1000000),
                random.randint(100, 50000),
                random.randint(10, 10000)
            ])

    print(f"Generated {rows} rows → {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=100000)
    parser.add_argument("--output", default="dataset.csv")

    args = parser.parse_args()

    generate_dataset(args.rows, args.output)