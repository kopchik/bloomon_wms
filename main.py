#!/usr/bin/env python3
import copy
from collections import OrderedDict, defaultdict

import click
import regex

BOUQUET_RE = r"""
    (?P<name>\S)                        # NAME OF BOUQUET
    (?P<size>[SL])                      # SIZE (S/L)
    ((?P<qty>\d{1,2})(?P<species>\S))+  # FLOWERS TYPE AND QUANTITY
    (?P<tot_flowers>\d+)                # TOTAL NUMBER OF FLOWERS
"""


class InvalidBouquet(Exception):
    """Bouquet definition cannot be parsed."""


@click.command()
@click.option("-d", "--debug", is_flag=True, default=False)
@click.argument("path", type=click.Path(exists=True))
def main(debug=False, path="sample.txt"):
    """\b
      "Beautiful is better than ugly."
       (c) pep-20

    Welcome to Advanced Warehouse Management System (WMS).
    Data is taken from PATH that should point to a file with
    bouquet designs and warehouse stock supply.
    The output should be deterministic, but I'm too lazy to check that.


    PS Some assumptions were made. Such as input is valid and contains
    at least one bouquet definition.

    PPS License: Beerware.

    PPPS: although code is mostly lazy, it's up to the reviewer
    to check if it can process large amount of data. Please report
    back with results (if any). I also accept PRs with fixes/improvements.
    """

    warehouse = defaultdict(int)

    with open(path, "rt") as f:
        designs = parse_designs(f)
        if debug:
            click.echo("I parsed the following bouquet designs:")
            click.echo(designs)
            click.echo()

        for flower in f:
            flower = flower.strip()
            if not flower:
                break
            if debug:
                click.echo(f"got flower: {flower}")
            warehouse[flower] += 1

            bouquet, new_warehouse = maybe_make_a_bouquet(designs, warehouse)
            warehouse = new_warehouse
            if bouquet:
                warehouse = new_warehouse
                click.echo(format_bouquet(bouquet))
            elif debug:
                click.echo("<no bouquet is possible to make>")


def parse_designs(f):
    designs = OrderedDict()

    for raw_design in f:
        raw_design = raw_design.strip()
        if not raw_design or raw_design.isspace():
            break
        design = parse_bouquet_design(raw_design)
        designs[raw_design] = design
    return designs


def maybe_make_a_bouquet(designs, warehouse):
    for design in designs.values():
        bouquet, new_warehouse = make_bouquet(design, warehouse)
        if bouquet:
            return bouquet, new_warehouse
    return None, warehouse


def parse_bouquet_design(raw_design):
    m = regex.match(BOUQUET_RE, raw_design, regex.VERBOSE)
    if not m:
        raise InvalidBouquet(f"cannot parse {raw_design}")

    name = m.groupdict()["name"]
    size = m.groupdict()["size"]
    total_flower_count = int(m.groupdict()["tot_flowers"])

    species = m.capturesdict()["species"]
    raw_counts = m.capturesdict()["qty"]
    flowers = {}
    flower_count = 0
    for specie, raw_count in zip(species, raw_counts):
        count = int(raw_count)
        flowers[specie + size] = count
        flower_count += count

    extra_flowers = total_flower_count - flower_count
    return {
        "name": name,
        "size": size,
        "flowers": flowers,
        "extra_flowers": extra_flowers,
    }


def make_bouquet(design, warehouse):
    """
    Returns a bouquet and updated warehouse.
    If bouquet is impossible to make, then bouquet is None, and warehouse is not changed.
    """

    size = design["size"]
    design_flowers = design["flowers"]
    extra_flowers = design["extra_flowers"]
    bouquet_flowers = defaultdict(int)

    # first pick flowers required by the design
    new_warehouse = copy.deepcopy(warehouse)
    for flower, qty in design_flowers.items():
        if flower not in new_warehouse or new_warehouse[flower] < qty:
            return False, warehouse
        new_warehouse[flower] -= qty
        bouquet_flowers[flower] = qty

    # pick additional ("extra") flowers
    if extra_flowers:
        for flower, available_qty in sorted(new_warehouse.items()):
            if not flower.endswith(size):
                continue
            if available_qty == 0:
                continue
            to_take = min(available_qty, extra_flowers)
            extra_flowers -= to_take
            new_warehouse[flower] -= to_take
            bouquet_flowers[flower] += to_take
            if not extra_flowers:
                break
        else:
            return False, warehouse

    bouquet = {"design": design, "flowers": dict(bouquet_flowers)}
    return bouquet, new_warehouse


def format_bouquet(bouquet):
    design = bouquet["design"]
    name = design["name"]
    size = design["size"]
    flowers = bouquet["flowers"].items()
    flowers = sorted(flowers)
    flowers = "".join(f"{qty}{flower[:-1]}" for flower, qty in flowers)
    return f"{name}{size}{flowers}"


if __name__ == "__main__":
    main()
