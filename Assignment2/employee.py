import csv
import os


class Employee:
    def __init__(self, filename="employee.csv"):
        self.file = filename
        self.fields = ["id", "name", "department", "salary"]
        if not os.path.exists(self.file):
            with open(self.file, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writeheader()

    def _read_all(self):
        with open(self.file, "r", newline="") as file:
            return list(csv.DictReader(file))

    def _write_all(self, rows):
        with open(self.file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(rows)

    def add_employee(self):
        emp_id = input("Enter ID: ").strip()
        rows = self._read_all()
        if any(row["id"] == emp_id for row in rows):
            print("ID already exists.")
            return

        name = input("Enter Name: ").strip()
        department = input("Enter Department: ").strip()
        salary = input("Enter Salary: ").strip()

        with open(self.file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([emp_id, name, department, salary])

        print("Record added successfully!")

    def display_employee(self):
        rows = self._read_all()
        if not rows:
            print("No records available.")
            return
        print("\nEmployee Details:")
        for row in rows:
            print(
                f"ID: {row['id']} | Name: {row['name']} | "
                f"Department: {row['department']} | Salary: {row['salary']}"
            )

    def search_employee(self):
        emp_id = input("Enter ID to search: ").strip()
        rows = self._read_all()
        for row in rows:
            if row["id"] == emp_id:
                print("Record found:", row)
                return
        print("Record not found.")

    def update_employee(self):
        emp_id = input("Enter ID to update: ").strip()
        rows = self._read_all()
        found = False
        for row in rows:
            if row["id"] == emp_id:
                row["name"] = input("Enter new Name: ").strip()
                row["department"] = input("Enter new Department: ").strip()
                row["salary"] = input("Enter new Salary: ").strip()
                found = True
                break
        if found:
            self._write_all(rows)
            print("Record updated successfully!")
        else:
            print("Employee ID not found.")

    def delete_employee(self):
        emp_id = input("Enter ID to delete: ").strip()
        rows = self._read_all()
        remaining = [row for row in rows if row["id"] != emp_id]
        if len(remaining) == len(rows):
            print("Employee ID not found.")
        else:
            self._write_all(remaining)
            print("Record deleted successfully!")


def main():
    emp = Employee()
    while True:
        print("\n--- EMPLOYEE MANAGEMENT SYSTEM ---")
        print("1. Add Employee")
        print("2. Display Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            emp.add_employee()
        elif choice == "2":
            emp.display_employee()
        elif choice == "3":
            emp.search_employee()
        elif choice == "4":
            emp.update_employee()
        elif choice == "5":
            emp.delete_employee()
        elif choice == "6":
            print("Program ended")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
