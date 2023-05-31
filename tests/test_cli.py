from unittest import mock

from click.testing import CliRunner

from connect4.__main__ import main
from connect4.controllers import Connect4Controller


class TestCli:
    def test_main_command_starts_controller(self, monkeypatch):
        # invoke main command
        monkeypatch.setattr(Connect4Controller, "start", mock.Mock(side_effect=KeyboardInterrupt))
        result = CliRunner().invoke(main)
        assert result.exit_code == 0
        assert "Game stopped by user. Thanks for playing!" in result.output
