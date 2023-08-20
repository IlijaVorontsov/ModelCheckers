# Modelcheckers
Module implementing Bounded Model Checking for the verification of AIGER circuits.
Currently only supports bad state detection (Circuits with one output that is 1 iff the circuit is in a bad state).

### Installation
Install the requirements with `pip install -r requirements.txt`.

### Usage
* Bound Model Checking: `python3 modelcheckers/BoundedModelChecker.py <path-to-aiger-circuit> <bound>`
* Model Checking: `python3 modelcheckers/ModelChecker.py <path-to-aiger-circuit>`

### Examples
* `python3 modelcheckers/BoundedModelChecker.py benchmarks/texas.PI_main%5E02.E.aag 10`
* `python3 modelcheckers/ModelChecker.py benchmarks/vis.emodel.E.aag`