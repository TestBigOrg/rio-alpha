import logging
import click
import rasterio as rio
from rio_alpha.utils import _parse_ndv
from rio_alpha.islossy import count_ndv_regions
from rio_alpha.findnodata import determine_nodata

logger = logging.getLogger('rio_alpha')


@click.group('alpha')
def alpha():
    """Add alpha band to imagery based on nodata values,
        Find nodata in input image.
    """
    pass


@click.command('islossy')
@click.argument('input', nargs=1, type=click.Path(exists=True))
@click.option('--ndv', default='[0, 0, 0]',
              help='Expects an integer or a len(list) == 3 representing a nodata value')
def islossy(input, ndv):
    """
    Determine if there are >= 10 nodata regions in an image

    If true, returns the string `--lossy lossy`.
    """
    with rio.open(input, "r") as src:
        img = src.read()

    ndv = _parse_ndv(ndv, 3)

    if count_ndv_regions(img, ndv) >= 10:
        click.echo("--lossy lossy")
    else:
        click.echo("")


@click.command('findnodata')
@click.argument('src_path', type=click.Path(exists=True))
@click.option('--user_nodata', '-u', default=None,
              help="User supplies the nodata value, "
              "input a single value or a list of per-band values.")
@click.option('--debug', help="Enables matplotlib & printing of figures")
@click.option('--verbose', '-v',
              help="Prints extra information, "
              "like competing candidate values")
@click.option('--discovery', default=None,
              help="Prints extra information, "
              "like competing candidate values")
def findnodata(src_path, user_nodata, debug, verbose, discovery):
    determine_nodata(src_path, user_nodata)

# with rio.drivers():
#   with rio.open(args.infile, "r") as src:
#     count = src.count

# if ( count == 4 ):
#     print "alpha"
# else:
#     nodata = src.nodata
#     if ( nodata == None ):
#         if discovery:
#             discover_ndv()
#         else:
#             print ""
#     else:
#         print str(int(nodata)) + " " + str(int(nodata)) + " " + str(int(nodata))


alpha.add_command(islossy)
alpha.add_command(findnodata)
