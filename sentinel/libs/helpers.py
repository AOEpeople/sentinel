import random
import socket
from contextlib import closing
import click

from sentinel.context import Context


def format_header(header):
    return f"===================={header.upper()}===================="


def format_color(text, color):
    return click.style(text, fg=color)


def print_error(text):
    click.echo(format_error(text))


def format_error(text):
    return format_color(text, "red")


def print_warning(text):
    if Context.verbose:
        click.echo(format_warning(text))


def format_warning(text):
    return format_color(text, "yellow")


def print_info(text):
    if Context.verbose:
        click.echo(format_info(text))


def format_info(text):
    return format_color(text, "blue")


def print_success(text):
    if Context.verbose:
        click.echo(format_success(text))


def format_success(text):
    return format_color(text, "green")


def print_debug(text):
    if Context.verbose:
        click.echo(format_debug("############START DEBUG############"))
        click.echo(format_debug(str(text)))
        click.echo(format_debug("############END DEBUG############"))


def format_debug(text):
    return format_color(text, "cyan")


def print_normal(text):
    if Context.verbose:
        click.echo(text)


def find_free_port(start, end):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as open_socket:
        port_range = list(range(start, end))
        random.shuffle(port_range)
        for port in port_range:
            try:
                open_socket.bind(('', port))
                open_socket.close()
                return port
            except OSError:
                continue
    raise IOError('no free ports')
