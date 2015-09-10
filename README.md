# upversion
Release python packages with ease

Operate with package version numbers.
Parse the version, increment it and save it.

```
python setup.py --version
0.1.0

upversion up --major
From 0.1.0 to 1.0.0
Writing setup.py

python setup.py --version
1.0.0
```

Supports python versions 2.7, 3.3 and 3.4

## Development

To run the tests install ``tox`` and run it:

```
pip install tox
tox
```
