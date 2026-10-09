#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "requests",
# ]
# ///

from dataclasses import fields
import csv
'''
row_dict = {'ID': 'oid0001', 'Original Description': 'Sargent, John Singer (1856-1925), \
    portrait of Medallion (circular)  Inscribed:  "My Friend John Sargent. Paris IVLX M.D.CC.LLXX"', \
    'Creator': 'Saint-Gaudens, Augustus (1848-1907)', \
    'Narrative': 'Portrait cast on bronze Medallion (circular) Inscribed: "My Friend John Sargent. Paris IVLX M.D.CC.LLXX"', \
    'Provenance': 'Sargent, John Singer. Unknown', \
    'Donor': 'Sargent,Winthrop & Charles Sprague', \
    'Date of Gift': '1918?', 'Condition': 'CAPS:  Excellent condition. ', 'Conservation Recommendations ': 're-mount bronze to non-acidic backing board', 'Assessment Comment': 'Mounted directly onto a piece of wood. This acidic wood might cause corrosion to the bronze inside this closed frame  (see recommendations)', \
    'Creation_Date': ' 1880', \
    '2027 Location': 'JSSargent Room', \
    '2025 Location': 'JSSargent Room', \
    'Reference': 'See addenda', 'Priority To Conserve': 'CAPS#3', 'sub-Location': '', 'Origin': '', 'Medium': 'Cast Bronze', \
    'Object_Type': 'portrait', 'Subject_Style': 'Sargent, John Singer (1856-1925)', \
    'Dimensions': '2 1/2" ', 'Framed Dimensions': '', '2007 Location': 'Sargent Exhibit Room', 'Accession #': '1', 'Category': 'Fine Arts'}
'''

new_old_name_map = {
'John Murray Parlor': 'Best Parlor',
'Judith Sargent Murray Parlor': 'Common Parlor', 
'Historical Context Room': 'Murray Room',
'Boston-Gloucester Room': 'Judiths Room',
'Visitors Center': 'Museum Shop'}

fields = ['Priority', 'ID', 'Type', 'Subject/Style', 'Current Location', 'New Location',  'Dimensions (inches)', 'Comment']

def make_move_list_all_objects():
    move_list = []
    with open( "Collections-Inventory.csv", 'r' ) as f:
        sheet_rows = csv.DictReader(f)
        for idx, row_dict in enumerate(sheet_rows):
            # map new names to old names so things don't have to move based on room name change
            new_location = row_dict['2027 Location']
            if new_location in new_old_name_map:
                new_location = new_old_name_map[new_location]
            if row_dict['2025 Location'] != new_location:
                move_list.append([None, \
                            row_dict['ID'], row_dict['Object_Type'], row_dict['Subject_Style'][:31], \
                            row_dict['2025 Location'], row_dict['2027 Location'], \
                            row_dict['Dimensions'].replace('"','')[:25], ''])

    move_list.sort(key=lambda x: x[4])  #sort by Current location
    with open("objects_to_move.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(move_list)

def make_move_list_per_category(categories_dict):
    with open( "Collections-Inventory.csv", 'r' ) as f:
        sheet_rows = csv.DictReader(f)
        for idx, row_dict in enumerate(sheet_rows):
            # map new names to old names so things don't have to move based on room name change
            new_location = row_dict['2027 Location']
            if new_location in new_old_name_map:
                new_location = new_old_name_map[new_location]

            for category_dict in categories_dict:
                for pattern in categories_dict[category_dict]["oid_list"]:
                    if pattern == row_dict['ID'][:len(pattern)] and row_dict['2025 Location'] != new_location:
                        shortened_dimensions = row_dict['Dimensions'].replace('"','')[:25]
                        categories_dict[category_dict]["objects"].append([None, \
                            row_dict['ID'], row_dict['Object_Type'], row_dict['Subject_Style'][:31], \
                            row_dict['2025 Location'], row_dict['2027 Location'], \
                            shortened_dimensions, ''])

    categories_dict["furniture"]["objects"].append(['1', 'None', 'Cabinet', 'Painted White', '2ndFloorWorkshop', 'Street Curb', '46 x 20 x 80', 'making space for other furniture'])
    categories_dict["furniture"]["objects"].append(['1', 'None', 'Cabinet', 'Pine', '2ndFloorWorkshop', 'Street Curb', '46 x 20 x 80', 'making space for other furniture'])

    for category_dict in categories_dict:
        categories_dict[category_dict]["objects"].sort(key=lambda x: x[4])  #sort by Current location

    for category_dict in categories_dict:
        filename = category_dict + ".csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(categories_dict[category_dict]["objects"])

if __name__ == "__main__":
    make_move_list_all_objects()
    exit()

    categories_dict = {"furniture": {"oid_list":['oid05', 'oid06'], "objects":[]}, \
                        "artwork": {"oid_list":['oid00', 'oid0013'], "objects":[]}, \
                    }
    make_move_list_per_category(categories_dict)
