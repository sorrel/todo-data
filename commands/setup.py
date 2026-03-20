"""
Setup and authentication commands.
"""

import click

from core.auth import device_code_flow, clear_tokens, load_tokens
from core.client import TadoClient


class ColouredGroup(click.Group):
    """Click group with coloured command listing."""

    def format_commands(self, ctx, formatter):
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None or cmd.hidden:
                continue
            help_text = cmd.get_short_help_str(limit=150)
            commands.append((subcommand, help_text))

        if commands:
            with formatter.section("Commands"):
                for name, help_text in commands:
                    name_str = click.style(name, fg="cyan")
                    formatter.write_text(f"  {name_str:30s} {help_text}")


@click.command("auth")
def auth_command():
    """Authenticate with Tado (OAuth2 device code flow)."""
    tokens = device_code_flow()
    if tokens:
        click.echo()
        click.echo("Token saved. You can now use other commands.")


@click.command("logout")
def logout_command():
    """Remove saved authentication tokens."""
    clear_tokens()
    click.echo("Tokens cleared.")


@click.command("status")
def status_command():
    """Show connection status and home info."""
    tokens = load_tokens()
    if not tokens:
        click.echo(click.style("Not authenticated.", fg="red"))
        click.echo("Run 'tado auth' to authenticate.")
        return

    client = TadoClient()
    if not client.connect():
        return

    home = client.get_home()
    if not home:
        return

    click.echo(click.style("Connected to Tado", fg="green"))
    click.echo(f"  Home:     {home.get('name', 'Unknown')}")
    click.echo(f"  Home ID:  {client.home_id}")

    address = home.get("contactDetails", {}).get("name", "")
    if address:
        click.echo(f"  Contact:  {address}")

    # Show zone count
    zones = client.get_zones()
    if zones:
        click.echo(f"  Zones:    {len(zones)}")

    # Show device count
    devices = client.get_devices()
    if devices:
        click.echo(f"  Devices:  {len(devices)}")
