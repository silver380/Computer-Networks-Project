import random
import csv


def id_generator():
    id = ""
    for j in range(10):
        id += str(random.randint(0,9))
    return id


First_name = ['Reza', 'Ali', 'Mohammad', 'Jack', 'James', 'Till', "Hashem", "Ehsan", "Master", "Chief", "Kamal"]
Last_name = ['Rastegari', 'Balochi', 'Mohebi', 'Jafari', "Sharbaaf", "Hami", "Jalali", "Mahi"]
Lessons = ["Computer Networks", "Signals and Systems", "Databases", "Calculus", "Operating Systems"]
Used_ID = []
final_info = []
number_of_persons = int(input("how many people would you like to have? "))
file_name = input("Write a name to save your file using it ")

for i in range(number_of_persons):
    info = {}
    fname = First_name[random.randint(0, len(First_name)-1)] +' '+First_name[random.randint(0, len(First_name)-1)]
    lname = Last_name[random.randint(0, len(Last_name)-1)]
    ID = ""
    while True:
        ID = id_generator()
        if ID not in Used_ID:
            Used_ID.append(ID)
            break

    Second_ID = ID
    info = {'ID': ID, 'Second_ID': Second_ID, 'First_name': fname, 'Last_Name': lname,
            'Computer Networks': random.randint(0, 20), "Signals and Systems": random.randint(0, 20),
            'Databases': random.randint(0, 20), 'Calculus': random.randint(0, 20),
            'Operating Systems': random.randint(0, 20)}

    final_info.append(info)

csv_file = f"./Client_CSVs/{file_name}.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(final_info[0].keys()))
        writer.writeheader()
        for data in final_info:
            writer.writerow(data)
except IOError:
    print("I/O error")
