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


def parseName(line):
    index = line.index('.')
    name = line[0:index]
    if ('_' in name) == True:
        index2 = line.index('_')
        name = line[0:index2] + " " + line[index2+1:index]
    return name

def parseClass(line):
    index = line.index('.')
    return int(line[index+1:])