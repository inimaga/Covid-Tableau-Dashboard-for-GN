## Author: Issa Nimaga
## Project Name: Dashboard data refresher/updater
## Description: This python script runs to refresh the data for the Guinea Covid19 Tableau Dashboard (https://issanimaga.com/projects/GN_Covid19_Dashboard/)

import requests
import pandas
import io
import gspread

# Fetch covid data from 'Our World in Data' (@ https://ourworldindata.org/coronavirus-source-data)
print("\nFetching data from 'Our World in Data' ...")
dataSourceUrl = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
dataFile = requests.get(dataSourceUrl).content
data = pandas.read_csv(io.StringIO(dataFile.decode('utf-8')))
print("Data fetched succesfully!")

# Selection of specific columns relevant to the dashboard
print("\nSelecting relevant columns..")
data2post = data[['location','date','total_cases','total_deaths','population']]
print("The selection/filtering operation succeeded!")

# Posting fetched data from EU open data portal to the google sheets
print("\nPosting fetched data to google sheets...")
pandas.options.mode.chained_assignment = None  # Disabling warnings regarding copying sliced data
data2post.fillna('', inplace=True) #Replacing all NaN values with empty string, otherwise the posting to google sheets will fail

gs = gspread.service_account(filename='./CovidDataRefresher.json')
sh = gs.open("Data Source for GN Tableau Covid Dashboard")

worksheet = sh.worksheet("Raw Data - Automated Refresh")
worksheet.update([data2post.columns.values.tolist()] + data2post.values.tolist())

print("\nDone! All tasks have been succesfully completed.\n")