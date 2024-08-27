"""Test the FEN regex with various valid and invalid FEN strings."""

import re

from main import FEN_REGEX


def test_valid_fen_starting_position() -> None:
    """Test a valid FEN string representing the starting position."""
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert re.match(FEN_REGEX, fen)


def test_valid_fen_with_en_passant() -> None:
    """Test a valid FEN string with an en passant target square."""
    fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e3 0 2"
    assert re.match(FEN_REGEX, fen)


def test_valid_fen_with_no_castling() -> None:
    """Test a valid FEN string with no castling rights."""
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b - - 1 2"
    assert re.match(FEN_REGEX, fen)


def test_invalid_fen_missing_rank() -> None:
    """Test an invalid FEN string missing one rank."""
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/ w KQkq - 0 1"
    assert not re.match(FEN_REGEX, fen)


def test_invalid_fen_with_wrong_en_passant() -> None:
    """Test an invalid FEN string with an incorrect en passant square."""
    fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq z9 0 2"
    assert not re.match(FEN_REGEX, fen)


def test_invalid_fen_missing_fullmove_number() -> None:
    """Test an invalid FEN string missing the fullmove number."""
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0"
    assert not re.match(FEN_REGEX, fen)


def test_valid_fen_without_castling_rights() -> None:
    """Test a valid FEN string with no castling rights available."""
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
    assert re.match(FEN_REGEX, fen)


def test_invalid_fen_extra_rank() -> None:
    """Test an invalid FEN string with an extra rank."""
    fen = "rnbqkbnr/pppppppp/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert not re.match(FEN_REGEX, fen)


def test_valid_fen_with_minimal_input() -> None:
    """Test a valid FEN string with minimal pieces and no castling."""
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    assert re.match(FEN_REGEX, fen)
