import pandas as pd
import openpyxl

a = list(5 for i in range(25))
data_frame = pd.DataFrame({"Phone Number": "880", "ID": "125", "First Name": "",
                           "Last Name": "", "Class": a})
print(data_frame.head())

for i in range(25):
    x = input("Enter first name: ")
    data_frame.iloc[i, 2] += x.title()
    y = input("Enter last name: ")
    data_frame.iloc[i, 3] += y.title()
    if (len(x)+ len(y)) == 0:
        ask = input("End of entries? \n")
        if ask.lower() == 'y':
            break
    z = input("Enter phone number: ")
    while len(z) != 10:
        z = input("Error\nRe-enter phone number: ")
    data_frame.iloc[i, 0] += z
    dig = input("Enter last 3 digits of ID: ")
    while len(dig) != 3:
        dig = input("Error\n Re-Enter Last 3 digits: ")
    data_frame.iloc[i, 1] += dig

    print("Entry done\n")

print(data_frame.head)

data_frame.to_excel("Class 5.xlsx")
