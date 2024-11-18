import pandas as pd
from random import randint
import os

# Reads all .csv files in the working directory and merges them into a single main.csv
# All CSVs are space-separated
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')]
df = pd.concat([pd.read_csv(f, sep=' ') for f in files])
df.to_csv('main.csv', sep=' ', index=False)

# Makes 3 new DataFrames: training, validation, and test
# Each DataFrame gets 75% training, 12.5% validation, and 12.5% test
training = []
validation = []
test = []

# Loop through the rows of the DataFrame
for i in range(len(df)):
    rand_num = randint(1, 8)  # Generate a random number between 1 and 8
    if rand_num <= 6:  # 6 out of 8 chance (75%)
        training.append(df.iloc[i])
    elif rand_num == 7:  # 1 out of 8 chance (12.5%)
        validation.append(df.iloc[i])
    else:  # 1 out of 8 chance (12.5%)
        test.append(df.iloc[i])

# Convert the lists back into DataFrames
training_df = pd.DataFrame(training)
validation_df = pd.DataFrame(validation)
test_df = pd.DataFrame(test)

# Save the DataFrames to separate files
training_df.to_csv('training.csv', sep=' ', index=False)
validation_df.to_csv('validation.csv', sep=' ', index=False)
test_df.to_csv('test.csv', sep=' ', index=False)
