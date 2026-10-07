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

output_rows = []

new_old_name_map = {
'John Murray Parlor': 'Best Parlor',
'Judith Sargent Murray Parlor': 'Common Parlor', 
'Historical Context Room': 'Murray Room',
'Boston-Gloucester Room': 'Judiths Room',
'Visitors Center': 'Museum Shop'}

output_files =[("furniture", ['oid05', 'oid06']), ("artwork", ['oid00', 'oid0013'])]

for item in output_files:
    list[item[0]] = []

with open( "Collections-Inventory.csv", 'r' ) as f:
    sheet_rows = csv.DictReader(f)
    for idx, row_dict in enumerate(sheet_rows):
        # map new names to old names so things don't have to move based on room name change
        new_location = row_dict['2027 Location']
        if new_location in new_old_name_map:
            new_location = new_old_name_map[new_location]

        #only list furniture and specific artwork, e.g. busts
        furniture_id_patterns = ['oid05', 'oid06', 'oid0014', 'oid0015']
        for pattern in furniture_id_patterns:
            if pattern == row_dict['ID'][:len(pattern)] and row_dict['2025 Location'] != new_location:
                shortened_dimensions = row_dict['Dimensions'].replace('"','')[:25]
                output_rows.append([None, row_dict['2025 Location'], row_dict['2027 Location'], \
                    row_dict['Object_Type'], row_dict['Subject_Style'][:14], shortened_dimensions, '', row_dict['ID']])

fields = ['Priority', 'Current Location', 'New Location', 'Type', 'Subject/Style', 'Dimensions (inches)', 'Comment', 'ID']
cabinet1 = ['1', '2ndFloorWorkshop', 'Street Curb', 'Cabinet', 'Painted White', '46 x 20 x 80', 'making space for other furniture', 'None']
cabinet2 = ['1', '2ndFloorWorkshop', 'Street Curb', 'Cabinet', 'Pine', '46 x 20 x 80', 'making space for other furniture','None']
output_rows.sort(key=lambda x: x[2])  #sort by New location
with open('move_list.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerow(cabinet1)
    writer.writerow(cabinet2)
    writer.writerows(output_rows)