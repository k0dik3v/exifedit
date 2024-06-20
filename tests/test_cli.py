from click.testing import CliRunner
from app.cli import hello


def test_hello():
    runner = CliRunner()
    result = runner.invoke(hello, ['--name', 'World'])
    assert result.exit_code == 0
    assert 'Hello, World' in result.output
