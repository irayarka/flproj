# flproj

**Lab 6:**

Wrote 38 tests

Tests running:

```
C:\Users\iryna\PycharmProjects\flproj>coverage run -m unittest test_flask.py
......................................
----------------------------------------------------------------------
Ran 38 tests in 65.327s

OK
```

Coverage report:

```
C:\Users\iryna\PycharmProjects\flproj>coverage report -i dbu.py models.py schema.py bprint.py app.py
Name        Stmts   Miss  Cover
-------------------------------
app.py         19      1    95%
bprint.py     153      9    94%
dbu.py         48      2    96%
models.py      33      0   100%
schema.py      46      0   100%
-------------------------------
TOTAL         299     12    96%
```
