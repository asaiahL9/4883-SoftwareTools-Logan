## Assignment 8

### Create an API using fastapi

|   #   | File                 | Description               |
| :---: | -------------------- | ------------------------- |
|   1   | [main.py](main.py)   | [Implementation](main.py) |
|   2   | [data.csv](data.csv) | [Data File](data.csv)     |


http:localhost:5000/deaths/

This method will return a total death count or can be filtered by country and year, average deaths per year, and deaths per country per year.
    - **Params:**
      - type(str) : the type of query: country, min, max, avg
      - optional: min_date(str) : start date of search query 
      - optional: max_date(str) : end date of search query
      - optional: country (str) : A country name
      - optional: year (str) : A 4 digit year

    #### Example 1:

    http://localhost:5000/deaths/?type=country&country=Algeria

    #### Response 1:

    {
        "success": true,
        "data": "Algeria",
        "deaths": 6881,
        "message": "Deaths By Country"
    }

    #### Response 2:

    http://localhost:5000/deaths/?type=country&min_date=2020-01-03&max_date=2023-07-08

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

    http://localhost:5000/deaths/?type=country&year=2020&country=Andorra

    {
        "success": true,
        "data": "Andorra",
        "deaths": 159,
        "year": "2020",
        "message": "Deaths By Country"
    }

    #### Response 4

    http://localhost:5000/deaths/?type=min&min_date=2020-01-03&max_date=2023-07-07
     
    {
        "success": true,
        "min_deaths2020-01-03 -> 2023-07-07": [
            "Democratic People's Republic of Korea",
            0
            ],
        "message": "least_deaths"
    }

    #### Response 5

    http://localhost:5000/deaths/?type=max&min_date=2020-01-03&max_date=2023-07-07
     
    {
        "success": true,
        "max_deaths2020-01-03 -> 2023-07-07": [
        "United States of America",
        1127152
        ],
        "message": "most_deaths"
    }


http:localhost:5000/deaths_by_country/
    This method will return a total death count or can be filtered by country and year, average deaths per year, and deaths per country per year.
    - **Params:**
      - region(str) : a WHO region code (optional)
    - **Returns:**
      - {dict} : regions : deaths

localhost:5000/countries/
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
          ]
    }


http://localhost:5000/whos/

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


http://localhost:5000/casesByRegion/

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