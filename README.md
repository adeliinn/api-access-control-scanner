# api-access-control-scanner
Automated detection of broken access control vulnerabilities in REST APIs

## Python scanner in PyCharm

The scanner is in `scanner/main.py`. Open the repository root in PyCharm, enable
the Python plugin, and configure a Python 3 interpreter in **Settings >
Project > Python Interpreter**. PyCharm will then detect Python files and the
shared **BOLA Scanner** run configuration will be available.

The scanner uses only the Python standard library. Its test settings are in
`scanner/config/bola-test-config.json`.
