# File: numericize_graph_json.py
# @author: Isaac Caswell
# @created: 8 Jun 2016, 2:12pm
#
# Purpose: 
# converts a list of nodes and links between them to the same thing only where the links 
# are numerical indices of the nodes.  This is so you can specify the file in a human-readible 
# way, and use this script to convert it to something that d3 can visualize.
#
# The input file must be a json file with two keys: 
#	"nodes": a list of dicts with name field
#	"links": a list of dicts with source and target fields


import json
from pprint import pprint



INFILE = "../data/concretions/RagamsTraditional_human_readable.json"
OUTFILE = "../data/concretions/RagamsTraditional.json"



assert INFILE != OUTFILE, "You'll regret overwriting the same file, trust me"

data=None
with open(INFILE) as data_file:    
    data = json.load(data_file)

assert data.keys() == [u"nodes", u"links"], "just making sure that this is being called on the right sort fo file"

node_name_to_numeric_value = {}
for i, obj in enumerate(data["nodes"]):
	node_name_to_numeric_value[obj["name"]] = i


for obj in data["links"]:
	obj["source"] = node_name_to_numeric_value[obj["source"]]
	obj["target"] = node_name_to_numeric_value[obj["target"]]	


with open(OUTFILE, 'w') as outfile:
    json.dump(data, outfile)