from Instruction import Instruction
from Datum import Datum
import struct
import sys
import filecmp
class Interpreter(object):
    def __init__(self):
        self.rstack = [] #list of Datum
        self.sp = -1
        self.fpstack = []
        self.fpsp = -1
        self.pc = 0
        self.mem = [] ##list of bytes
        self.availableInstructions = {
            "cmpe": self.cmpe,
            "cmplt": self.cmplt,
            "cmpgt": self.cmpgt,
            "jmp": self.jmp,
            "jmpc": self.jmpc,
            "call": self.call,
            "ret": self.ret,
            "pushc": self.pushc,
            "pushs": self.pushs,
            "pushi": self.pushi,
            "pushf": self.pushf,
            "pushvc": self.pushvc,
            "pushvs": self.pushvs,
            "pushvi": self.pushvi,
            "pushvf": self.pushvf,
            "popm": self.popm,
            "popa": self.popa,
            "popv": self.popv,
            "peekc": self.peekc,
            "peeks": self.peeks,
            "peeki": self.peeki,
            "peekf": self.peekf,
            "pokec": self.pokec,
            "pokes": self.pokes,
            "pokei": self.pokei,
            "pokef": self.pokef,
            "swp": self.swp,
            "add": self.add,
            "sub": self.sub,
            "mul": self.mul,
            "div": self.div,
            "printc": self.printc,
            "prints": self.prints,
            "printi": self.printi,
            "printf": self.printf,
            "halt": self.halt
        }

    def loadProgram(self, fileName):
        with open(fileName, "rb") as fp:
            self.mem = bytearray(fp.read())
    def executeProgram(self):
        try:
            while True:
                instruction = Instruction(self.mem[self.pc])
                ##print(instruction.numericalInstruction)
                #print(instruction.instruction)
                #print(self.pc)
                fun = self.availableInstructions.get(instruction.instruction)
                fun()
                #print([str(d) for d in self.rstack])
                if instruction.instruction == "halt":
                    break
        except Exception as e:
            print("ERROR OCCURED, DUMPING")
            print(e)
            self.halt()

    def halt(self):
        print()
        print("Compile values:")
        print(str(self), end="")

    def call(self):
        #self.halt()
        self.fpsp += 1
        self.fpstack.insert(self.fpsp, self.sp - self.rstack[self.sp].value - 1)
        del self.rstack[self.sp]
        self.sp -= 1
        self.pc = self.rstack[self.sp].value
        #print("GOTO " + str(self.rstack[self.sp].value))
        del self.rstack[self.sp]
        #print(str([str(d.value) for d in self.rstack]))
        #print("PC: " + str(self.pc))
        #del self.rstack[self.sp]
        self.sp -= 1
        #print(self.fpstack)

    def ret(self):
        #print([str(d) for d in self.rstack])
        self.sp = self.fpstack[self.fpsp]
        #print(self.sp)
        del self.fpstack[self.fpsp]
        self.fpsp -= 1
        self.pc = self.rstack[self.sp].value
        del self.rstack[self.sp]
        self.sp -= 1

    def jmp(self):
        self.pc = self.rstack[self.sp].value
        del self.rstack[self.sp]
        self.sp -= 1

    def jmpc(self):
        if self.rstack[self.sp - 1].value == 1:
            self.pc = self.rstack[self.sp].value
        else:
            self.pc += 1
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.sp -= 2

    def pushc(self):
        data = Datum(self.mem[self.pc+1], "char")
        self.sp += 1
        self.rstack.insert(self.sp, data)
        self.pc += data.size
        self.pc += 1

    def pushs(self):
        data = Datum(int.from_bytes(bytearray(self.mem[self.pc + 1:self.pc + 3]), byteorder="little"), "short")
        self.sp += 1
        self.rstack.insert(self.sp, data)
        self.pc += data.size
        self.pc += 1

    def pushi(self):
        data = Datum(int.from_bytes(bytearray(self.mem[self.pc + 1:self.pc + 5]), byteorder="little"), "int")
        #print(data.value)
        self.sp += 1
        self.rstack.insert(self.sp, data)
        self.pc += data.size
        self.pc += 1

    def pushf(self):
        data = Datum(struct.unpack("<f", bytearray(self.mem[self.pc+1:self.pc + 5]))[0], "float")
        self.sp += 1
        self.rstack.insert(self.sp, data)
        self.pc += data.size
        self.pc += 1

    def pushvi(self):
        self.rstack[self.sp] = self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        #self.sp += 1
        self.pc += 1

    def pushvc(self):
        self.rstack[self.sp] = self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        self.pc += 1

    def pushvs(self):
        self.rstack[self.sp] = self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        self.pc += 1

    def pushvf(self):
        self.rstack[self.sp] = self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        self.pc += 1

    def popa(self):
        numToKeep = self.rstack[self.sp].value
        del self.rstack[self.sp]
        self.sp -= 1
        tempStack = []
        for i in range(numToKeep):
            tempStack = self.rstack[self.sp - numToKeep:self.sp]
        #print([str(d) for d in self.rstack])
        numToPop = self.sp - self.fpstack[self.fpsp]
        #print(numToPop)
        for i in range(numToPop):
            del self.rstack[self.sp]
            self.sp -= 1
        self.pc += 1

    def popm(self):
        numToPop = self.rstack[self.sp].value + 1
        for i in range(numToPop):
            del self.rstack[self.sp]
            self.sp -= 1
        self.pc += 1

    def popv(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1].value = self.rstack[self.sp - 1].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.sp -= 2
        self.pc += 1

    def peekc(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1] = self.rstack[
            self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.sp -= 2
        self.pc += 1

    def peeks(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1] = self.rstack[
            self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.sp -= 2
        self.pc += 1

    def peeki(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1] = self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.sp -= 2
        self.pc += 1

    def peekf(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1] = self.rstack[
            self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1]
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.sp -= 2
        self.pc += 1

    def cmpe(self):
        t1 = self.rstack[self.sp - 1].value
        t2 = self.rstack[self.sp].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.rstack.insert(self.sp - 1, Datum(1 if t1 == t2 else 0, "int"))
        self.sp -= 1
        self.pc += 1

    def cmplt(self):
        t1 = self.rstack[self.sp - 1].value
        t2 = self.rstack[self.sp].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.rstack.insert(self.sp - 1, Datum(1 if t1 < t2 else 0, "int"))
        self.sp -= 1
        self.pc += 1

    def cmpgt(self):
        t1 = self.rstack[self.sp - 1].value
        t2 = self.rstack[self.sp].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.rstack.insert(self.sp - 1, Datum(1 if t1 > t2 else 0, "int"))
        self.sp -= 1
        self.pc += 1

    def add(self):
        t1 = self.rstack[self.sp - 1].value
        t2 = self.rstack[self.sp].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.rstack.insert(self.sp - 1,
                               Datum(t1 + t2, "int"))
        self.sp -= 1
        self.pc += 1

    def sub(self):
        t1 = self.rstack[self.sp - 1].value
        t2 = self.rstack[self.sp].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.rstack.insert(self.sp - 1,
                           Datum(t1 - t2, "int"))
        self.sp -= 1
        self.pc += 1

    def mul(self):
        t1 = self.rstack[self.sp - 1].value
        t2 = self.rstack[self.sp].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.rstack.insert(self.sp - 1,
                           Datum(t1 * t2, "int"))
        self.sp -= 1
        self.pc += 1

    def div(self):
        t1 = self.rstack[self.sp - 1].value
        t2 = self.rstack[self.sp].value
        del self.rstack[self.sp]
        del self.rstack[self.sp - 1]
        self.rstack.insert(self.sp - 1,
                           Datum(t1 / t2, "int"))
        self.sp -= 1
        self.pc += 1

    def printc(self):
        print(int(self.rstack[self.sp].value))
        del self.rstack[self.sp]
        self.sp -= 1
        self.pc += 1

    def prints(self):
        print(int(self.rstack[self.sp].value))
        del self.rstack[self.sp]
        self.sp -= 1
        self.pc += 1

    def printi(self):
        print(int(self.rstack[self.sp].value))
        del self.rstack[self.sp]
        self.sp -= 1
        self.pc += 1

    def printf(self):
        print(self.rstack[self.sp].value)
        del self.rstack[self.sp]
        self.sp -= 1
        self.pc += 1

    def swp(self):
        self.rstack[self.sp - 1], self.rstack[self.sp] = self.rstack[self.sp], self.rstack[self.sp - 1]
        self.pc += 1

    def pokec(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1] = self.rstack[
            self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1]
        self.pc += 1

    def pokes(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1] = self.rstack[
            self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1]
        self.pc += 1

    def pokei(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1] = self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1]
        self.pc += 1

    def pokef(self):
        self.rstack[self.fpstack[self.fpsp] + self.rstack[self.sp].value + 1] = self.rstack[
            self.fpstack[self.fpsp] + self.rstack[self.sp - 1].value + 1]
        self.pc += 1

    def __str__(self):
        buff = ""
        buff += "PC: " + str(self.pc) + "\n"
        buff += "sp: " + str(self.sp) + "\n"
        buff += "rstack: "
        buff += "empty" if len(self.rstack) == 0 else str([str(d) for d in self.rstack])
        buff += "\n"
        buff += "fpsp: " + str(self.fpsp) + "\n"
        buff += "fpstack: "
        buff += "empty" if len(self.fpstack) == 0 else str(self.fpstack)
        return buff

if __name__ == "__main__":

    sys.stdout = open("TestOutputs/BasicsOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Basics.bin")
    interpreter.executeProgram()

    sys.stdout = open("TestOutputs/ComparisonsOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Comparisons.bin")
    interpreter.executeProgram()

    sys.stdout = open("TestOutputs/Interpreter_InputOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Interpreter_Input.bin")
    interpreter.executeProgram()

    sys.stdout = open("TestOutputs/JumpsOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Jumps.bin")
    interpreter.executeProgram()

    sys.stdout = open("TestOutputs/MathOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Math.bin")
    interpreter.executeProgram()

    sys.stdout = open("TestOutputs/Peek_PokeOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Peek_Poke.bin")
    interpreter.executeProgram()

    sys.stdout = open("TestOutputs/Push_PopOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Push_Pop.bin")
    interpreter.executeProgram()

    sys.stdout = open("TestOutputs/SubroutinesOutput.txt", "w")
    interpreter = Interpreter()
    interpreter.loadProgram("Test_Binaries/Subroutines.bin")
    interpreter.executeProgram()
