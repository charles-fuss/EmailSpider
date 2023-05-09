import pandas as pd
from real_email_crawl import EmailCrawler
import time,requests
from lxml import html


# update the path to your excel sheet
pathToExcel = r"yourpathhere"
df = pd.read_excel(pathToExcel)

# update to the name of all columns in the excel sheet
# ex.) columnsList = ['PWS ID', 'PWS Name', 'Status', 'Contact First', 'Contact Last', 'Address1', 'Address2', 'City','State','Zip', 'Phone', 'NAICS', 'PWS Type',	'OWNER',	'Site', 'Emails']
columnsList = []
print('Loaded DF')
newDF = pd.DataFrame(columns=columnsList)


# this will go thru each site and add array to sheet -- make sure the name of the column of URLs you're trying to parse are called "Site" and the title of the column holding the sites' names is called "Name"
for i, value in enumerate(df['Site']):
    time.sleep(1)
    if value != 'nil':
        print(f"Inputs to EmailCrawer: {df['Name'][i], df['Site'][i]}")
        testCrawl = EmailCrawler(df['Name'][i], df['Site'][i])
        x = testCrawl.crawl()
        rowToCopy = df.loc[i]
        dfToAppend = pd.DataFrame([rowToCopy])
        # add new row for each email
        for f in range(len(x[2])):
            dfToAppend.iloc[[0], [15]] = str(x[2][f]) # modify 15 to the last filled column of your excel sheet 
            newDF = pd.concat([newDF, dfToAppend], ignore_index=True)
            print(newDF)
        newDF.iloc
        print(f'Processed {x[0]}')
newDF.to_csv('mailResults.csv', index=False)