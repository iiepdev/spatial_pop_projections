from invoke import task


@task
def jupyter(ctx):
    ctx.run("jupyter lab --allow-root --no-browser --ip=0.0.0.0", pty=True)


@task
def format(ctx):
    ctx.run("black --extend-exclude scripts/tests/ .", pty=True)


@task
def test(ctx):
    ctx.run("pytest scripts/", pty=True)
