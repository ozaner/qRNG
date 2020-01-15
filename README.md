<p align="center">
  <img src="https://github.com/ozanerhansha/qRNG/blob/master/qRNG.png?raw=true" width="500px"/>
</p>

-----------------

**qRNG** is an open-source quantum random number generator written in python. It achieves this by using IBM's [QISKit](https://qiskit.org/) API to communicate with any one of their publicly accessible quantum computers:

- `ibmq_armonk` 1 qubit
- `ibmq_london` 5 qubits
- `ibmq_burlington` 5 qubits
- `ibmq_essex` 5 qubits
- `ibmq_ourense` 5 qubits
- `ibmq_vigo` 5 qubits
- `ibmqx2` 5 qubits
- `ibmq_qasm_simulator` 32 qubits (simulated)
- `qasm_simulator` 8 qubits (simulated)

Note that you need to input your IBMQ API token to access any of these quantum computers/simulators except for the last one `qasm_simulator`.

## Installation
You can use the pip package manager to install the [current release](https://pypi.org/project/qrng/) of qRNG (along with its dependencies):
```
pip install qrng
```

Upgrading is as simple as:
```
pip install qrng -U
```
## Tutorial
Now you can try generating your first random number. First open python in the shell or use an IDE:
```shell
$ python
```
Now try generating a random 32-bit integer:
```python
>>> import qrng
>>> qrng.set_provider_as_IBMQ('YOUR_IBMQ_TOKEN_HERE')
>>> qrng.set_backend('ibmq_london')
>>> qrng.get_random_int32()
3834878552
```

If you don't need or want to use IBM's actual quantum computers, you can instead just use the default backend like so:
```python
>>> import qrng
>>> qrng.set_provider_as_IBMQ('') #empty string denotes default backend
>>> qrng.set_backend() #defaults to `qasm_simulator`
>>> qrng.get_random_int32()
2760805561
```

<!-- For a more detailed tutorial, including connecting to quantum hardware, click here. -->

## What is Random Number Generation?
There are a variety of applications that require a source of random data in order to work effectively (e.g. simulations and cryptography). To that end, we make use of random number generators (RNGs) to generate sequences of numbers that are, ideally, indistinguishable from random noise.

There are two types of RNGs: Pseudo-RNGs (PRNGs) and True RNGs (TRNGs). Pseudo-RNGs, while not truly and statistically random, are used in a variety of applications as their output is 'random enough' for many purposes.

For a True RNG, however, an actual piece of hardware is required to measure some random process in the real world as no computer program could suffice due to being deterministic in nature. These devices vary from apparatuses that measure atmospheric noise to pieces of radioactive material connected via USB.

## Why Quantum?
Modern physics has shown us that there are really only two types of events that can happen in the universe: the unitary transformation of a quantum system, and quantum wavefunction collapse (i.e. **measurement**). The former being a totally deterministic process and the latter being a random one.

Indeed, all randomness in the universe (as far we know) is the result of the collapse of quantum systems upon measurement. In a sense, this is randomness in its purest form and the underlying source of it in any TRNG.

The point of this package then, besides it being a fun side project, is to cut out the middle man entirely, whether it be a radioactive isotope or the thermal noise in your PC, and simply measure an actual quantum system. For example, we can prepare the following state in a quantum computer:

<p align="center">
  <img src="https://latex.codecogs.com/png.latex?\dpi{150}&space;\left|{\psi}\right\rangle&space;=\frac{1}{\sqrt&space;2}\left|{0}\right\rangle&space;&plus;\frac{1}{\sqrt&space;2}\left|{1}\right\rangle" title="\left|{\psi}\right\rangle =\frac{1}{\sqrt 2}\left|{0}\right\rangle +\frac{1}{\sqrt 2}\left|{1}\right\rangle" />
</p>

There is a 50-50 chance of measuring the above state as a 0 or 1 and we can continually iterate this process for as many random bits as we require. Note that while such a simple algorithm doesn't require a full-blown quantum computer, there are some random algorithms that do.

## Practicality
Of course, while the numbers generated from a quantum computer are amongst the most random, the practicality of connecting to one of IBM's quantum computers to generate a large amount of these numbers is nonexistent. For most real world use cases that require such high-caliber random numbers, an off the shelf hardware RNG would suffice. The purpose of this package is thus to provide a working example of how a real cloud based quantum random number generator may operate.
