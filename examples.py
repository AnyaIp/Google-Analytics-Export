from codes.query import *

# Authentication
# Define the path to the key file and the view id
key_file_location = 'xxxxxxxxx.json'
view_id = '123456789'
auth = gaAuth(key_file_location, view_id)

### Example 1: Get the number of users and sessions by country (7 days ago - present)
# Build your query
ga = gaQuery(
    auth=auth,
    metrics=['ga:users', 'ga:sessions'],
    dimensions=['ga:country'],
    startDate='7daysAgo',
    endDate='today'
)
# save the outputs as a Pandas DataFrame
df = ga.retrieve_data()
print(df.head())

### Example 2: Get the number of users and sessions by source channel (2021-05-01 to 2023-05-01)
ga = gaQuery(
    auth=auth,
    metrics=['ga:users'],
    dimensions=['ga:channelGrouping', 'ga:date'],
    startDate='2021-05-01',
    endDate='2023-05-01'
)
# export the data to an Excel file
ga.to_excel(filename='examples.xlsx')

