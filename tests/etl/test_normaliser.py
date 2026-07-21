import pytest

from src.etl.normaliser import normalize_year, normalize_ticker


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (2024, 2024),
        ("2024", 2024),
        ("FY24", 2024),
        ("FY 2024", 2024),
        ("Mar-24", 2024),
        ("Mar 2024", 2024),
        ("2023", 2023),
        ("FY23", 2023),
        ("Mar-23", 2023),
        ("FY 2022", 2022),
        ("Mar-2021", 2021),
        ("2020", 2020),
        ("FY20", 2020),
        ("FY19", 2019),
        ("Mar-18", 2018),
        (None, None),
        ("", None),
        ("ABC", None),
        ("Unknown", None),
        ("--", None),
    ],
)
def test_normalize_year(input_value, expected):
    assert normalize_year(input_value) == expected


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("TCS", "TCS"),
        ("tcs", "TCS"),
        (" TCS ", "TCS"),
        ("INFY.NS", "INFY"),
        ("infy.ns", "INFY"),
        ("HDFCBANK", "HDFCBANK"),
        (" hdfcbank ", "HDFCBANK"),
        ("SBIN.NS", "SBIN"),
        ("RELIANCE", "RELIANCE"),
        (" reliance ", "RELIANCE"),
        ("LTIM", "LTIM"),
        ("BAJAJ FINANCE", "BAJAJFINANCE"),
        ("HCL TECH", "HCLTECH"),
        ("", None),
        (None, None),
    ],
)
def test_normalize_ticker(input_value, expected):
    assert normalize_ticker(input_value) == expected