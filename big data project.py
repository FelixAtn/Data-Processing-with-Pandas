#!/usr/bin/env python
# coding: utf-8

# In[355]:


import pandas as PandaLib
from enum import Enum

# Felix Atanasescu - HE20830




# 1. For the first step I will create an enum class in order to keep track of my 
# loaded files with ease, as I am planning to add the files in a map container, and the IDs will 
# act as the key for each file.  

class FileType(Enum):
    BOOKS = 'books'
    LISTINGS = 'listings'
    PHONE_DATA = 'phone_data'
    OLYMPICS = 'tolympics' 

dataFrame = {
    FileType.BOOKS: PandaLib.read_csv('books.csv'),
    FileType.LISTINGS: PandaLib.read_csv('listings.csv'),
    FileType.PHONE_DATA: PandaLib.read_csv('phone_data.csv'),
    FileType.OLYMPICS: PandaLib.read_csv('tolympics.csv') # broken header, so I will not load it
}

# For utility I will create a print function and declare some strings,to print text. 
# Having to repeat the text over and over is unnecessary.

def LogMessage(message):
    print("[INFO] " + message + "\n")

def LogFileReading(fileTypeID):
    fileReadBegins = f"READING FROM THE FILE----------- {fileTypeID.value} ------------ \n"
    print("[INFO]: " + fileReadBegins)

def LogFileEndReading(fileTypeID):
    fileReadEnds = f"ENDING READING FOR THE FILE ----------- {fileTypeID.value} ------------ \n"
    print("[INFO]: " + fileReadEnds)
# Done 


# In[164]:


# 2.
for fileTypeID, someData in dataFrame.items():
    LogFileReading(fileTypeID)
    
    print("First 10 rows:")
    print(someData.head(10)) 

    print("\nLast 10 rows:")  
    print(someData.tail(10))  
    LogFileEndReading(fileTypeID)
# Done


# In[166]:


# 3. For the thrid step, I wll crate a simple array of strings for each file that will
# represent 3 columns each.
books_columns_to_show = ['Title', 'Author', 'Place of Publication'] 
listings_columns_to_show = ['room_type', 'price', 'availability_365']  
phone_data_columns_to_show = ['index', 'network', 'network_type'] 
olympics_columns_to_show = ['1', '2', '3']

# Once that done, I will iterate through the map and print the details of the columns.
# Since it is a map of files, each file has an ID,
# so in order to print the desired columns data for each file
# I will have to use conditions 
# Explanation: if the n0 file is currently iterated, "print the data of this file",
# else if n1 is currently iterated, "print the data of n1 file", etc.

for fileTypeID, data in dataFrame.items():
    LogFileReading(fileTypeID)
    
    if fileTypeID == FileType.BOOKS:
        print(data[books_columns_to_show]) 
             
    elif fileTypeID == FileType.LISTINGS:
        print(data[listings_columns_to_show]) 
              
    elif fileTypeID == FileType.PHONE_DATA:
        print(data[phone_data_columns_to_show])
              
    elif fileTypeID == FileType.OLYMPICS:
        print(data[olympics_columns_to_show])

    LogFileEndReading(fileTypeID)
# Done


# In[170]:


# Step 4. Next I will add a new column to each dataFrame that I previously 
# loaded. The new name "The_New_Frame_Column" and it can have any desired value.
# The steps from above will need to be repeated since there are separate exercises, otherwise, 
# I could have fit this step and the previous one into a single one, simplyfing the work by reducing 
# it to one iterator and conditional check, but for the sake of separation of concerns, and exercise 
# requirements, I will do it in a new cell. ^_^

columnName = "The_New_Column"
columnValue = 0

for fileTypeID, data in dataFrame.items():
    LogFileReading(fileTypeID)

    columnValue += 1
    
    if fileTypeID == FileType.BOOKS:
        data[columnName] = columnValue
        
    elif fileTypeID == FileType.LISTINGS:
        data[columnName] = columnValue

    elif fileTypeID == FileType.PHONE_DATA:
        data[columnName] = columnValue
    
    elif fileTypeID == FileType.OLYMPICS:
        data[columnName] = columnValue
        
    print("The new column added:")    
    print(data.head())
    LogFileEndReading(fileTypeID) 
#Done 


# In[224]:


# Step 5: For this step, I will choose a specific column for each data frame to
# calculate their average values. 
# To do so, I will create a new map for each file pointing to the chosen column.

average_column = {
    FileType.BOOKS: 'Identifier',
    FileType.LISTINGS: 'price',
    FileType.PHONE_DATA: 'duration',
    FileType.OLYMPICS: '5'
}

for fileTypeID, someData in dataFrame.items():
    LogFileReading(fileTypeID)
    
    # Need to write a safety guard to check if the column exists,
    # otherwise runtime errors / undefined behaviours might occur.
    # Since it can only be eiter true or false, I will do 
    # a negation instead of a straight forward if else, a good practice standard
    # which will reduce the amount of written code, and therefore -> more readable 
    
    if average_column[fileTypeID] not in someData.columns: 
        LogMessage(f"Column '{average_column[fileTypeID]}' not found in {fileTypeID.value}.")
        continue  # Skip to the next iteration if the column is not found.

    someData[average_column[fileTypeID]] = PandaLib.to_numeric(someData[average_column[fileTypeID]], errors='coerce')
    average_value = someData[average_column[fileTypeID]].mean()
    LogMessage(f"The average of {average_column[fileTypeID]} in {fileTypeID.value}: {average_value:.2f}")

# Errors:
#  1. The safety guards were indeed useful, the output has shown that some of the columns don't existt.
#     why: case sensitive 
#     what I did: I had to double-check the column cases and correct in the map where needed. 

#  2. Due to the fact that the rows are numbered manually and under them there are strings,
#     I converted the string value to a numeric value. this might lead to some loss of accuracy, 
#     but for now should be fine.

# done


# In[284]:


# Step 6: For this step, I will display only the rows where the value 
# in any column is greater than 90.
# So I will start by iterating the map once more

filterinValue = 90 # no idea how to actually declare a const in python xD

for fileTypeID, someData in dataFrame.items():
    LogFileReading(fileTypeID)
    
    # I convert all values that are not valid(strings, chars, etc) to numerics, 
    # avoiding the errors from step 5. ("Fool me once... No more string calculation errors (-_-)")
    
    someData = someData.apply(PandaLib.to_numeric, errors='coerce')
    
    # Filter rows where any column has a value greater than filteringValue
    dataFilter = someData[someData > filteringValue].dropna(how='all')

    # Beautify the output by replacing the "NaN" with an empty space
    dataFilter = dataFilter.fillna(" ")
    
    LogMessage("Rows where any value is above 90: ")
    LogMessage(dataFilter.to_string())
    LogFileEndReading(fileTypeID)
    


# In[317]:


# Step 7. For this step, I will check if there are any missing values 
# in the rows of each DataFrame. 
# - If any missing values are found, I will fill them with the character "M"

for fileTypeID, someData in dataFrame.items():
    LogFileReading(fileTypeID)

    # Debugging - Logging the current data frame content for verification
    
    # Check for !null 
    if not someData.isnull().values.any():
        LogMessage("No missing values found within Data")
        continue
        
    # If missing values are found
    LogMessage("Missing values have been found! Filling with 'M': ")

    # but first we need type conversion to string.
    someData = someData.astype(str)
    someData.fillna("M", inplace=True)
        
    # Log the modified DataFrame
    LogMessage(f"Updated data for {fileTypeID} after filling NaNs:")
    LogMessage(someData.to_string())
 
# BUG: "??? No missing values found ???". 
# Potential logic error in my approach or misunderstood 
# the problem context - To fix later.

# Done (not quite)


# In[347]:


# Step 8. For this step, I will sort a specified column in 
# each DataFrame in ascending order.

book_column = 'Identifier'
phone_column = 'duration'
listing_column = 'price'
olympics_column = '5'

for fileTypeID, someData in dataFrame.items():
    LogFileReading(fileTypeID)

    if fileTypeID == FileType.BOOKS:
        sortedData = someData.sort_values(by=book_column, ascending=True)
        LogMessage(f"Sorted data for {fileTypeID} by column '{book_column}' in ascending order:")
             
    elif fileTypeID == FileType.LISTINGS:
        sortedData = someData.sort_values(by=listing_column, ascending=True)
        LogMessage(f"Sorted data for {fileTypeID} by column '{listing_column}' in ascending order:")
              
    elif fileTypeID == FileType.PHONE_DATA:
        sortedData = someData.sort_values(by=phone_column, ascending=True)
        LogMessage(f"Sorted data for {fileTypeID} by column '{phone_column}' in ascending order:")
              
    elif fileTypeID == FileType.OLYMPICS:
        sortedData = someData.sort_values(by=olympics_column, ascending=True)
        LogMessage(f"Sorted data for {fileTypeID} by column '{olympics_column}' in ascending order:")

# Done


# In[359]:


# Step 9. Exporting to csv

for fileTypeID, someData in dataFrame.items():
    modified_filename = f"modified_{fileTypeID}.csv"
    
    someData.to_csv(modified_filename, index=False)
    LogMessage(f"Exported modified data to {modified_filename}")

#Done


# In[ ]:




