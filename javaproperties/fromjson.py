"""
:program:`json2properties`
--------------------------

.. code-block:: shell

    python -m javaproperties.fromjson [-s|--separator <sep>] [infile [outfile]]
    # or, if the javaproperties package was properly installed:
    json2properties [-s|--separator <sep>] [infile [outfile]]

Convert a JSON file :option:`infile` to a Latin-1 ``.properties`` file and
write the results to :option:`outfile`.  If not specified, :option:`infile` and
:option:`outfile` default to `sys.stdin` and `sys.stdout`, respectively.

The JSON document must be an object with scalar (i.e., string, numeric,
boolean, and/or null) values; anything else will result in an error.

Output is sorted by key, and numeric, boolean, & null values are output using
their JSON representations; e.g., the input:

.. code-block:: json

    {
        "yes": true,
        "no": "false",
        "nothing": null
    }

becomes:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    no=false
    nothing=null
    yes=true

The key-value separator used in the output defaults to ``=`` and can be
overridden with the :option:`-s` or :option:`--separator` option; e.g.,
supplying ``--separator ': '`` on the command line with the above JSON file as
input produces:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    no: false
    nothing: null
    yes: true

.. versionchanged:: 0.2.0
    Added the :option:`--separator` option
"""

from   decimal  import Decimal
import json
import click
from   .        import __version__
from   .util    import strify_dict
from   .writing import dump

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, '-V', '--version',
                      message='%(prog)s %(version)s')
@click.option('-s', '--separator', default='=',
              help='Key-value separator in output; default: "="')
@click.argument('infile', type=click.File('r'), default='-')
@click.argument('outfile', type=click.File('w', encoding='iso-8859-1'),
                default='-')
@click.pass_context
def fromjson(ctx, infile, outfile, separator):
    """Convert a JSON object to a Java .properties file"""
    with infile:
        props = json.load(infile, parse_float=Decimal)
    if not isinstance(props, dict):
        ctx.fail('Only dicts can be converted to .properties')
    with outfile:
        dump(sorted(strify_dict(props).items()), outfile, separator=separator)

if __name__ == '__main__':
    fromjson()
