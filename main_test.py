import textwrap
from collections import defaultdict

from click.testing import CliRunner

from main import format_bouquet, main, make_bouquet, parse_bouquet_design


def test_parse_design():
    result = parse_bouquet_design("AL10a15b5c30")
    assert result == {
        "size": "L",
        "name": "A",
        "flowers": {"aL": 10, "bL": 15, "cL": 5},
        "extra_flowers": 0,
    }


def test_make_bouquet():
    # empty warehouse
    warehouse = defaultdict(int)
    design = {"size": "L", "flowers": {"aL": 3}, "extra_flowers": 3}
    bouquet, _warehouse = make_bouquet(design, warehouse)
    assert bouquet is False

    #

    # make sure only flowers of right size are used
    warehouse = {"aL": 3, "bL": 0, "cL": 1, "dL": 2, "aS": 1, "bS": 1, "cS": 0}
    design = {"size": "L", "flowers": {"aL": 3}, "extra_flowers": 2}
    bouquet, new_warehouse = make_bouquet(design, warehouse)
    assert bouquet["flowers"] == {"aL": 3, "cL": 1, "dL": 1}
    assert new_warehouse == {
        "aL": 0,
        "aS": 1,
        "bL": 0,
        "bS": 1,
        "cL": 0,
        "cS": 0,
        "dL": 1,
    }


def test_format_bouquet():
    design = {"name": "a", "size": "S"}
    flowers = {"aS": 10, "bS": 15, "cS": 5}
    bouquet = {"design": design, "flowers": flowers}
    assert format_bouquet(bouquet) == "aS10a15b5c"


def test_main():
    """
    As one old but wise SRE once said "It's always a good idea
    to have some end-to-end smoke test.". Here it is!

    PS it was me
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        filename = "input.txt"
        with open(filename, "wt") as f:
            f.write(
                textwrap.dedent(
                    """\
                AL1a2
                
                aL
                bL
                aS
                aL
                bL
            """
                )
            )
        result = runner.invoke(main, ["--debug", filename])

    assert result.exit_code == 0
    assert result.output == textwrap.dedent(
        """\
        I parsed the following bouquet designs:
        OrderedDict([('AL1a2', {'name': 'A', 'size': 'L', 'flowers': {'aL': 1}, 'extra_flowers': 1})])
        
        got flower: aL
        <no bouquet is possible to make>
        got flower: bL
        AL1a1b
        got flower: aS
        <no bouquet is possible to make>
        got flower: aL
        <no bouquet is possible to make>
        got flower: bL
        AL1a1b
        """
    )
