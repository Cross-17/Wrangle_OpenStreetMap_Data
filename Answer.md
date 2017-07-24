
# Wrangling OpenStreetMap Data

## Map Area
 Southampton,UK
* https://www.openstreetmap.org/relation/127864

The OML file is 63.9 MB

This is the place I got my Master degree in Computer Science. It's a small city famous for its education, and I spend around 1 year study here.

## Process of Project
After downloading the OML file, I firstly explore the dataset, by auditing the address field in all way and node tags. For example, in audit.py, I inspect all the postcode and street type in the dataset, and ensures that they conform to the correct format.

Then I read all the data from OML file, store them in python dictionary format, correcting the error data found on the auditing phase, and saving all corrected data into csv file. All code in this phase could be found on process.py

Lastly I import all the csv file into sqlite database on the sqlite3 command line, and explore the data with all kinds of SQL command.

## Problems encountered in  map
I audited lots of field in this dataset and surprisingly find that this dataset is overall quite clean.

One problem I encountered in the map is inconsistent street type name ('Bluebell Raod','Bluebell road','Bellevue Rd' etc)

Here is how I fix this in code:


```python
mapping = { "Raod": "Road",
            "road": "Road",
            "Rd": "Road",
            "Rd.": "Road",
            }
def update_name(name, mapping):
    for key in mapping.keys():
        if key in name and not mapping[key] in name:
            name = name.replace(key,mapping[key])
    return name
```

Another problem is that there are some strange number or character ("387","S") in the steet field, which I have no idea to deal with.

## Overview of the data
### Size of files


```python
import os
files = os.listdir(os.getcwd())
interested = ['csv','osm','db']
for item in files:
    for extention in interested:
        if extention in item:
            print item+":"
            print os.path.getsize(item)/1024.0/1024.0,"MB"
            print " "
```

    nodes.csv:
    22.3287258148 MB
     
    nodes_tags.csv:
    0.774829864502 MB
     
    southampton_england.osm:
    63.9946393967 MB
     
    sqlite.db:
    38.3193359375 MB
     
    ways.csv:
    3.10630226135 MB
     
    ways_nodes.csv:
    8.90686416626 MB
     
    ways_tags.csv:
    6.02402973175 MB
     
    

### Number of nodes


```python
import sqlite3
db = sqlite3.connect('sqlite.db')

def makequery(query):
    "accept and run the query, then print out results"
    c = db.cursor()
    c.execute(query)
    rows = c.fetchall()
    for row in rows:
        print row
```


```python
query = '''
select count() from nodes
'''
makequery(query)
```

    (273444,)
    

### Number of ways


```python
query = '''
select count() from ways
'''
makequery(query)
```

    (51489,)
    

### Number of unique users


```python
query = '''
select count() from 
(select uid from nodes 
UNION ALL
select uid from ways
group by uid) as view;
'''
makequery(query)
```

    (273842,)
    

### Top 10 contributing users


```python
query = '''
select view.user,count() as num from 
(select user from nodes 
UNION ALL
select user from ways) as view
group by user
order by num desc
limit 10
'''
makequery(query)
```

    (u'Chris Baines', 107146)
    (u'Harjit (CabMyRide)', 24969)
    (u'0123456789', 23755)
    (u'Nick Austin', 17677)
    (u'pcman1985', 14149)
    (u'Deanna Earley', 13430)
    (u'Arjan Sahota', 12946)
    (u'Kuldip (CabMyRide)', 9614)
    (u'Andy Street', 9181)
    (u'Harry Cutts', 6675)
    

### Top 10 popupar amenty


```python
query = '''
select value, count() as num from nodes_tags
where key = 'amenity'
Group by value
Order by num desc
limit 10'''
makequery(query)
```

    (u'post_box', 568)
    (u'bicycle_parking', 408)
    (u'telephone', 236)
    (u'bench', 208)
    (u'fast_food', 120)
    (u'atm', 90)
    (u'pub', 86)
    (u'restaurant', 86)
    (u'cafe', 84)
    (u'waste_basket', 68)
    

###  Additional exploration
###  Religion


```python
query = '''
select value, count() as num
from nodes_tags 
where nodes_tags.key='religion'
group by value
order by num desc
'''
makequery(query)
```

    (u'christian', 48)
    (u'muslim', 8)
    (u'Multifaith', 2)
    

### Popular food type


```python
query = '''
select value, count() as num from nodes_tags where key = 'cuisine'
group by value
order by num desc
'''
makequery(query)
```

    (u'chinese', 36)
    (u'coffee_shop', 26)
    (u'fish_and_chips', 22)
    (u'indian', 16)
    (u'italian', 14)
    (u'pizza', 12)
    (u'sandwich', 12)
    (u'chicken', 6)
    (u'kebab', 6)
    (u'burger', 4)
    (u'pie', 4)
    (u'thai', 4)
    (u'British', 2)
    (u'american', 2)
    (u'chinese_food_and_fish_and_chips', 2)
    (u'greek', 2)
    (u'spanish', 2)
    (u'sushi', 2)
    

### City


```python
query = '''
SELECT *, COUNT() as count
FROM 
(SELECT * FROM nodes_tags UNION ALL
SELECT * FROM ways_tags) as tags
WHERE tags.key = 'city'
GROUP BY tags.value
ORDER BY count DESC
'''
makequery(query)
```

    (503101329, u'city', u'Southampton', u'addr\r', 17104)
    (398218129, u'city', u'Woolston, Southampton', u'addr\r', 12)
    (392320664, u'city', u'Netley Abbey', u'addr\r', 10)
    (291613728, u'city', u'West End, Southampton', u'addr\r', 8)
    (4283133928L, u'city', u'Marchwood, Southampton', u'addr\r', 6)
    (445923165, u'city', u'Eastleigh', u'addr\r', 5)
    (3768107099L, u'city', u'Bursledon, Southampton', u'addr\r', 2)
    (3789048114L, u'city', u'Nursling, Southampton', u'addr\r', 2)
    (4944303106L, u'city', u'Solihull', u'addr\r', 2)
    (293465469, u'city', u'Thornhill, Southampton', u'addr\r', 2)
    (4661365635L, u'city', u'Townhill Park, Southampton', u'addr\r', 2)
    (40581969, u'city', u'Bassett', u'addr\r', 1)
    (294010101, u'city', u'Bitterne Village, Southampton', u'addr\r', 1)
    (265076854, u'city', u'Southampton`', u'addr\r', 1)
    

### Source


```python
query = '''
SELECT value,type,COUNT(*) as count
FROM 
(SELECT * FROM nodes_tags UNION ALL
SELECT * FROM ways_tags) as tags
WHERE tags.key = 'source'
GROUP BY value
ORDER BY count DESC
'''
makequery(query)
```

    (u'Bing', u'regular\r', 5023)
    (u'PGS', u'regular\r', 424)
    (u'naptan_import', u'regular\r', 285)
    (u'Yahoo', u'regular\r', 268)
    (u'survey', u'regular\r', 231)
    (u'Bing Imagery', u'regular\r', 166)
    (u'OS_OpenData_StreetView', u'regular\r', 140)
    (u'OS VectorMap District', u'regular\r', 107)
    (u'OS_opendata_streetview', u'regular\r', 73)
    (u'OS OpenData StreetView', u'regular\r', 70)
    (u'bing', u'regular\r', 66)
    (u'local_knowledge', u'regular\r', 49)
    (u'US NGA Pub. 114. 2011-05-26.', u'regular\r', 40)
    (u'Landsat', u'regular\r', 36)
    (u'survey,Bing', u'regular\r', 36)
    (u'Survey', u'regular\r', 33)
    (u'yahoo', u'regular\r', 30)
    (u'Yahoo imagery', u'regular\r', 27)
    (u'OS_OpenData_Streetview', u'regular\r', 21)
    (u'Dashcam survey;Bing Imagery', u'regular\r', 18)
    (u'OS_OpenData_Boundary-Line', u'regular\r', 18)
    (u'GPS', u'regular\r', 15)
    (u'Bing;local_knowledge', u'regular\r', 14)
    (u'Bing, Survey', u'regular\r', 13)
    (u'www.npemap.org.uk', u'regular\r', 12)
    (u'Bing imagery', u'regular\r', 11)
    (u'local knowledge', u'regular\r', 11)
    (u'GPS trace (bad) and local knowledge', u'regular\r', 10)
    (u'survey;bing', u'regular\r', 10)
    (u'yahoo;survey', u'regular\r', 9)
    (u'OS_OpenData_BoundaryLine', u'regular\r', 8)
    (u'Survey;Bing', u'regular\r', 8)
    (u'Bing imagery;Local knowledge', u'regular\r', 7)
    (u'Bing_Aerial', u'regular\r', 7)
    (u'npe', u'regular\r', 7)
    (u'WebSite', u'regular\r', 6)
    (u'local_knowledge;Bing', u'regular\r', 6)
    (u'yahoo; Bing', u'regular\r', 6)
    (u'yahoo;knowledge', u'regular\r', 6)
    (u'Bing,Ground visit', u'regular\r', 5)
    (u'Yahoo Ariel Imagary', u'regular\r', 5)
    (u'gas', u'plant\r', 5)
    (u'knowledge', u'regular\r', 5)
    (u'local_knowledge; Bing', u'regular\r', 5)
    (u'local_knowledge; Yahoo', u'regular\r', 5)
    (u'Local knowledge', u'regular\r', 4)
    (u'bing;OS_OpenData_StreetView', u'regular\r', 4)
    (u'interpolation', u'regular\r', 4)
    (u'Bing, local visit', u'regular\r', 3)
    (u'Bing;OS_OpenData_Streetview', u'regular\r', 3)
    (u'Hampshire County Council', u'regular\r', 3)
    (u'Local Knowledge', u'regular\r', 3)
    (u'os_opendata_streetview', u'regular\r', 3)
    (u'survey;yahoo', u'regular\r', 3)
    (u'Bing; OS_OpenData_StreetView', u'regular\r', 2)
    (u'Bing; Yahoo', u'regular\r', 2)
    (u'Bing; survey', u'regular\r', 2)
    (u'Bing;OS_OpenData_StreetView', u'regular\r', 2)
    (u'Bing_Aerial; Bing', u'regular\r', 2)
    (u'GPS trace', u'regular\r', 2)
    (u'Local_Knowledge', u'regular\r', 2)
    (u'Local_knowledge', u'regular\r', 2)
    (u'OS_OpenData_Boundary Maps Extract', u'regular\r', 2)
    (u'Own Knowledge', u'regular\r', 2)
    (u'Unknown;Bing', u'regular\r', 2)
    (u'Yahoo; Local knowledge', u'regular\r', 2)
    (u'Yahoo_Aerial', u'regular\r', 2)
    (u'http://www.openstreetmap.org/browse/changeset/10537517', u'regular\r', 2)
    (u'landsat', u'regular\r', 2)
    (u'survey;Bing', u'regular\r', 2)
    (u'wind', u'generator\r', 2)
    (u'www.isoc.susu.org', u'regular\r', 2)
    (u'www.starbucks.co.uk/store/1006110/', u'regular\r', 2)
    (u'Bing,local knowledge', u'regular\r', 1)
    (u'Bing,survey', u'regular\r', 1)
    (u'Bing/local knowledge', u'regular\r', 1)
    (u'Bing; yahoo;survey', u'regular\r', 1)
    (u'Bing;Gagravarr_Airports', u'regular\r', 1)
    (u'Bing;OS OpenData StreetView', u'regular\r', 1)
    (u'Bing;local visit', u'regular\r', 1)
    (u'Bing;survey', u'regular\r', 1)
    (u'Disused', u'regular\r', 1)
    (u'GPS survey', u'regular\r', 1)
    (u'Groundsource', u'regular\r', 1)
    (u'Local', u'regular\r', 1)
    (u'My own photos', u'regular\r', 1)
    (u'NPE', u'regular\r', 1)
    (u'OS Streetview', u'regular\r', 1)
    (u'OS_opendata_streetview;Bing', u'regular\r', 1)
    (u'OpenStreetView', u'regular\r', 1)
    (u'Personal', u'regular\r', 1)
    (u'Personal Knowledge', u'regular\r', 1)
    (u'Potlatch OS b/g', u'regular\r', 1)
    (u'Potlatch background', u'regular\r', 1)
    (u'SCC Definitive Statement of Rights of Way April 2012', u'regular\r', 1)
    (u'Site visit', u'regular\r', 1)
    (u'Yahoo, Bing', u'regular\r', 1)
    (u'Yahoo, local_knowledge', u'regular\r', 1)
    (u'Yahoo/OS', u'regular\r', 1)
    (u'Yahoo/train journey/Bing', u'regular\r', 1)
    (u'Yahoo; knowledge; Bing', u'regular\r', 1)
    (u'Yahoo; local_knowledge', u'regular\r', 1)
    (u'Yahoo;local_knowledge', u'regular\r', 1)
    (u'accolade', u'regular\r', 1)
    (u'bing plus visit', u'regular\r', 1)
    (u'buildings inside tagged as offices', u'regular\r', 1)
    (u'charity', u'regular\r', 1)
    (u'extrapolation', u'regular\r', 1)
    (u'geothermal', u'generator\r', 1)
    (u'gps', u'regular\r', 1)
    (u'http://www.gleneagles.org.uk/', u'regular\r', 1)
    (u'http://www.premier-stores.co.uk/find-our-stores.html', u'regular\r', 1)
    (u'landsat/Bing', u'regular\r', 1)
    (u'local visit', u'regular\r', 1)
    (u'local visit;Bing', u'regular\r', 1)
    (u'local_knowledge: Yahoo; Bing', u'regular\r', 1)
    (u'resident', u'regular\r', 1)
    (u'survey;bing;inferred', u'regular\r', 1)
    (u'user knowledge', u'regular\r', 1)
    (u'yahoo imagery', u'regular\r', 1)
    (u'yahoo;Bing', u'regular\r', 1)
    (u'yahoo;knowledge;bing', u'regular\r', 1)
    

## Additional suggestions & Conclusion

Wrangling this dataset gives me a flavour of how the dataset was cleaned, processed and imported into database, and how we could make use of these data. 

To improve the dataset and it's analysis, I think openstreet map should add a  automatic association system.  

Reason: The same thing often appears in the dataset in different ways(e.g. 'Rd'. vs 'Road', Southampton vs 'Southampton`', 'Bing' vs 'bing'). This is often caused by data edited from different user.  
If the system could automatically associate a existing common key when user enter a few letter, such error would reduce significantly.  
Although the system is effective not hard to write, it is kind of difficult to update all the programs which write data to the Openstreet map project.



## Sources
* [Sample project](https://gist.github.com/carlward/54ec1c91b62a5f911c42#openstreetmap-data-case-study)


```python

```
