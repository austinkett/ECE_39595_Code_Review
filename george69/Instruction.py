class Instruction(object):
    def __init__(self, numericalInstruction):
        self.instruction = self.getInstruction(numericalInstruction)
        self.numericalInstruction = numericalInstruction
    def getInstruction(self, numericalInstruction):
        instructionSet = {
            132: "cmpe",
            136: "cmplt",
            140: "cmpgt",
            36 : "jmp",
            40 : "jmpc",
            44 : "call",
            48 : "ret",
            68 : "pushc",
            69 : "pushs",
            70 : "pushi",
            71 : "pushf",
            72 : "pushvc",
            73 : "pushvs",
            74 : "pushvi",
            75 : "pushvf",
            76 : "popm",
            77 : "popa",
            80 : "popv",
            84 : "peekc",
            85 : "peeks",
            86 : "peeki",
            87 : "peekf",
            88 : "pokec",
            89 : "pokes",
            90 : "pokei",
            91 : "pokef",
            94 : "swp",
            100: "add",
            104: "sub",
            108: "mul",
            112: "div",
            144: "printc",
            145: "prints",
            146: "printi",
            147: "printf",
            0  : "halt"
        }
        return instructionSet.get(numericalInstruction)
    def __str__(self):
        return str(self.instruction)
