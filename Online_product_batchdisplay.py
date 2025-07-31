import time
import sys

sample_data = [
    {"ProductID": 101, "ProductName": "Widget A", "Category": "Gadgets"},
    {"ProductID": 102, "ProductName": "Widget B", "Category": "Gadgets"},
    {"ProductID": 103, "ProductName": "Gizmo A",   "Category": "Tools"},
    {"ProductID": 104, "ProductName": "Gizmo B",   "Category": "Tools"},
    {"ProductID": 105, "ProductName": "Doodad A",  "Category": "Widgets"},
    {"ProductID": 106, "ProductName": "Doodad B",  "Category": "Widgets"},
    {"ProductID": 107, "ProductName": "Gadget C",  "Category": "Gadgets"},
    {"ProductID": 108, "ProductName": "Tool X",    "Category": "Tools"},
    {"ProductID": 109, "ProductName": "Tool Y",    "Category": "Tools"},
    {"ProductID": 110, "ProductName": "Gadget Z",  "Category": "Gadgets"}
]

BATCH_SIZE = 2
DELAY = 10

def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r Next batch in {i} seconds")
        sys.stdout.flush()
        time.sleep(1)
    print("\r Showing next batch")

def batch_product_data():
    print("Starting live stream of data\n")
    current_index = 0
    batch_num = 1

    while current_index < len(sample_data):
        batch = sample_data[current_index:current_index + BATCH_SIZE]
        print(f"\n Batch {batch_num}:")
        for record in batch:
            print(f"{record}")
        current_index += BATCH_SIZE
        batch_num += 1

        if current_index < len(sample_data):
            countdown(DELAY)

if __name__ == "__main__":
    batch_product_data()