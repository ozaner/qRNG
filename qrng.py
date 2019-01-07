import qiskit
import math
import struct

## Initialize Quantum Circuit w/ 1 qubit
# All qubits start at |0> state
qr = qiskit.QuantumRegister(1)
cr = qiskit.ClassicalRegister(1)
circuit = qiskit.QuantumCircuit(qr, cr)

## Create Quantum Circuit
# |0> --> H|0>=(|0>+|1>)/sqrt(2) --> Measure 50% |0>, 50% |1>
circuit.h(qr[0]) # Apply Hadamard gate to qubit
circuit.measure(qr,cr) # Collapses qubit to either 1 or 0 w/ equal prob.

# Strips QISKit ouput to just the output bit.
def bit_from_counts(counts):
    return [k for k, v in counts.items() if v == 1][0]

# Returns a random n-bit string
def getBitString(n):
    bitString = ''
    for _ in range(n):
        # Create new job and run the quantum circuit
        job = qiskit.execute(circuit, qiskit.BasicAer.get_backend('qasm_simulator'), shots=1)
        bitString += bit_from_counts(job.result().get_counts())
    return bitString

## Returns a random integer between and including [min, max].
# Running time is probabalistic but complexity is still O(n)
def getRandomInt(min,max):
    delta = max-min
    n = math.floor(math.log(delta,2))+1
    result = int(getBitString(n),2)
    while(result > delta):
        result = int(getBitString(n),2)
    return result+min

# def getRandomIntEntaglement(min,max):

# Returns a random 32 bit integer
def getRandomInt32():
    return int(getBitString(32),2)

# Returns a random 64 bit integer
def getRandomInt64():
    return int(getBitString(64),2)

# Returns a random float from a uniform distribution in the range [min, max).
def getRandomFloat(min,max):
    # Get random float from [0,1)
    binaryVal = 0x3F800000 | getRandomInt32() >> 9
    binaryRep = struct.pack('I',binaryVal)
    floatVal = struct.unpack('f',binaryRep)[0] - 1.0
    # Scale float to given range
    delta = max-min
    return delta*floatVal+min

# Returns a random double from a uniform distribution in the range [min, max).
def getRandomDouble(min,max):
    # Get random double from [0,1)
    binaryVal = 0x3FF0000000000000 | getRandomInt64() >> 12
    binaryRep = struct.pack('Q',binaryVal)
    floatVal = struct.unpack('d',binaryRep)[0] - 1.0
    # Scale double to given range
    delta = max-min
    return delta*floatVal+min

# Print results
print(getRandomDouble(0,1))
