import sqlite3


class Employee:
    def __init__(self, db_name="employee.db"):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL
            )
        """)
        self.con.commit()

    def add(self):
        try:
            emp_id = int(input("Enter employee id: ").strip())
            name = input("Enter name: ").strip()
            department = input("Enter department: ").strip()
            salary = float(input("Enter salary: ").strip())

            self.cur.execute(
                "INSERT INTO employee (id, name, department, salary) VALUES (?, ?, ?, ?)",
                (emp_id, name, department, salary),
            )
            self.con.commit()
            print("Employee added successfully")
        except ValueError:
            print("Please enter valid numeric values.")
        except sqlite3.IntegrityError:
            print("Employee ID already exists.")

    def display(self):
        self.cur.execute("SELECT * FROM employee")
        rows = self.cur.fetchall()
        if not rows:
            print("No records found")
            return
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Department: {row[2]} | Salary: {row[3]}")

    def update(self):
        try:
            emp_id = int(input("Enter employee id to update: ").strip())
            name = input("Enter new name: ").strip()
            department = input("Enter new department: ").strip()
            salary = float(input("Enter new salary: ").strip())

            self.cur.execute(
                """
                UPDATE employee
                SET name = ?, department = ?, salary = ?
                WHERE id = ?
                """,
                (name, department, salary, emp_id),
            )
            self.con.commit()

            if self.cur.rowcount > 0:
                print("Employee updated successfully")
            else:
                print("Employee not found")
        except ValueError:
            print("Please enter valid numeric values.")

    def delete(self):
        try:
            emp_id = int(input("Enter employee id to delete: ").strip())
            self.cur.execute("DELETE FROM employee WHERE id = ?", (emp_id,))
            self.con.commit()

            if self.cur.rowcount > 0:
                print("Employee deleted successfully")
            else:
                print("Employee not found")
        except ValueError:
            print("Please enter a valid employee ID.")

    def close(self):
        self.con.close()


def main():
    emp = Employee()
    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Display Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            emp.add()
        elif choice == "2":
            emp.display()
        elif choice == "3":
            emp.update()
        elif choice == "4":
            emp.delete()
        elif choice == "5":
            emp.close()
            print("Program ended")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
