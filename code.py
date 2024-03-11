import requests as rq
import bs4
import pandas as pd
import plotly.express as px
import numpy as np

## START PART 1
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
page = rq.get(url)
## print out the first 50 characters just to see what it looks like
page.text[0 : 50]

bs4page = bs4.BeautifulSoup(page.text, 'html.parser')
tables = bs4page.find_all('table',{'class':"wikitable"})

from io import StringIO
# Read the table from the StringIO object into pandas
# Note most recent version of pandas won't accept a string as input, it needs to be passed through stringio
gdp = pd.read_html(StringIO(str(tables[0])))[0]
gdp = gdp.dropna()
gdp.head()

gdp.columns = gdp.columns.droplevel(0)
gdp.rename(columns={'UN region': 'Region'}, inplace=True)
gdp.rename(columns={'Country/Territory': 'Country_or_territory'}, inplace=True)

gdp = gdp.assign(region = gdp.Region.astype(str))
gdp = gdp.assign(GDP = gdp.Forecast.astype(str))
gdp = gdp.assign(Country_or_territory = gdp.Country_or_territory.astype(str))

gdp.head()

fig = px.bar(gdp, x = "Region", y = "GDP", color = "Country_or_territory")
fig.show()
## END PART 1

fig.write_html(outfile, include_plotlyjs='cdn')
