# WAREHOUSE MANAGEMENT SYSTEM FOR BLOOMON

## Quickstart


```
make image && make run-example-in-container
```

Read data from stdin: `cat ./sample.txt | ./main.py /dev/stdin`

## Options and flags

```
Usage: main.py [OPTIONS] PATH

    "Beautiful is better than ugly."
     (c) pep-20

  Welcome to Advanced Warehouse Management System (WMS). Data is taken from
  PATH that should point to a file with bouquet designs and warehouse stock
  supply. The output should be deterministic, but I'm too lazy to check
  that.

  PS Some assumptions were made. Such as input is valid and contains at
  least one bouquet definition.

  PPS License: Beerware.

  PPPS: although code is mostly lazy, it's up to the reviewer to check if it
  can process large amount of data. Please report back with results (if
  any). I also accept PRs with fixes/improvements.

Options:
  -d, --debug
  --help       Show this message and exit.
```
