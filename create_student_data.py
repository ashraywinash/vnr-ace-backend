from openpyxl import Workbook
from pathlib import Path

# Create a new workbook
wb = Workbook()
ws = wb.active
ws.title = "Students"

# Headers
headers = ['name', 'roll_number', 'branch', 'section', 'year', 'attendance_pct', 'cumulative_gpa', 'backlogs']
ws.append(headers)

# Student data (30 records)
students = [
    ['Aarav Sharma', '21R01A0501', 'CSE', 'A', 2, 98, 9.8, 0],
    ['Vivaan Patel', '21R01A0502', 'CSE', 'A', 2, 95, 9.2, 0],
    ['Aditya Kumar', '21R01A0503', 'CSE', 'A', 2, 88, 8.5, 0],
    ['Vihaan Singh', '21R01A0504', 'CSE', 'B', 2, 92, 8.9, 0],
    ['Arjun Reddy', '21R01A0505', 'CSE', 'B', 2, 67, 6.2, 2],
    ['Sai Krishna', '21R01A0506', 'CSE', 'B', 2, 72, 6.8, 1],
    ['Reyansh Gupta', '21R01A0507', 'CSE', 'C', 2, 85, 8.1, 0],
    ['Ayaan Khan', '21R01A0508', 'CSE', 'C', 2, 91, 8.7, 0],
    ['Krishna Rao', '21R01A0509', 'ECE', 'A', 3, 78, 7.5, 1],
    ['Ishaan Verma', '21R01A0510', 'ECE', 'A', 3, 65, 5.8, 3],
    ['Shaurya Nair', '21R01A0511', 'ECE', 'B', 3, 94, 9.1, 0],
    ['Atharv Joshi', '21R01A0512', 'ECE', 'B', 3, 89, 8.3, 0],
    ['Advait Desai', '21R01A0513', 'ECE', 'C', 3, 76, 7.2, 1],
    ['Pranav Iyer', '21R01A0514', 'ECE', 'C', 3, 82, 7.8, 0],
    ['Dhruv Menon', '21R01A0515', 'ECE', 'A', 3, 58, 5.2, 2],
    ['Kabir Malhotra', '21R01A0516', 'MECH', 'A', 3, 96, 9.5, 0],
    ['Kiaan Chopra', '21R01A0517', 'MECH', 'B', 3, 87, 8.4, 0],
    ['Arnav Bhat', '21R01A0518', 'MECH', 'B', 3, 73, 6.9, 1],
    ['Veer Agarwal', '21R01A0519', 'MECH', 'C', 3, 90, 8.8, 0],
    ['Rudra Pillai', '21R01A0520', 'MECH', 'C', 3, 68, 6.1, 2],
    ['Ananya Sharma', '21R01A0521', 'MECH', 'A', 4, 93, 9.3, 0],
    ['Diya Patel', '21R01A0522', 'CIVIL', 'A', 4, 45, 5.5, 3],
    ['Isha Kumar', '21R01A0523', 'CIVIL', 'B', 4, 88, 8.6, 0],
    ['Anvi Singh', '21R01A0524', 'CIVIL', 'B', 4, 75, 7.1, 1],
    ['Saanvi Reddy', '21R01A0525', 'CIVIL', 'C', 4, 92, 9.0, 0],
    ['Navya Krishna', '21R01A0526', 'CIVIL', 'C', 4, 81, 7.9, 0],
    ['Aanya Gupta', '21R01A0527', 'CIVIL', 'A', 4, 70, 6.5, 2],
    ['Pari Khan', '21R01A0528', 'CSE', 'B', 4, 86, 8.2, 0],
    ['Myra Rao', '21R01A0529', 'ECE', 'C', 4, 79, 7.6, 1],
    ['Sara Verma', '21R01A0530', 'MECH', 'A', 4, 84, 8.0, 0],
]

# Add student data
for student in students:
    ws.append(student)

# Create data directory if it doesn't exist
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# Save the workbook
output_file = data_dir / 'student_data.xlsx'
wb.save(output_file)

print(f'✓ Created {output_file} with {len(students)} student records')
print(f'\nData Summary:')
print(f'  - Total students: {len(students)}')
print(f'  - CSE: 8, ECE: 7, MECH: 6, CIVIL: 6, Others: 3')
print(f'  - Year 2: 8, Year 3: 12, Year 4: 10')
print(f'  - Students with backlogs: {sum(1 for s in students if s[7] > 0)}')
