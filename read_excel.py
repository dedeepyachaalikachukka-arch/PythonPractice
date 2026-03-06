# read excel data and then write it to another excel

import pandas as pd

file_name = input("Enter the Excel file name (Example: input.xlsx): ")

sheets = pd.read_excel(file_name, sheet_name=None)

sheet_names = list(sheets.keys())
total_sheets = len(sheet_names)

print("This file contains", total_sheets, "sheets.")

choice = input("Enter sheet numbers to copy (Example: 1,2,3) or type ALL: ")

with pd.ExcelWriter("output.xlsx") as writer:

    if choice.upper() == "ALL":
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)
    
    else:
        numbers = [int(x.strip()) for x in choice.split(",")]

        if max(numbers) > total_sheets:
            print("Error: Wrong sheet number entered.")
            exit()

        for n in numbers:
            sheet_name = sheet_names[n-1]
            sheets[sheet_name].to_excel(writer, sheet_name=sheet_name,index=False)

print ("Sheets copied successfully! Reveal the output file in finder")            