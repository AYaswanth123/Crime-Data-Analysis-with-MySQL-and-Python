
# CRIME DATA ANALYSIS

# Database Connection
import pymysql
conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Yaswanth@789",
    db = "crime_data"
)

# checking server is connect or not
print("checking the connection")
print(conn)

# Data Exploration

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


query = "select * from crime_info"
df = pd.read_sql(query,conn)
print(df)

print("Information of the given data:-")
print(df.info()) # information of database
print("\n")

# Retriving basic statistics on the dataset, such as the total number of records
print("Total records in the given database:-")
print(df.shape)  # for the records
print("\n")
# Unique values in specific columns
df1 = pd.DataFrame(df) # dataframe
unique_values = df1["Crm_Cd"].unique()
print("unique values from crime code column:-")
print(unique_values) # for uniqe values
print("\n")

unique_values_of_Desc = df1["Crm_Cd_Desc"].unique()
print("unique values from crime code description column:-")
print(unique_values_of_Desc) # uniqe values for description
print("\n")

# Identify the distinct crime codes and their descriptions
print("distinct crime codes and their descriptions")
df2 = pd.DataFrame(data=unique_values_of_Desc,index=unique_values,columns=["description"])
print(df2)
print("\n")


# Temporal Analysis

# Determine trends columns in crime occurrence over time
#convert date columns to datetime objectives
df['Date_Rptd'] = pd.to_datetime(df['Date_Rptd'])
df['DATE_OCC'] = pd.to_datetime(df['DATE_OCC'])
# Aggregate by mounth
monthly_crime = df.resample('M', on='Date_Rptd').size()
#plot the trend
# usiing matplot lib

plt.figure(figsize=(10,6))  # Use plt.figure() instead of plt.Figure()
plt.plot(monthly_crime.index, monthly_crime.values, marker='H', color='#54B435')
plt.title('Crime occurrence over time')
plt.xlabel('Month')
plt.ylabel('Number of Crimes')  # Added y-axis label
plt.grid(True)  # Added grid
plt.show()

# Spatial Analysis

# Utilize the geographical information(Latitude and Longitude) to perform spatial analysis
# usiing matplot lib

plt.figure(figsize=(10,8))
plt.scatter(df['LON'], df['LAT'], s=15, alpha=0.5, c='blue')
plt.title('Crime occurrences')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()

# using plotyl.express
# create a scatter plot
fig = px.scatter(df, x='LON', y='LAT',title='Crime occurrences(spatial)')
fig.show()

# Visualize crime hotspots on a map
# Importing python folium library for creating interactive maps
import folium

# creating a folium map centered around the average latitude and longitude of crime date
crime_map = folium.Map(location=[df['LAT'].mean(),df['LON'].mean()],zoom_start=10)
# adding crime markers to the map
for index, row in df.iterrows():
    popup=folium.Popup(f"Type:{row['Crm_Cd_Desc']}, Location:{row['Location']},Date:{row['DATE_OCC']}",parse_html=True)
# Add a marker for each crime with popup message
    folium.Marker(location=[row['LAT'],row['LON']],popup=popup).add_to(crime_map)
#display(crime_map)
crime_map.save("crime_map.html")

# Victim Demographics

# Investigate the distribution of victim ages and genders
# plot distribution of victim ages

plt.figure(figsize=(10,6))
sns.histplot(df['Vict_Age'], color='#FF6000',edgecolor='black')
plt.title('Distribution of victim ages')
plt.xlabel('Age')
plt.ylabel('Frequency')  # Added y-axis label
plt.grid(True)  # Added grid
plt.show()

# plot distribution of victim genders

plt.figure(figsize=(6,6))
sns.countplot(x=df['Vict_Sex'], palette=['#5356FF','#201658','#0D9276'],edgecolor='black')
plt.title('Distribution of victim gender')
plt.xlabel('Gender')
plt.ylabel('Count')  # Added y-axis label
plt.grid(True)  # Added grid
plt.show()

# Identify common premises descriptions where crimes occur
# Get the premisses descriptions

premise = df['Premis_Desc']
count_of_premises=premise.value_counts()
print(count_of_premises)
print('\n')
# Examine the status of reported crimes

# Status Analysis
crime = df['Status']
status_counts = crime.value_counts()
print(status_counts)

# Creating a pie chart

plt.figure(figsize=(6,6))
plt.pie(status_counts,labels=status_counts.index, autopct='1%.1f%%', startangle=140)
plt.title('status of reported crimes')
# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')
plt.show()

''' Qutiones '''

'''Spatial Analysis:

1) Where are the geographical hotspots for reported crimes?
Ans:-
From the analysis of the hotspot map for crimes,
I have concluded that Los Angeles is the hostspot country where most crimes have happened.'''


'''  Victim Demographics:

2) What is the distribution of victim ages in reported crimes?
Ans:-
1.From the analysis of Histogram,
In our dataset there are zero values in the age column where we can see that most of the 
crime happend in that age group of 0 to 5.
The frequency of that age group is above 90 

2.The age group of 23 to 35 the crime frequency is above 50

3. Some of the crimes has frequency less than 40 and the age group for those crimes 
are (6-11) and (36-80)

3) Is there a significant difference in crime rates between male and female victims?
Ans:-
yes there is significant diffrence in male and female crime rates.
Males crime rates is more than 250.
The female have the crime rates is about 150.
the x victimes has crime rates less than 50.'''


''' Location Analysis:

4)Where do most crimes occur based on the "Location" column?'''
#Ans:-
location_counts = df['Location'].value_counts()
#print the top 5 most frequent locations
print("Top 5 locations where crimes occur:-")
print(location_counts.head())



# Crime Code Analysis:

# 5) What is the distribution of reported crimes based on Crime Code?
#Ans:-

# get the premises descriptions
code=df['Crm_Cd']
count_of_codes=code.value_counts()
print(count_of_codes)
# Visualize the distribution of crime statuses
plt.figure(figsize=(9,7))
count_of_codes.plot(kind='bar', color='skyblue')
plt.title('Distribution of reported crime code')
plt.xlabel('code')
plt.ylabel('Number of crimes')
plt.show()

# Conclusion
'''From above analysis i  came to a conclusion that the crime code 330 has the most occurance
which is more than 82.
The crime code 624 has occured more than 74.'''


