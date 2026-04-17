class Employee:
    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary

    def display(self):
        return f"ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}"


employees = {}

while True:
    try:
        emp_id = input("Enter Employee ID (or type 'exit'): ")

        if emp_id.lower() == "exit":
            break

        name = input("Enter Employee Name: ")

        # Exception handling for salary input
        salary = float(input("Enter Salary: "))

        if salary < 0:
            raise ValueError("Salary cannot be negative")

        # Store in dictionary
        emp = Employee(emp_id, name, salary)
        employees[emp_id] = emp

        print("Employee added successfully.\n")

    except ValueError as e:
        print("Invalid input:", e)

# Display all employees using loop
print("\n--- Employee List ---")
for emp in employees.values():
    print(emp.display())

# Save to file
try:
    with open("employees.txt", "w") as file:
        file.write("--- Employee Data ---\n")
        for emp in employees.values():
            file.write(emp.display() + "\n")

    print("\nData saved to file successfully.")

except Exception as e:
    print("File error:", e)
