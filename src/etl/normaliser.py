import re


def normalize_year(year):
    """
    Convert different year formats into a 4-digit integer.
    """

    if year is None:
        return None

    year = str(year).strip().upper()

    if year == "":
        return None

    # FY24, FY23
    match = re.fullmatch(r"FY\s*(\d{2})", year)
    if match:
        return 2000 + int(match.group(1))

    # FY2024
    match = re.fullmatch(r"FY\s*(\d{4})", year)
    if match:
        return int(match.group(1))

    # 2024
    match = re.search(r"(19|20)\d{2}", year)
    if match:
        return int(match.group())

    # Mar-24, Mar 24
    match = re.search(r"(\d{2})", year)
    if match:
        return 2000 + int(match.group(1))

    return None


def normalize_ticker(ticker):
    """
    Standardize stock ticker symbols.
    """

    if ticker is None:
        return None

    ticker = str(ticker).strip()

    if ticker == "":
        return None

    ticker = ticker.upper()
    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(" ", "")

    return ticker