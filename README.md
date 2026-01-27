# Confuser #

Confuser is a database noise simulator, designed to make “clean vanilla” simulated patient data (eg. data produced by Synthea) into a more realistic representation of real-world healthcare data (RWD). 
Confuser is intended for methodological reasearch only and should not be used for de-identification of patient data.

### Pre-requisites

* Python (version 3+)
* pip
* requirements:

```bash
pip install -r requirements.txt
```

[Virtual environments](https://docs.python-guide.org/dev/virtualenvs/) are recommended

### Unit Tests

See [here](https://docs.python.org/3/library/unittest.html) for guidelines on how to write 
unit tests.

The following assume _python_ is pointing to python version 3.

To run all unit tests:

```bash
python -m unitttest discover -v tests/unit
```

To run a specific test file:

```bash
python -m unittest -v tests/unit/test_confuser.py
```

### Execution

```bash
python -m confuser.main
```

### Authors

* Guy Tsafnat, [Evidentli](http://evidentli.com)
