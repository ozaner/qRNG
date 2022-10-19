import qiskit
from qiskit import IBMQ
import math
import struct

_circuit = None
_bitCache = ''
def set_provider_as_IBMQ(token: str = None):
    """
    Sets the backend provider to IBMQ with the given account token. Will fall back to a local (simulated) provider if no token is given.

    Parameters:
        token (string): Account token on IBMQ. If no token is given, will fall back to a local provider.
    """
    global provider
    if token == None or '':
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
 
def set_backend(backend: str = 'qasm_simulator'):
    """
    Sets the backend to one of the provider's available backends (quantum computers/simulators).

    Parameters:
        backend (string): Codename for the backend. If no backend is given, a default (simulated) backend will be used.
    """
    global _backend
    global provider
    available_backends = provider.backends(backend, filters = lambda x: x.status().operational == True)
    if (backend != '') and (backend in str(available_backends)):
        _backend = provider.get_backend(backend)
    else:
        print(str(backend)+' is not available. Backend is set to qasm_simulator.')
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

def get_bit_string(n: int) -> str:
    """
    Returns a random n-bit bitstring.

    Parameters:
        n (int): Account token on IBMQ. If no token is given, will fall back to a local provider.
    """
    global _bitCache
    if len(_bitCache) < n:
        _request_bits(n-len(_bitCache))
    bitString = _bitCache[0:n]
    _bitCache = _bitCache[n:]
    return bitString

# Running time is probabalistic but complexity is still O(n)
def get_random_int(min: int, max: int) -> int:
    """
    Returns a random int from [min, max] (bounds are inclusive).

    Parameters:
        min (int): The minimum possible returned integer.
        max (int): The maximum possible returned integer.
    """
    delta = max-min
    n = math.floor(math.log(delta,2))+1
    result = int(get_bit_string(n),2)
    while(result > delta):
        result = int(get_bit_string(n),2)
    result += min
    return result

# def getRandomIntEntaglement(min,max):

def get_random_int32() -> int:
    """Returns a uniformly random 32 bit integer."""
    return int(get_bit_string(32),2)

def get_random_int64() -> int:
    """Returns a uniformly random 64 bit integer."""
    return int(get_bit_string(64),2)

def get_random_float(min: float = 0, max: float = 1) -> float:
    """
    Returns a uniformly random single-precision float from the range [min,max).

    Parameters:
        min (float): The minimum possible returned float (inclusive). Default is 0.0
        max (float): The maximum possible returned float (exclusive). Default is 1.0

    Algorithm provided by: https://experilous.com/1/blog/post/perfect-fast-random-floating-point-numbers.
    """
    unpacked = 0x3F800000 | get_random_int32() >> 9
    packed = struct.pack('I',unpacked)
    value = struct.unpack('f',packed)[0] - 1.0
    return (max-min)*value+min # Scale float to given range

def get_random_double(min: float = 0, max: float = 1) -> float:
    """
    Returns a uniformly random double-precision float from the range [min,max).

    Parameters:
        min (float): The minimum possible returned double (inclusive). Default is 0.0
        max (float): The maximum possible returned double (exclusive). Default is 1.0

    Algorithm provided by: https://experilous.com/1/blog/post/perfect-fast-random-floating-point-numbers.
    """
    unpacked = 0x3FF0000000000000 | get_random_int64() >> 12
    packed = struct.pack('Q',unpacked)
    value = struct.unpack('d',packed)[0] - 1.0
    return (max-min)*value+min # Scale double to given range

# Returns a random complex with both real and imaginary parts
# from the given ranges. If no imaginary range specified, real range used.
def get_random_complex_rect(real_min: float = 0, real_max: float = 0, img_min: float | None = None, img_max: float | None = None) -> complex:
    """
    Returns a random complex number with:
        Real-part: a uniformly sampled single-precision float from the range [real_min,real_max).
        Imaginary-part: a uniformly sampled single-precision float from the range [img_min,img_max).

    Parameters:
        real_min (float): The minimum possible real component (inclusive). Default is 0.
        real_max (float): The maximum possible real component (exclusive). Default is 1.
        img_min (float): The minimum possible imaginary component (inclusive). If unspecified, will default to real_min.
        img_max (float): The maximum possible imaginary component (exclusive). If unspecified, will default to real_max.
    """
    if img_min is None:
        img_min = real_min
    if img_max is None:
        img_max = real_max
    re = get_random_float(real_min,real_max)
    im = get_random_float(img_min,img_min)
    return re+im*1j

def get_random_complex_polar(r: float = 1, theta: float = 2*math.pi) -> complex:
    """
    Returns a random complex uniformly sampled from an arc sweeping across the complex plane, starting at theta = 0.

    Parameters:
        r (float): The radius of the arc being sampled. Default is 1.
        theta (float): The ending angle of the arc.
    """
    r0 = r * math.sqrt(get_random_float(0,1))
    theta0 = get_random_float(0,theta)
    return r0*math.cos(theta0)+r0*math.sin(theta0)*1j
