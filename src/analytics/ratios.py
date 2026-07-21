"""
Financial Ratio Engine
Sprint 2 - Day 08
"""

from typing import Optional
import sqlite3


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """Net Profit Margin (%)"""
    if net_profit is None or sales is None or sales == 0:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit: float, sales: float) -> Optional[float]:
    """Operating Profit Margin (%)"""
    if operating_profit is None or sales is None or sales == 0:
        return None
    return (operating_profit / sales) * 100


def roe(net_profit: float, equity_capital: float, reserves: float) -> Optional[float]:
    """Return on Equity (%)"""
    if net_profit is None:
        return None

    equity = (equity_capital or 0) + (reserves or 0)

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def roce(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float,
) -> Optional[float]:
    """Return on Capital Employed (%)"""

    if ebit is None:
        return None

    capital = (
        (equity_capital or 0)
        + (reserves or 0)
        + (borrowings or 0)
    )

    if capital <= 0:
        return None

    return (ebit / capital) * 100


def roa(net_profit: float, total_assets: float) -> Optional[float]:
    """Return on Assets (%)"""

    if net_profit is None or total_assets is None or total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


def update_financial_ratios():

    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    query = """
    SELECT
        pl.company_id,
        pl.year,
        pl.sales,
        pl.operating_profit,
        pl.other_income,
        pl.net_profit,
        bs.equity_capital,
        bs.reserves,
        bs.borrowings,
        bs.total_assets

    FROM profitandloss pl

    JOIN balancesheet bs

    ON pl.company_id = bs.company_id
    AND pl.year = bs.year
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    updated = 0

    for row in rows:

        (
            company_id,
            year,
            sales,
            operating_profit,
            other_income,
            net_profit,
            equity_capital,
            reserves,
            borrowings,
            total_assets,
        ) = row


        # EBIT approximation
        ebit = (
            (operating_profit or 0)
            + (other_income or 0)
        )


        cursor.execute(
            """
            UPDATE financial_ratios

            SET

            net_profit_margin_pct = ?,
            operating_profit_margin_pct = ?,
            return_on_equity_pct = ?,
            return_on_capital_employed_pct = ?,
            return_on_assets_pct = ?

            WHERE company_id = ?
            AND year = ?

            """,

            (

                net_profit_margin(
                    net_profit,
                    sales
                ),

                operating_profit_margin(
                    operating_profit,
                    sales
                ),

                roe(
                    net_profit,
                    equity_capital,
                    reserves
                ),

                roce(
                    ebit,
                    equity_capital,
                    reserves,
                    borrowings
                ),

                roa(
                    net_profit,
                    total_assets
                ),

                company_id,
                year
            )
        )

        updated += cursor.rowcount


    conn.commit()
    conn.close()


    print(
        f"Financial ratios updated successfully. Rows updated: {updated}"
    )


if __name__ == "__main__":
    update_financial_ratios()