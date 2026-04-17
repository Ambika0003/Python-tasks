import numpy as np
#Student Score Processor 
#A teacher stores student names and marks in a list of tuples.
Student=[("Ravi",90),("John",40),("Ash",75),("Ambi",85),("Sas",50)]

#Convert data into a dictionary 
dict_stud=dict(Student)
print(dict_stud)

#Use a loop + condition to find students scoring above 50 
for names,marks in dict_stud.items():
    if marks>50:
        print(names,marks)

#Use math module to calculate average 
avg=np.mean((list(dict_stud.values())))
print(avg)

#Store results in a text file 
with open("student_results.txt","w") as file:
    file.write("Students scoring above 50:\n")
    
    for names, marks in dict_stud.items():
        file.write(f"{names}: {marks}\n")
    
    file.write(f"\nAverage Marks: {avg}")
