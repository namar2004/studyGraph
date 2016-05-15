from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph
from nodebox.gui import *
import data_setup as su
import networkx as nx

fileN = "data.txt"
#Save to
fileN2 = "Ragas.txt"
colors = [Color(0,0,0), Color(255,0,0), Color(0, 255, 0), Color(0, 0, 255)]
width = 1200
height = 700

# Create a graph with randomly connected nodes.
# Nodes and edges can be styled with fill, stroke, strokewidth parameters.
# Each node displays its id as a text label, stored as a Text object in Node.text.
# To hide the node label, set the text parameter to None.
g = Graph()
G2 = nx.Graph()
#data = su.initialize(fileN)
#G2.add_nodes_from(data)
#nx.write_adjlist(G2, "data2.txt")
G2 = nx.read_adjlist(fileN)

#plot nodes
for drug in G2.nodes():
    classId = su.parseClass(drug)
    g.add_node(id=su.parseName(drug), id2 = classId, radius=8, stroke=color(0), fill=colors[classId - 1],
               text=color(0))

#plot edges
for ed in G2.edges():
    node1 = su.parseName(ed[0])
    node2 = su.parseName(ed[1])
    g.add_edge(node1, node2, length=20.0, weight=1.0, stroke=color(0))

#for edge in G2.edges():

#g.add_edge(node1, node2,
           #length = 1.0,
           #weight = random(),
           #stroke = color(0))

# Two handy tricks to prettify the layout:
# 1) Nodes with a higher weight (i.e. incoming traffic) appear bigger.
for node in g.nodes:
    node.radius = node.radius + node.radius*node.weight*0.5
# 2) Nodes with only one connection ("leaf" nodes) have a shorter connection.
for node in g.nodes:
    if len(node.edges) == 1:
        node.edges[0].length *= 0.1

g.distance         = 25   # Overall spacing between nodes.
g.layout.force     = 0.005 # Strength of the attractive & repulsive force.
g.layout.repulsion = 5   # Repulsion radius.

save = None
zoomed = False
dragged = None
node1 = None
node2 = None
node3 = None
def ntx(nodex):
    name = nodex.id
    if (' ' in name) == True:
        name = name.replace(" ", "_")
    return name+'.'+str(nodex.id2)

def addEdge():
    global node1, node2
    g.add_edge(node1, node2, length=20.0, weight=1.0, stroke=color(0))
    G2.add_edge(ntx(node1), ntx(node2))
    unselect(node1)
    unselect(node2)
    node1 = None
    node2 = None

def addNodeF(ida, idb, fld):
    ids = ida+'.'+idb
    ids = ids.replace(" ", "_")
    print ids
    global node1, node2
    if len(ida)>0 and not zoomed:
        G2.add_node(ids)
        classI = su.parseClass(ids)
        newn2 = g.add_node(id=su.parseName(ids), id2=classI, radius=8, stroke=color(0), fill=colors[classI - 1], text=color(0))
        fld.value = ""
        if node1 and not node2:
            node2 = newn2
            addEdge()
    elif node1 and node2:
        addEdge()

def delNode(ida, fld):
    global node1, node2
    if zoomed:
        return
    if len(ida)>0:
        nodex = g.node(ida)
        if nodex:
            G2.remove_node(ntx(nodex))
            g.remove(nodex)
        fld.value=""
    if node1:
        nodeName1 = node1.id
        if node2:
            nodeName2 = node2.id
            edge1 = g.edge(nodeName1, nodeName2)
            if edge1:
                g.remove(edge1)
                G2.remove_edge(ntx(node1), ntx(node2))
            else:
                print "No edge between these nodes"
            unselect(node2)
            node2 = None
        else:
            G2.remove_node(ntx(node1))
            g.remove(node1)
        unselect(node1)
        node1 = None

def zoom():
    global node1, zoomed, save
    if zoomed:
        g.nodes = save
        save = None
        zoomed = False
    elif not node2 and node1:
        save = g.nodes
        g.nodes = node1.flatten(1)
        zoomed = True
    elif node2 and node1:
        save = g.nodes

def scramble():
    for ed in g.edges:
        #G2.remove_edge(ntx(ed.node1), ntx(ed.node2))
        g.remove(ed)
    for nod in g.nodes:
        nod.x = 0
        nod.y = 0

def select(nod):
    nod.strokewidth = 4

def unselect(nod):
    nod.strokewidth = 1

def save():
    nx.write_adjlist(G2, fileN2)

def on_key_press(cvs, keys):
    global node1, node2
    if keys.char == 'a' and node2 and node1:
        addEdge()
    if keys.code == 'z' and CTRL in keys.modifiers:
        zoom()
    if keys.code == 'p' and CTRL in keys.modifiers:
        cvs.paused = not cvs.paused

def on_mouse_press(canvas, mouse):
    global node1
    global node2
    if canvas.paused:
        canvas.paused = False
    dx = mouse.x - width/2  # Undo translate().
    dy = mouse.y - height/2
    nodex = g.node_at(dx, dy)
    if not nodex:
        return
    # Node pressing is happening here
    # If the first one isn't selected, select it
    if not node1:
        # if it's a node and isn't null, select it
        if nodex is not node2:
            node1 = nodex
            select(node1)
    #for selecting the second item when node1 already exists
    else:
        if nodex is node1:
            unselect(node1)
            node1=node2
            if node1:
                select(node1)
            node2 = None
        elif nodex is node2:
            unselect(node2)
            node2 = None
        else:
            if node2:
                unselect(node2)
            node2 = nodex
            select(node2)

def draw(canvas):

    canvas.clear()
    background(1)
    hsize = height/2
    wsize = width/2
    translate(wsize, hsize)

    # With directed=True, edges have an arrowhead indicating the direction of the connection.
    # With weighted=True, Node.centrality is indicated by a shadow under high-traffic nodes.
    # With weighted=0.0-1.0, indicates nodes whose centrality > the given threshold.
    # This requires some extra calculations.
    g.update(iterations=5)
    g.draw(weighted=True, directed=False)

    # Make it interactive!
    # When the mouse is pressed, remember on which node.
    # Drag this node around when the mouse is moved.
    dx = canvas.mouse.x - wsize  # Undo translate().
    dy = canvas.mouse.y - hsize
    global dragged
    if canvas.mouse.pressed and not dragged:
        dragged = g.node_at(dx, dy)
    if not canvas.mouse.pressed:
        dragged = None
    if dragged:
        dragged.x = dx
        dragged.y = dy

panel = Panel("Add Item", width=200, height=200)
af = Field(value="", hint="")
bf = Field(value="1", hint="")
panel.append(
    Rows(controls=[
        ("Name", af),
        ("ID", bf),
        Button("Add", action=lambda button: addNodeF(af.value, bf.value, af)),
        Button("Delete", action=lambda button: delNode(af.value, af)),
        Button("Scramble", action=lambda button: scramble()),
        #Button("Zoom", action=lambda button: zoom()),
        Button("Save", action=lambda button: save())]))
panel.pack()
canvas.append(panel)
canvas.on_mouse_press = on_mouse_press
canvas.on_key_press = on_key_press
canvas.y = 50
canvas.run(draw)