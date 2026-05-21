"""
Sentilytics — Test: Text Preprocessing
Unit tests for the text preprocessing pipeline.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing.text_preprocessing import (
    combine_text, case_folding, clean_text, tokenize,
    remove_stopwords, preprocess_single
)


class TestCombineText:
    """Tests for text combination."""

    def test_combine_title_and_summary(self):
        result = combine_text("Judul Berita", "Ini adalah ringkasan berita")
        assert result == "Judul Berita Ini adalah ringkasan berita"

    def test_combine_title_only(self):
        result = combine_text("Judul Berita", "")
        assert result == "Judul Berita"

    def test_combine_summary_only(self):
        result = combine_text("", "Ini ringkasan")
        assert result == "Ini ringkasan"

    def test_combine_empty(self):
        result = combine_text("", "")
        assert result == ""

    def test_combine_none_handling(self):
        result = combine_text(None, "test")
        assert result == "test"


class TestCaseFolding:
    """Tests for case folding."""

    def test_uppercase_to_lower(self):
        assert case_folding("BBCA NAIK") == "bbca naik"

    def test_mixed_case(self):
        assert case_folding("Saham BRI Turun") == "saham bri turun"

    def test_already_lowercase(self):
        assert case_folding("sudah lowercase") == "sudah lowercase"

    def test_empty_string(self):
        assert case_folding("") == ""

    def test_non_string(self):
        assert case_folding(None) == ""


class TestCleanText:
    """Tests for text cleaning."""

    def test_remove_url(self):
        text = "berita dari https://cnbc.com tentang BBCA"
        result = clean_text(text)
        assert "https" not in result
        assert "cnbc" not in result or "berita" in result

    def test_remove_special_characters(self):
        text = "saham BBCA naik 10%! #trading @market"
        result = clean_text(text)
        assert "%" not in result
        assert "#" not in result
        assert "@" not in result

    def test_remove_numbers(self):
        text = "saham naik 123 persen"
        result = clean_text(text)
        assert "123" not in result

    def test_keep_letters(self):
        text = "saham perbankan indonesia"
        result = clean_text(text)
        assert "saham" in result
        assert "perbankan" in result

    def test_empty_string(self):
        assert clean_text("") == ""


class TestTokenize:
    """Tests for tokenization."""

    def test_basic_tokenize(self):
        tokens = tokenize("saham bbca naik hari ini")
        assert len(tokens) == 5
        assert "saham" in tokens

    def test_filter_short_tokens(self):
        tokens = tokenize("a di dan b itu saham")
        # Single-character tokens should be filtered
        assert "a" not in tokens
        assert "b" not in tokens

    def test_empty_string(self):
        tokens = tokenize("")
        assert tokens == []


class TestPreprocessSingle:
    """Tests for the full preprocessing pipeline."""

    def test_full_pipeline(self):
        text = "Saham BBCA naik 5% di Bursa https://example.com"
        result = preprocess_single(text)

        assert 'clean_text' in result
        assert 'tokens' in result
        assert 'stemmed_text' in result
        assert "https" not in result['clean_text']

    def test_empty_input(self):
        result = preprocess_single("")
        assert result['clean_text'] == ""
        assert result['tokens'] == ""
        assert result['stemmed_text'] == ""
