import itertools
from unittest import mock

import pytest

from connect4.controllers import Connect4Controller


class TestConnect4Controller:
    @pytest.fixture
    def controller(self):
        return Connect4Controller()

    @pytest.fixture
    def m_cycle(self, monkeypatch):
        m_cycle = mock.Mock(return_value=iter(["X", "O"]))
        monkeypatch.setattr(Connect4Controller, "cycle", m_cycle)
        return m_cycle

    @pytest.fixture
    def m_get_input(self, monkeypatch):
        m_get_input = mock.Mock(return_value=2)
        monkeypatch.setattr(Connect4Controller, "get_input", m_get_input)
        return m_get_input

    def test_cycle(self, controller):
        expected = controller._player_token_types + (controller._player_token_types[0],)

        result = itertools.islice(controller.cycle(), 3)

        assert tuple(result) == expected

    def test_start(self, monkeypatch, controller, m_cycle, m_get_input):
        m_cycle.return_value = iter(["X"])
        m_insert_token = mock.Mock()
        monkeypatch.setattr(Connect4Controller, "insert_token", m_insert_token)
        m_print_board = mock.Mock()
        monkeypatch.setattr(Connect4Controller, "print_board", m_print_board)

        controller.start()

        m_get_input.assert_called_once()
        m_insert_token.assert_called_once_with(2, "X")
        m_print_board.assert_called_once()

    def test_get_input(self, monkeypatch, controller):
        monkeypatch.setattr("builtins.input", lambda _: "2")

        result = controller.get_input()

        assert result == 2 - 1

    def test_insert_token(self, monkeypatch, controller):
        controller.insert_token(2, "X")
        assert controller._board[2][0] == "X"
        controller.insert_token(2, "O")
        assert controller._board[2][1] == "O"

    def test_print_board(self, capsys, controller):
        controller._board = [["0", "1", "2", "3", "4"], ["5", "6", "7", "8", "9"]]

        controller.print_board()

        out, err = capsys.readouterr()

        assert out == ("4 9 \n" "3 8 \n" "2 7 \n" "1 6 \n" "0 5 \n" "1 2\n")
