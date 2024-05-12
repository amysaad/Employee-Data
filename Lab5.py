import sqlite3
import csv

connection = sqlite3.connect("HR.db")

cursor = connection.cursor()

# Step 2: Make new table for current employees

cursor.execute("""
CREATE TABLE IF NOT EXISTS current_employees (
id INTEGER PRIMARY KEY,
name TEXT,
email TEXT UNIQUE,
current_title TEXT,
current_salary INTEGER,
recommended_for_bonus INTEGER
)""") 


connection.commit()

# Step 3: Add data
# with open('current_employees.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)  
#
#     for row in csv_reader:
#         id, name, email, current_title, current_salary, recommended_for_bonus = row
#         cursor.execute("""
#         INSERT INTO current_employees (id, name, email, current_title, current_salary, recommended_for_bonus)
#         VALUES (?, ?, ?, ?, ?, ?)
#         """, (id, name, email, current_title, current_salary, recommended_for_bonus))
#
# connection.commit()

# Step 4: Make new table for former employees

cursor.execute("""
CREATE TABLE IF NOT EXISTS former_employees (
id INTEGER,
name TEXT,
email TEXT UNIQUE,
former_title TEXT,
former_salary INTEGER,
FOREIGN KEY(id) REFERENCES current_employees (id)
)""")

connection.commit()

# Step 5: Add data
# with open('former_employees.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)  
#
#     for row in csv_reader:
#         id, name, email, former_title, former_salary = row
#         cursor.execute("""
#         INSERT INTO former_employees (id, name, email, former_title, former_salary)
#         VALUES (?, ?, ?, ?, ?)
#         """, (id, name, email, former_title, former_salary))
#
# connection.commit()

# Step 6: Make new table for employee bonus

cursor.execute("""
CREATE TABLE IF NOT EXISTS employee_bonus_2024 (
id INTEGER,
name TEXT,
email TEXT UNIQUE,
bonus REAL,
FOREIGN KEY(id) REFERENCES current_employees (id)
)""")

connection.commit()

# Step 7: Add data 
# employee_data = cursor.execute("""
# SELECT id, name, email, current_salary
# FROM current_employees
# WHERE recommended_for_bonus = 1
# """)
# employee_data = employee_data.fetchall()
# bonus_people = []
# for current_employee in employee_data:
#     
#     employee_id = current_employee[0]
#     name = current_employee[1]
#     email = current_employee[2]
#     bonus = current_employee[3] * 0.05  # bonus = (salary * 5%)
#     
#     employee = (employee_id, name, email, bonus)
#     bonus_people.append(employee)
#
# cursor.executemany("INSERT INTO employee_bonus_2024 VALUES (?,?,?,?)", bonus_people)
# connection.commit()

# Step 8: Bob's name update

cursor.execute("""
UPDATE current_employees
SET name = 'Robert'
WHERE name = 'Bob'
""")
cursor.execute("""
UPDATE former_employees
SET name = 'Robert'
WHERE name = 'Bob'
""")

connection.commit()

# Step 9: Jamies status update
# cursor.execute("""
# INSERT INTO former_employees (id, name, email, former_title, former_salary)
# VALUES (10007, 'Jamie', 'jamie@example.com', 'Junior Developer', 50000)
# """)
# cursor.execute("""
# DELETE FROM current_employees
# WHERE id = 10007
# """)
#
# connection.commit()

# Step 10: Keep track of former employees

# cursor.execute("""ALTER TABLE former_employees
# ADD terms_of_termination TEXT
# DEFAULT 'N/A'""")
# connection.commit()

# Step 11: Update Jamie's termination

cursor.execute("""
UPDATE former_employees
SET terms_of_termination = 'Good'
WHERE id = 10007
""")
connection.commit()

# Step 12: Which current employees are former employees

both = cursor.execute("""
SELECT current_employees.name, current_employees.current_title,
former_employees.former_title
FROM current_employees
INNER JOIN former_employees
ON current_employees.id = former_employees.id
""")
both = both.fetchall()

print("\nCurrent employees who were once former employees: ")
for row in both:
    for datum in row:
        print(datum, end="\t ")
    print()

# Step 13: Top 3 salary earners

top_3 = cursor.execute("""
SELECT name, current_salary
FROM current_employees
ORDER BY current_salary DESC
LIMIT 3
""")
top_3 = top_3.fetchall()
print("\nTop 3 earners: ")
for row in top_3:
    print(row[0], row[1])

# Step 14: Max, min, and average salary

salary_stats = cursor.execute("""
SELECT MAX(current_salary), MIN(current_salary), AVG(current_salary)
FROM current_employees
""")
salary_stats = salary_stats.fetchone()
average_salary = "{:.2f}".format(salary_stats[2])
print("\nMaximum salary:", salary_stats[0])
print("Minimum salary:", salary_stats[1])
print("Average salary:", average_salary)

# Step 15: Printing sum total

total_bonus = cursor.execute("""
SELECT SUM(bonus)
FROM employee_bonus_2024
""")
total_bonus = total_bonus.fetchone()[0]
print("\nTotal amount of bonuses to be paid in 2024:", total_bonus)

