
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import csv
from tqdm import tqdm
from datetime import datetime, timedelta


description = """🚀
## 4883 Software Tools
### Where awesomeness happens
"""


app = FastAPI(

    description=description,

)

db = []

# Open the CSV file
with open('data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    i = 0
    # Read each row in the CSV file
    for row in reader:
        if i == 0:
            i += 1
            continue
        db.append(row)


def getUniqueCountries():
    global db
    countries = {}

    for row in db:
        # print(row)
        if not row[2] in countries:
            countries[row[2]] = 0

    return list(countries.keys())



def getUniqueWhos():
    global db
    whos = {}

    for row in db:
        # print(row)
        if not row[3] in whos:
            whos[row[3]] = 0
   
    return list(whos.keys())

@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/deaths/")
async def deaths(type: str, year: str | None = None, min_date: str | None=None, max_date: str|None=None, country: str|None=None):
    """
    This method will return a total death count or can be filtered by country and year, average deaths per year, and deaths per country per year.
    - **Params:**
      - type(str) : the type of query: country, min, max, avg
      - optional: min_date(str) : start date of search query 
      - optional: max_date(str) : end date of search query
      - optional: country (str) : A country name
      - optional: year (str) : A 4 digit year

    #### Example 1:

    [http://localhost:5000/deaths/?type=country&country=Algeria](http://localhost:5000/deaths/?type=country&country=Algeria)

    #### Response 1:

    {
        "success": true,
        "data": "Algeria",
        "deaths": 6881,
        "message": "Deaths By Country"
    }

    #### Response 2:

    [http://localhost:5000/deaths/?type=country&min_date=2020-01-03&max_date=2023-07-08](http://localhost:5000/deaths/?type=country&min_date=2020-01-03&max_date=2023-07-08)

    {
    "success": true,
    "deaths_by_countries": {
        "Afghanistan": 7922,
        "Albania": 3604,
        "Algeria": 6881,
        "American Samoa": 34,
        "Andorra": 159,
        "Angola": 1934,
        "Anguilla": 12,
        "Antigua and Barbuda": 146,
        "Argentina": 130472,
        "Armenia": 8750,
        "Aruba": 290,
        etc...
    }

    #### Response 3:

    [http://localhost:5000/deaths/?type=country&year=2020&country=Andorra](http://localhost:5000/deaths/?type=country&year=2020&country=Andorra)

    {
        "success": true,
        "data": "Andorra",
        "deaths": 159,
        "year": "2020",
        "message": "Deaths By Country"
    }

    #### Response 4

    [http://localhost:5000/deaths/?type=min&min_date=2020-01-03&max_date=2023-07-07](http://localhost:5000/deaths/?type=min&min_date=2020-01-03&max_date=2023-07-07)
     
    {
        "success": true,
        "min_deaths2020-01-03 -> 2023-07-07": [
            "Democratic People's Republic of Korea",
            0
            ],
        "message": "least_deaths"
}

    #### Response 5

    [http://localhost:5000/deaths/?type=max&min_date=2020-01-03&max_date=2023-07-07](http://localhost:5000/deaths/?type=max&min_date=2020-01-03&max_date=2023-07-07)
     
    {
        "success": true,
        "max_deaths2020-01-03 -> 2023-07-07": [
        "United States of America",
        1127152
        ],
        "message": "most_deaths"
    }
    """
    # import data into funtion
    global db
    deaths = {}
    # add data to dictionary
    for row in db:
        # add key to dict if it does not exist
        if not row[2] in deaths:
            deaths[row[2]] = row[6]
        # add new deaths to key value
        else: 
            deaths[row[2]] = int(deaths[row[2]]) + int(row[6]) 
    # if type is not entered
    if not type:
        return {"success": False, "message" : 'type required - min, max, avg, total'}
    # begin total calculation
    if type == 'total':
        # add dict values
        total = sum(deaths.values())
        # return total deaths with status message
        return {"success": True, "data": total, "message": "total_deaths"}
    # calc avg of all data
    if type == 'avg' and not year:
        # calc average
        avg = sum(deaths.values()) / len(deaths)
        # return total deaths with status message
        return {"success": True, "avg_deaths_all": avg, "message": "average_deaths"}
    #  calc avg for given year
    if type == 'avg' and year:
        sum = 0
        # new empty dict
        per_year = {}
        # print(year)
        i = 0
        for row in db:
            # append new data to dict if year in db = given year
            if row[0][:4] == str(year):
                i = i+1
                print(i)
                # make new keys
                if not row[2] in per_year:
                    per_year[row[2]] = row[6]
                else:
                    # add new deaths
                    per_year[row[2]] = int(deaths[row[2]]) + int(row[6])
            # return per year dict
        return {"success": True, "data": per_year}
    # begin country operation
    if type == 'country':
        # if no country provided return all countries : deaths
        if not country:
            return {"success": True, "deaths_by_countries":deaths.items(), "message":"Deaths By Country"}
        # return deaths for specific country
        if country and not year:
            if country in deaths:
                return {"success": True,"data": country, "deaths": deaths[country], "message": "Deaths By Country"}
        # calc deaths for a specific country in specific year
        if country and year:
            newdict = {}
            if country in deaths:
                for row in db:
                    if row[0][:4] == year and row[2] == country:
                        if not row[2] in newdict:
                            newdict[row[2]] = row[6]
                        else:
                            newdict[row[2]] = int(deaths[row[2]]) + int(row[6])
                return {"success": True,"data": country, "deaths": newdict[country], "year": year, "message": "Deaths By Country"}
        # if country does not exist
        else:
            return {"success": False, "message":"Country not found"}
    # calculate country with minimum deaths in a time period
    if type == 'min' and min_date and max_date:
        minmax = {}
        # init datetime objects
        ogdate = date = datetime.strptime(min_date, "%Y-%m-%d")
        end_date = datetime.strptime(max_date,'%Y-%m-%d')

        i = 0
        # search db for matching dates until the end of the max_date
        # add data to new dict
        for row in tqdm(db, desc='db'):
            rowdate = datetime.strptime(row[0], "%Y-%m-%d")
            if date.date() < rowdate.date():
                date = rowdate
            if i < 2:
                print(str(date.date()) + " " + row[0])
                i = i + 1
            if row[0] == str(date.date()): 

                if not row[2] in minmax:
                    
                    minmax[row[2]] = row[6]
                else:
                    minmax[row[2]] = int(deaths[row[2]]) + int(row[6])
            date += timedelta(days=1)
            if date > end_date:
                date = ogdate
        min_item = min(minmax.items(), key=lambda x:x[1])
        return {"success": True, f"min_deaths{min_date} -> {max_date}": min_item, "message": "least_deaths"}

    if type == 'max':
        minmax = {}
        # init datetime objects
        ogdate = date = datetime.strptime(min_date, "%Y-%m-%d")
        end_date = datetime.strptime(max_date,'%Y-%m-%d')

        i = 0
        # search db for matching dates until the end of the max_date
        # add data to new dict
        for row in tqdm(db, desc='db'):
            rowdate = datetime.strptime(row[0], "%Y-%m-%d")
            if date.date() < rowdate.date():
                date = rowdate
            if i < 2:
                print(str(date.date()) + " " + row[0])
                i = i + 1
            if row[0] == str(date.date()): 

                if not row[2] in minmax:
                    
                    minmax[row[2]] = row[6]
                else:
                    minmax[row[2]] = int(deaths[row[2]]) + int(row[6])
            date += timedelta(days=1)
            if date > end_date:
                date = ogdate
        # return max item
        max_item = max(minmax.items(), key=lambda x:x[1])
        return {"success": True, f"max_deaths{min_date} -> {max_date}":  max_item, "message": "most_deaths"}

@app.get("/deaths_by_region/")
async def deaths_by_region(region: str | None = None):
    """
    This method will return a total death count or can be filtered by country and year, average deaths per year, and deaths per country per year.
    - **Params:**
      - region(str) : a WHO region code (optional)
    - **Returns:**
      - {dict} : regions : deaths
    """
    global db
    deaths = {}

    for row in db:
        if not row[3] in deaths:
            deaths[row[3]] = row[6]
        else: 
            deaths[row[3]] = int(deaths[row[3]]) + int(row[6]) 

    if not region:
        return deaths
    else:
        if region in deaths:
            return {"success": True, "data": deaths[region]}
        else:
            return {"success": False, "message": "Region not found"}

@app.get("/deaths_by_country/")
async def deaths_by_country(country: str | None = None, year: str | None=None):
    """
    This method will return a total death count for a country or all countries
    - **Params:**
      - country(str) : a country name (optional)
    - **Returns:**
      - {dict} : countries : deaths
    """
    global db
    deaths = {}
    for row in db:
        if not row[2] in deaths:
            deaths[row[2]] = row[6]
        else: 
            deaths[row[2]] = int(deaths[row[2]]) + int(row[6]) 
    if not country:
        return {"success": True, "deaths_by_countries":deaths.items(), "message":"Deaths By Country"}
    if country and not year:
        if country in deaths:
            return {"success": True,"data": country, "deaths": deaths[country], "message": "Deaths By Country"}
        else:
            return {"success": False, "message":"Country not found"}


@app.get("/countries/")
async def countries():
    """
    Returns a dictionary of all unique country names
    #### Response 1

    http://localhost:5000/countries/

    {
    "success": true,
    "countries": [
        "Afghanistan",
        "Albania",
        "Algeria",
        "American Samoa",
        "Andorra",
        "Angola",
        "Anguilla",
        "Antigua and Barbuda",
        "Argentina",
        "Armenia",
        "Aruba",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Bahamas",
        ...
    }
    """
    return {"success": True, "countries":getUniqueCountries()}


@app.get("/whos/")
async def whos():
    """
    Returns a dictionary of all WHO region codes

    #### Response 
    {
    "success": true,
    "whos": [
        "EMRO",
        "EURO",
        "AFRO",
        "WPRO",
        "AMRO",
        "SEARO",
        "Other"
    ]
    }

    """
    return {"success": True, "whos":getUniqueWhos()}

"""
Returns total of all deaths in each region

#### Response 1
()
"""
@app.get("/casesByRegion/")
async def casesByRegion(year:int = None):
    """
    Returns the number of cases by region
    
    #### Response

    {
        "data": {
            "EMRO": 23382124,
            "EURO": 276545765,
            "AFRO": 9538679,
            "WPRO": 204478043,
            "AMRO": 193056651,
            "SEARO": 61185070,
            "Other": 764
        },
        "success": true,
        "message": "Cases by Region",
        "size": 7,
        "year": null
    }
    """

    cases = {}
    
    for row in db:
        if year != None and year != int(row[0][:4]):
            continue
            
        if not row[3] in cases:
            cases[row[3]] = 0
        cases[row[3]] += int(row[4])    

    return {"data":cases,"success":True,"message":"Cases by Region","size":len(cases),"year":year}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="debug", reload=True) #host="127.0.0.1"