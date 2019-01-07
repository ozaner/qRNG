<p align="center">
  <img src="qRNG.png" width="475px"/>
</p>

-----------------

**qRNG** is a python package that generates truly random numbers via quantum mechanics. It does this by using IBM's [**QISKit**](https://qiskit.org/) API to communicate with any one of their 3 publicly accessible quantum computers.

<!-- ### Installation
You can use the pip package manager to install the current release of qRNG (along with its dependencies):
```
pip install qrng
```

Upgrading is as simple as:
```
pip install qrng -U
``` -->

### What is Random Number Generation?
There are a variety of applications that require a source of random data in order to work effectively such as simulations or cryptography. To that end, we use random number generators (RNGs) to generate sequences of numbers that are, ideally, indistinguishable from random noise.

There are two types of RNGs: Pseudo-RNGs (PRNGs) and True RNGs (TRNGs). Pseudo-RNGs, while not truly and statistically random, are used in a variety of applications as their random numbers are 'random enough' for many purposes.

For a True RNGs, however, an actual piece of hardware is required to measure some random process in the real world as no deterministic computer program could do the same. These devices vary from pieces of radioactive isotopes connected via USB to apparatuses that measure atmospheric noise.

### Why Quantum?
Modern physics has shown us that there are really only two types of events that can happen in the universe: the unitary transformation of a quantum system, and quantum wavefunction collapse (i.e. **measurement**). The former being a totally deterministic process and the latter being a random one.

Indeed, all randomness in the universe (as far we know) is the result of the collapse of quantum systems upon measurement. In a sense this is the truest form of randomness and the underlying source of it any TRNG.

The point of this package then, besides it being a fun side project, is to cut out the middle man entirely, whether it be a radioactive isotope with a known half-life or measuring the thermal noise in your PC, and simply measure an actual quantum system. For example:

<p align="center">
  <img src="https://latex.codecogs.com/png.latex?\dpi{150}&space;\left|{\psi}\right\rangle&space;=\frac{1}{\sqrt&space;2}\left|{0}\right\rangle&space;&plus;\frac{1}{\sqrt&space;2}\left|{1}\right\rangle" title="\left|{\psi}\right\rangle =\frac{1}{\sqrt 2}\left|{0}\right\rangle +\frac{1}{\sqrt 2}\left|{1}\right\rangle" />
</p>

There is a 50-50 chance of measuring the above system as a 0 or 1 and we continually iterate this measurement for as many random bits as we require.

### Practicality
Of course, while the numbers generated from a quantum computer are amongst the most random, the practicality of connecting to one IBM's quantum computers for a large amount of said numbers is nonexistent. For most real world use cases that require such high-caliber random numbers, an off the shelf hardware RNG would suffice.
