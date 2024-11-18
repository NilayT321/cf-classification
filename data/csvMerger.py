import os 
import csv 

# Get all csv files in the directory
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')]
print(len(files))

with open("mainData/main.csv", "w", encoding = "utf-8", newline = '') as outfile:
    main_writer = csv.writer(outfile, delimiter = " ")

    # For each file in the files array 
    # Open a new reader for it 
    # Concatenate the rows in to the main.csv file 
    for file in files:
        with open(file, "r", encoding = "utf-8", newline = '') as infile:
            infile_reader = csv.reader(infile, delimiter = " ") 

            print(f"Writing {file}. There are {len(list(infile_reader))} rows to be written")
            for row in infile_reader:
                main_writer.writerow(row)
    