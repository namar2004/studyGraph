#A relic from the old times - no longer opening files on my own
def initialize(filename):
    with open(filename) as f:
        lines = []
        if f is None:
            print("Invalid file")
            return None
        print("Success!")
        for line in f:
            lines.append(line.strip())
        return lines

#gets the name up to the '.' and also removes _, which
#are necessary for the NetworkX integration. It doesn't
#like spaces in the node name
def parseName(line):
    index = line.index('.')
    name = line[0:index]
    if ('_' in name) == True:
        index2 = line.index('_')
        name = line[0:index2] + " " + line[index2+1:index]
    return name

#Finds the '.' to give back the type of node
def parseClass(line):
    index = line.index('.')
    return int(line[index+1:])