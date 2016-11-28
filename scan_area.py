import os
import sys
import math
import json

import s2sphere
# add directory of this file to PATH, so that the package will be found
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from mock_pgoapi import mock_pgoapi as pgoapi

def break_down_area_to_cel(north, south, west, east):
	""" Return a list of s2 cell id """
	result = []

	region = s2sphere.RegionCoverer()
	region.min_level = 15
	region.max_level = 15
	p1 = s2sphere.LatLng.from_degrees(north, west)
	p2 = s2sphere.LatLng.from_degrees(south, east)

	cellids = region.get_covering(s2sphere.LatLngRect.from_point_pair(p1, p2))

	for cell in cellids:
		result.append(cell.id())

	return result

def get_position_from_cell_id(cell_id):
	cell = s2sphere.CellId(id_ = cell_id).to_lat_lng()

	return (math.degrees(cell._LatLng__coords[0]), math.degrees(cell._LatLng__coords[1]), 0)

def parse_pokemons_from_response(response_dict):
    return response_dict["responses"]["GET_MAP_OBJECTS"]["map_cells"][0]["catchable_pokemons"]

def scan_point(cell_id):
	""" Return pokemons in cell_id """

	api = pgoapi.PGoApi()

	position = get_position_from_cell_id(cell_id)
	cell_ids = [cell_id]
	response_dict = api.get_map_objects(latitude =position[0],
									    longitude = position[1], 
									    since_timestamp_ms = [0], 
									    cell_id = cell_ids)

	return parse_pokemons_from_response(response_dict)

def scan_area(north, south, west, east):
	pokemons = []

	# 1. Find all points in this area
	cell_ids = break_down_area_to_cel(north, south, west, east)

	# 2. Scan current area
	for cell_id in cell_ids:
		pokemons += scan_point(cell_id)

	return pokemons

if __name__ == "__main__":
	print "Hello World"
	print json.dumps(scan_area(40.8, 40.7, -74, -73.9), indent = 2)