class Datum(object):
    def __init__(self, value, type):
        self.value = value
        if type not in ["char", "short", "int", "float"]:
            raise Exception
        self.type = type
        if self.type == "char":
            self.size = 1
        elif self.type == "short":
            self.size = 2
        elif self.type == "int" or self.type == "float":
            self.size = 4

    def __str__(self):
        return self.type + ":" + str(self.value)
