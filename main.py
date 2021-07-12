import click

from sentinel.commands import m2m, proxy, connect, configure
from sentinel.context import Context


@click.group()
@click.option("--verbose", help="verbose output", is_flag=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.color = True

    Context.verbose = verbose


cli.add_command(configure.configure)
cli.add_command(connect.connect)
cli.add_command(proxy.proxy)
cli.add_command(m2m.m2m)

cli()
