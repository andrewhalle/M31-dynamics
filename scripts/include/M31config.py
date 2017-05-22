class Config:
    def __init__(self, filename):
        file = open(filename, "r")
        line = file.readline()
        while line:
            items = line.split(":")
            for i in range(len(items)):
                items[i] = items[i].strip()
            exec("self." + items[0] + " = " + items[1])
            line = file.readline()
