name = "qrng"

import qiskit
from qiskit import IBMQ
import math
import struct

_circuit = None
_bitCache = ''
def set_provider_as_IBMQ(token):
  global provider
  if token == '':
    provider = qiskit.BasicAer 
  else: 
    IBMQ.save_account(token)
    IBMQ.load_account()
    provider = IBMQ.get_provider('ibm-q')
 
def _set_qubits(n):
    global _circuit
    qr = qiskit.QuantumRegister(n)
    cr = qiskit.ClassicalRegister(n)
    _circuit = qiskit.QuantumCircuit(qr, cr)
    _circuit.h(qr) # Apply Hadamard gate to qubits
    _circuit.measure(qr,cr) # Collapses qubit to either 1 or 0 w/ equal prob.

_set_qubits(8) # Default Circuit is 8 Qubits
 
def set_backend(b = 'qasm_simulator'):
    global _backend
    global provider
    available_backends = provider.backends(b, filters = lambda x: x.status().operational == True)
    if (b is not '') and (b in str(available_backends)):
        _backend = provider.get_backend(b)
    else:
        print(str(b)+' is not available. Backend is set to qasm_simulator.')
        _backend = qiskit.BasicAer.get_backend('qasm_simulator')
    _set_qubits(_backend.configuration().n_qubits)

# Strips QISKit output to just a bitstring.
def _bit_from_counts(counts):
    return [k for k, v in counts.items() if v == 1][0]

# Populates the bitCache with at least n more bits.
def _request_bits(n):
    global _bitCache
    iterations = math.ceil(n/_circuit.width()*2)
    for _ in range(iterations):
        # Create new job and run the quantum circuit
        job = qiskit.execute(_circuit, _backend, shots=1)
        _bitCache += _bit_from_counts(job.result().get_counts())

# Returns a random n-bit string by popping n bits from bitCache.
def get_bit_string(n):
    global _bitCache
    if len(_bitCache) < n:
        _request_bits(n-len(_bitCache))
    bitString = _bitCache[0:n]
    _bitCache = _bitCache[n:]
    return bitString

# Returns a random integer between and including [min, max].
# Running time is probabalistic but complexity is still O(n)
def get_random_int(min,max):
    delta = max-min
    n = math.floor(math.log(delta,2))+1
    result = int(get_bit_string(n),2)
    while(result > delta):
        result = int(get_bit_string(n),2)
    return result+min

# def getRandomIntEntaglement(min,max):

# Returns a random 32 bit integer
def get_random_int32():
    return int(get_bit_string(32),2)

# Returns a random 64 bit integer
def get_random_int64():
    return int(get_bit_string(64),2)

# Returns a random float from a uniform distribution in the range [min, max).
def get_random_float(min,max):
    # Get random float from [0,1)
    unpacked = 0x3F800000 | get_random_int32() >> 9
    packed = struct.pack('I',unpacked)
    value = struct.unpack('f',packed)[0] - 1.0
    return (max-min)*value+min # Scale float to given range

# Returns a random double from a uniform distribution in the range [min, max).
def get_random_double(min,max):
    # Get random double from [0,1)
    unpacked = 0x3FF0000000000000 | get_random_int64() >> 12
    packed = struct.pack('Q',unpacked)
    value = struct.unpack('d',packed)[0] - 1.0
    return (max-min)*value+min # Scale double to given range

# Returns a random complex with both real and imaginary parts
# from the given ranges. If no imaginary range specified, real range used.
def get_random_complex_rect(r1,r2,i1=None,i2=None):
    re = get_random_float(r1,r2)
    if i1 == None or i2 == None:
        im = get_random_float(r1,r2)
    else:
        im = get_random_float(i1,i2)
    return re+im*1j

# Returns a random complex in rectangular form from a given polar range.
# If no max angle given, [0,2pi) used.
def get_random_complex_polar(r,theta=2*math.pi):
    r0 = r * math.sqrt(get_random_float(0,1))
    theta0 = get_random_float(0,theta)
    return r0*math.cos(theta0)+r0*math.sin(theta0)*1j
