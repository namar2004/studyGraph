README.md


# Javascript Version

## Running it
1. Navitage into the directory where `studyGraph.html` lives
2. Run the command 
`$ python -m SimpleHTTPServer`
3. visit http://0.0.0.0:8000/ in your browser, and observe the webpage!


## Making more data
1. **Make a data file in data/concretions** specifying the nodes and the connetions between them.  Specifically, it should be a json file containing two keys:
    1. `'nodes'`: a list of all nodes (including those unconnected to other nodes), with their names and groups (groups are used to assign colors to nodes).  As an example: 
       `{"group": 2, "name": "Haloperidol"}`
    2. `'links'`: a list of all links between nodes.  The nodes must already have been defined in `'nodes'`.  The value field is not important..._yet_.  (The thickness of the line representing the link between two nodes is proportional to this value).  As an example: 
`{"source": "Haloperidol", "target": "Antipsychotic", "value": 1}`
for notational consistency, append `human_readable` to the end of the filename
2. **Convert it to numericized file** using `extraneous_scripts/numericize_graph_json.py` by changing the `INFILE` and `OUTFILE` variables.  The only thing this script does it replace node names with indices, e.g. converting 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `{"source": "Haloperidol", "target": "Antipsychotic", "value": 1}`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;to 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `{"source": 0, "target": 25, "value": 1}`

3. **Make a file in data/abstractions that specifies display parameters specific** to these data, e.g. node size and charge

## Next Steps
* Expand the datasets!
* Make it so you can click on a node and zoom in on it (http://stackoverflow.com/questions/25225069/zooming-to-a-clicked-node-on-a-d3-force-directed-graph , https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=d3%20click%20on%20node%20and%20zoom%20in)
* Make it so you can click on a node and see information about it?}
* Allow the charge etc. to be specified by the uservia the interface?
* Allow the abstract files to specify the color scheme etc.
* Improve documentation on the javascript because who really knows how d3 works

# Python Version


## Dependencies

* nodebox
* networkx

## Errors

* _KeyError: 'panel'_ This could have happened because you used pip to install nodebox.  Go to https://github.com/nodebox/nodebox-opengl and download that folder.  Copy the theme folder from nodebox/gui into your own /Users/<username>/anaconda/lib/python2.7/site-packages/nodebox/gui/, or wherever your nodebox is installed.  

