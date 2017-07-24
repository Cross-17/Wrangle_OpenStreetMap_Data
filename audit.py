
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "southampton_england.osm"

def audit_postcode (osmfile):
	"audit the postcode"
	osm_file = open(osmfile, "r")
	key_type = set()
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if tag.attrib['k'] == 'addr:postcode':
					if len(tag.attrib['v']) != 8 or tag.attrib['v'][4]!= " ":
						print tag.attrib['v']
	osm_file.close()
	print "finished"

#audit the steet type
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types