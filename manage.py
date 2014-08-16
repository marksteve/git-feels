import click
from app.app import create_app


@click.group()
@click.pass_context
def cli(ctx):
  ctx.obj = create_app(
    DEBUG=True,
  )


@cli.command()
@click.pass_obj
def runserver(app):
  app.run(host="0.0.0.0")


if __name__ == '__main__':
  cli()
