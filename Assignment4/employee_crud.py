import os
import sqlite3
import pandas as pd


class EmployeeManager:
    def __init__(self, db_name="employee.db", table_name="employee", csv_backup="employee.csv"):
        self.db_name = db_name
        self.table_name = table_name
        self.csv_backup = csv_backup
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        conn = self._connect()
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _sync_csv(self, df):
        if self.csv_backup:
            df.to_csv(self.csv_backup, index=False)

    def add(self):
        try:
            emp_id = int(input("Enter employee id: ").strip())
            name = input("Enter name: ").strip()
            department = input("Enter department: ").strip()
            salary = float(input("Enter salary: ").strip())

            row_df = pd.DataFrame(
                [[emp_id, name, department, salary]],
                columns=["id", "name", "department", "salary"]
            )

            conn = self._connect()
            row_df.to_sql(self.table_name, conn, if_exists="append", index=False)
            full_df = pd.read_sql(f"SELECT * FROM {self.table_name}", conn)
            conn.close()

            self._sync_csv(full_df)
            print("Employee added successfully")
        except ValueError:
            print("Please enter valid numeric values.")
        except sqlite3.IntegrityError:
            print("Employee ID already exists.")
        except Exception as e:
            print("Error:", e)

    def display(self):
        try:
            conn = self._connect()
            df = pd.read_sql(f"SELECT * FROM {self.table_name}", conn)
            conn.close()

            if df.empty:
                print("No records found")
            else:
                print(df.to_string(index=False))
        except Exception as e:
            print("Error:", e)

    def update(self):
        try:
            emp_id = int(input("Enter employee id: ").strip())
            conn = self._connect()
            existing = pd.read_sql(
                f"SELECT * FROM {self.table_name} WHERE id = ?",
                conn,
                params=(emp_id,)
            )

            if existing.empty:
                print("Employee not found")
                conn.close()
                return

            name = input("Enter new name: ").strip()
            department = input("Enter new department: ").strip()
            salary = float(input("Enter new salary: ").strip())

            conn.execute(
                f"""
                UPDATE {self.table_name}
                SET name = ?, department = ?, salary = ?
                WHERE id = ?
                """,
                (name, department, salary, emp_id)
            )
            conn.commit()
            full_df = pd.read_sql(f"SELECT * FROM {self.table_name}", conn)
            conn.close()

            self._sync_csv(full_df)
            print("Employee updated successfully")
        except ValueError:
            print("Please enter valid numeric values.")
        except Exception as e:
            print("Error:", e)

    def delete(self):
        try:
            emp_id = int(input("Enter employee id: ").strip())
            conn = self._connect()
            existing = pd.read_sql(
                f"SELECT * FROM {self.table_name} WHERE id = ?",
                conn,
                params=(emp_id,)
            )

            if existing.empty:
                print("Employee not found")
                conn.close()
                return

            conn.execute(
                f"DELETE FROM {self.table_name} WHERE id = ?",
                (emp_id,)
            )
            conn.commit()
            full_df = pd.read_sql(f"SELECT * FROM {self.table_name}", conn)
            conn.close()

            self._sync_csv(full_df)
            print("Employee deleted successfully")
        except ValueError:
            print("Please enter a valid employee ID.")
        except Exception as e:
            print("Error:", e)


def main():
    manager = EmployeeManager()
    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Display Employee")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            manager.add()
        elif choice == "2":
            manager.display()
        elif choice == "3":
            manager.update()
        elif choice == "4":
            manager.delete()
        elif choice == "5":
            print("Program ended")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
