import numpy as np
import pandas as pd
import math
class Student:
    def __init__(self, student_id, marks):
        self.student_id = student_id
        self.marks = marks
        self.grade = self.assign_grade()
    def assign_grade(self):
        try:
            if self.marks >= 90: return 'A'
            elif self.marks >= 75: return 'B'
            elif self.marks >= 50: return 'C'
            else: return 'F'
        except TypeError:
            return 'Error'
num_students = 10
random_marks = np.random.randint(30, 101, size=num_students)
student_ids = [f"S{100+i}" for i in range(num_students)]
student_objects = [Student(student_ids[i], random_marks[i]) for i in range(num_students)]
data = {
    'Student_ID': [s.student_id for s in student_objects],
    'Marks': [s.marks for s in student_objects],
    'Grade': [s.grade for s in student_objects]
}
df = pd.DataFrame(data)
mean_marks = np.mean(df['Marks'])
std_dev = np.std(df['Marks'])
report_filename = 'exam_report.csv'
df.to_csv(report_filename, index=False)
print(f"Simulation Complete. Report saved to {report_filename}")
print(f"Average Class Marks: {mean_marks:.2f}")
print(df)
 