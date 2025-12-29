"""
Service for fetching ETF constituents
"""

from typing import List, Dict
import csv
import os


class ConstituentsService:
    """Service for managing ETF holdings/constituents"""

    def __init__(self):
        # Ticker to company name mapping
        self.ticker_names = {
            # Technology
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "NVDA": "NVIDIA Corporation",
            "AVGO": "Broadcom Inc.",
            "GOOGL": "Alphabet Inc.",
            "GOOG": "Alphabet Inc.",
            "META": "Meta Platforms Inc.",
            "TSLA": "Tesla Inc.",
            "AMD": "Advanced Micro Devices",
            "ARM": "ARM Holdings",
            "ADBE": "Adobe Inc.",
            "CSCO": "Cisco Systems",
            "NFLX": "Netflix Inc.",
            "AMZN": "Amazon.com Inc.",
            "QCOM": "Qualcomm Inc.",
            "TXN": "Texas Instruments",
            "INTC": "Intel Corporation",
            "ORCL": "Oracle Corporation",
            "CRM": "Salesforce Inc.",
            "IBM": "IBM",
            "ACN": "Accenture",
            "INTU": "Intuit Inc.",
            "MU": "Micron Technology",
            "AMAT": "Applied Materials",
            "LRCX": "Lam Research",
            "MRVL": "Marvell Technology",
            "ADI": "Analog Devices",
            "SNPS": "Synopsys Inc.",
            "CDNS": "Cadence Design",
            "KLAC": "KLA Corporation",
            "NXPI": "NXP Semiconductors",
            "ARM": "ARM Holdings",

            # Software & Cloud
            "SHOP": "Shopify Inc.",
            "SNOW": "Snowflake Inc.",
            "DOCU": "DocuSign Inc.",
            "OKTA": "Okta Inc.",
            "DDOG": "Datadog Inc.",
            "ZM": "Zoom Video Communications",
            "TWLO": "Twilio Inc.",
            "CRWD": "CrowdStrike Holdings",
            "PLTR": "Palantir Technologies",
            "COIN": "Coinbase Global",
            "SQ": "Block Inc.",
            "U": "Unity Software",
            "ROKU": "Roku Inc.",
            "Z": "Zillow Group",
            "RBLX": "Roblox Corporation",
            "AFRM": "Affirm Holdings",
            "UPST": "Upstart Holdings",
            "HOOD": "Robinhood Markets",
            "ETSY": "Etsy Inc.",
            "WDAY": "Workday Inc.",
            "SPLK": "Splunk Inc.",
            "PANW": "Palo Alto Networks",
            "ZS": "Zscaler Inc.",
            "FTNT": "Fortinet Inc.",
            "GEN": "Gen Digital",
            "CTXS": "Citrix Systems",

            # Semiconductors
            "ASML": "ASML Holding",
            "TSM": "Taiwan Semiconductor",
            "SOXX": "iShares Semiconductor ETF",

            # Consumer & Retail
            "COST": "Costco Wholesale",
            "SBUX": "Starbucks Corporation",
            "MCD": "McDonald's Corporation",
            "NKE": "Nike Inc.",
            "HD": "Home Depot Inc.",
            "LOW": "Lowe's Companies",
            "TGT": "Target Corporation",
            "WMT": "Walmart Inc.",
            "AMZN": "Amazon.com Inc.",
            "BKNG": "Booking Holdings",
            "MAR": "Marriott International",
            "ABNB": "Airbnb Inc.",
            "LULU": "Lululemon Athletica",
            "KHC": "Kraft Heinz Co.",
            "KDP": "Keurig Dr Pepper",
            "MNST": "Monster Beverage",
            "PEP": "PepsiCo Inc.",
            "KO": "Coca-Cola Company",
            "PG": "Procter & Gamble",
            "CL": "Colgate-Palmolive",
            "EL": "Estee Lauder Companies",
            "DIS": "Walt Disney Company",
            "CMCSA": "Comcast Corporation",
            "FOXA": "Fox Corporation",
            "WBD": "Warner Bros. Discovery",

            # Healthcare
            "JNJ": "Johnson & Johnson",
            "UNH": "UnitedHealth Group",
            "PFE": "Pfizer Inc.",
            "ABBV": "AbbVie Inc.",
            "MRK": "Merck & Co.",
            "TMO": "Thermo Fisher Scientific",
            "ABT": "Abbott Laboratories",
            "DHR": "Danaher Corporation",
            "BMY": "Bristol-Myers Squibb",
            "AMGN": "Amgen Inc.",
            "GILD": "Gilead Sciences",
            "REGN": "Regeneron Pharmaceuticals",
            "VRTX": "Vertex Pharmaceuticals",
            "ILMN": "Illumina Inc.",
            "IDXX": "IDEXX Laboratories",
            "DXCM": "DexCom Inc.",
            "ISRG": "Intuitive Surgical",
            "BDX": "Becton Dickinson",
            "BIIB": "Biogen Inc.",
            "MRNA": "Moderna Inc.",
            "SGEN": "Seagen Inc.",
            "LLY": "Eli Lilly and Company",
            "AZN": "AstraZeneca",
            "CVS": "CVS Health",

            # Financial Services
            "BRK.B": "Berkshire Hathaway",
            "JPM": "JPMorgan Chase & Co.",
            "BAC": "Bank of America",
            "WFC": "Wells Fargo",
            "C": "Citigroup Inc.",
            "GS": "Goldman Sachs",
            "MS": "Morgan Stanley",
            "SCHW": "Charles Schwab",
            "BLK": "BlackRock Inc.",
            "SPGI": "S&P Global",
            "ICE": "Intercontinental Exchange",
            "AXP": "American Express",
            "MA": "Mastercard Incorporated",
            "V": "Visa Inc.",
            "PYPL": "PayPal Holdings",
            "ADP": "Automatic Data Processing",
            "FISV": "Fiserv Inc.",
            "GPN": "Global Payments",
            "SQ": "Block Inc.",
            "COIN": "Coinbase Global",
            "IBKR": "Interactive Brokers",
            "ETFC": "E*TRADE Financial",
            "MET": "MetLife Inc.",
            "PRU": "Prudential Financial",
            "AIG": "American International",
            "AON": "Aon plc",
            "MMC": "Marsh & McLennan",
            "TRV": "The Travelers Companies",

            # Energy & Utilities
            "XOM": "Exxon Mobil",
            "CVX": "Chevron Corporation",
            "COP": "ConocoPhillips",
            "SLB": "Schlumberger NV",
            "EOG": "EOG Resources",
            "PXD": "Pioneer Natural Resources",
            "NEE": "NextEra Energy",
            "DUK": "Duke Energy",
            "SO": "Southern Company",
            "EXC": "Exelon Corporation",
            "D": "Dominion Energy",
            "XEL": "Xcel Energy",
            "ETR": "Entergy Corporation",

            # Industrials
            "BA": "Boeing Company",
            "CAT": "Caterpillar Inc.",
            "HON": "Honeywell International",
            "GE": "General Electric",
            "UNP": "Union Pacific",
            "UPS": "United Parcel Service",
            "FDX": "FedEx Corporation",
            "RTX": "Raytheon Technologies",
            "LMT": "Lockheed Martin",
            "NOC": "Northrop Grumman",
            "GD": "General Dynamics",
            "DE": "Deere & Company",
            "CM": "Cummins Inc.",
            "EMR": "Emerson Electric",
            "ITW": "Illinois Tool Works",
            "MMM": "3M Company",
            "OTIS": "Otis Worldwide",
            "CARR": "Carrier Global",
            "TM": "Toyota Motor",
            "GM": "General Motors",
            "F": "Ford Motor",

            # Materials
            "APD": "Air Products and Chemicals",
            "SHW": "Sherwin-Williams",
            "LIN": "Linde plc",
            "FCX": "Freeport-McMoRan",
            "NEM": "Newmont Corporation",
            "DOW": "Dow Inc.",
            "DD": "DuPont de Nemours",

            # Real Estate
            "AMT": "American Tower",
            "PLD": "Prologis Inc.",
            "CCI": "Crown Castle",
            "EQIX": "Equinix Inc.",
            "SPG": "Simon Property Group",
            "O": "Realty Income",
            "WELL": "Welltower Inc.",
            "AVB": "AvalonBay Communities",
            "EQR": "Equity Residential",

            # Communication & Telecom
            "GOOGL": "Alphabet Inc.",
            "META": "Meta Platforms Inc.",
            "T": "AT&T Inc.",
            "VZ": "Verizon Communications",
            "TMUS": "T-Mobile US",
            "CMCSA": "Comcast Corporation",
            "CHTR": "Charter Communications",
            "DIS": "Walt Disney Company",
            "NFLX": "Netflix Inc.",
            "EA": "Electronic Arts",
            "ATVI": "Activision Blizzard",

            # ETFs & Indices
            "SPY": "SPDR S&P 500 ETF",
            "QQQ": "Invesco QQQ Trust",
            "IWM": "iShares Russell 2000 ETF",
            "DIA": "SPDR Dow Jones Industrial Average ETF",
            "GLD": "SPDR Gold Shares",
            "USO": "United States Oil Fund",
            "SLV": "iShares Silver Trust",
            "TLT": "iShares 20+ Year Treasury Bond",
            "VXX": "iPath Series B S&P 500 VIX",
            "SVXY": "ProShares Short VIX Short-Term",
            "XLF": "Financial Select Sector SPDR",
            "XLE": "Energy Select Sector SPDR",
            "XLK": "Technology Select Sector SPDR",
            "XLV": "Health Care Select Sector SPDR",
            "XLY": "Consumer Discretionary Select Sector SPDR",
            "XLP": "Consumer Staples Select Sector SPDR",

            # Volatility & Indicators
            "VIX": "CBOE Volatility Index",
            "^VIX": "CBOE Volatility Index",
            "VXN": "Nasdaq-100 Volatility Index",
            "^VXN": "Nasdaq-100 Volatility Index",
            "RVX": "Russell 2000 Volatility Index",
            "PCR": "CBOE Total Put/Call Ratio",

            # Small Caps
            "SMCI": "Super Micro Computer",
            "SMG": "Scotts Miracle-Gro",
            "FRG": "Ferguson",
            "IART": "Integra LifeSciences",
            "PCT": "PCTEL",
            "INMD": "InMode Ltd.",
            "AYTU": "AyTu Bio Holdings",
            "EYPT": "EyePoint Pharmaceuticals",
            "KALA": "KALA Pharmaceuticals",
            "RGLS": "Regulus Therapeutics",
            "SLNO": "Silence Therapeutics",
            "TARS": "Tarsius Pharmaceuticals",
            "VYNE": "Vyne Therapeutics",
            "WVE": "Wave Life Sciences",
            "XAIR": "XAIR",
            "ZLAB": "Zai Lab",

            # Other Notable
            "MELI": "MercadoLibre Inc.",
            "NTES": "NetEase Inc.",
            "JD": "JD.com Inc.",
            "PDD": "PDD Holdings",
            "BABA": "Alibaba Group",
            "TCOM": "Trip.com Group",
            "PAYX": "Paychex Inc.",
            "PCAR": "PACCAR Inc.",
            "ODFL": "Old Dominion Freight",
            "ORLY": "O'Reilly Automotive",
            "ROST": "Ross Stores",
            "WBA": "Walgreens Boots Alliance",
            "CTSH": "Cognizant Technology",
            "FISV": "Fiserv Inc.",
            "IDXX": "IDEXX Laboratories",
            "REGN": "Regeneron Pharmaceuticals",
            "SIRI": "Sirius XM Holdings",
            "VRSK": "Verisk Analytics",
            "CSX": "CSX Corporation",
            "GEHC": "GE HealthCare",
            "HON": "Honeywell International",
            "SWKS": "Skyworks Solutions",
        }

        # Popular Nasdaq-100 stocks (top holdings)
        self.qqq_holdings = [
            "AAPL", "MSFT", "NVDA", "AVGO", "GOOGL", "META", "TSLA", "AMD", "ARM",
            "ADBE", "CSCO", "NFLX", "AMZN", "QCOM", "TXN", "INTC", "GOOG", "COST",
            "AMGN", "SBUX", "INTU", "MU", "ISRG", "GILD", "BKNG",
            "ADI", "MRVL", "LRCX", "CHTR", "AMAT", "TMUS", "SNPS", "CDNS",
            "MAR", "AZN", "ABNB", "CMCSA", "CSX",
            "CTSH", "DDOG", "DXCM", "EA", "EXC",
            "IDXX", "ILMN", "JD", "KDP", "KHC", "KLAC", "LULU", "MELI", "MNST",
            "MRNA", "NTES", "NXPI", "ODFL", "ORLY", "PANW", "PAYX",
            "PCAR", "PEP", "PDD", "PYPL", "REGN", "ROST", "SIRI", "SPLK",
            "SWKS", "TCOM", "VRSK", "VRTX", "WBD", "WDAY",
            "XEL", "ZM", "ZS"
        ]

        # Popular S&P 500 stocks (top holdings by market cap)
        self.spy_holdings = [
            "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "GOOG", "BRK.B", "LLY",
            "AVGO", "JPM", "XOM", "MA", "V", "JNJ", "UNH", "HD", "PG", "COST", "ABBV",
            "MRK", "CVX", "KO", "BAC", "PEP", "TMO", "WMT", "CSCO", "CRM", "ABT",
            "MCD", "ADBE", "NFLX", "AMD", "CMCSA", "INTU", "VZ", "DIS", "DHR", "QCOM",
            "NEE", "PFE", "HON", "WFC", "ABNB", "TXN", "ACN", "IBM", "AMGN", "PM",
            "BA", "CAT", "DE", "GE", "GM", "INTC", "LOW", "LMT", "MDLZ",
            "MET", "MS", "NKE", "ORCL", "PYPL", "SCHW", "SHOP", "SLB", "SPG", "T",
            "TGT", "UPS", "USB", "UNP", "WBA"
        ]

        # Russell 2000 holdings (sample of notable small caps)
        self.iwm_holdings = [
            "PLTR", "COIN", "SQ", "SHOP", "U", "DOCU", "SNOW", "CRWD", "ZM", "RBLX",
            "AFRM", "UPST", "HOOD", "ETSY", "ROKU", "Z", "TWLO", "OKTA", "DDOG",
            "SG", "SMCI", "FRG", "IART", "PCT", "INMD", "AYTU",
            "EYPT", "KALA", "RGLS", "SLNO", "TARS", "VYNE", "WVE", "XAIR", "ZLAB"
        ]

        self.cache = {
            "QQQ": self.qqq_holdings,
            "SPY": self.spy_holdings,
            "IWM": self.iwm_holdings,
        }

        # Load additional company names from SPY components CSV
        self._load_company_names_from_csv()

    def _load_company_names_from_csv(self):
        """Load company names from SPY-components.csv file"""
        csv_path = os.path.join(os.path.dirname(__file__), '../../../data/SPY-components.csv')

        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8-sig') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and len(row) >= 2:
                            ticker = row[0].strip()
                            company_name = row[1].strip()
                            # Only add if not already in ticker_names (prefer hardcoded names)
                            if ticker and ticker not in self.ticker_names:
                                self.ticker_names[ticker] = company_name
            except Exception as e:
                print(f"Warning: Could not load company names from CSV: {e}")

    async def get_etf_holdings(self, etf_ticker: str) -> List[str]:
        """
        Get holdings for an ETF

        Args:
            etf_ticker: ETF symbol (e.g., "QQQ", "SPY", "IWM")

        Returns:
            List of constituent ticker symbols
        """
        return self.cache.get(etf_ticker.upper(), [])

    async def get_all_index_constituents(self) -> Dict[str, List[str]]:
        """
        Get constituents for all major indices

        Returns:
            Dictionary mapping ETF tickers to their holdings
        """
        return self.cache

    async def search_tickers(self, query: str) -> List[dict]:
        """
        Search for tickers matching a query

        Args:
            query: Search string (e.g., "AAP", "Tech")

        Returns:
            List of matching tickers with company names
        """
        query = query.upper()

        all_tickers = set()

        # Get tickers from database (if available)
        try:
            from app.database.models import SessionLocal, Ticker
            db = SessionLocal()
            try:
                # Get all tickers from database
                db_tickers = db.query(Ticker.symbol).all()
                # Extract symbols from result tuples
                for ticker_row in db_tickers:
                    if isinstance(ticker_row, tuple):
                        all_tickers.add(ticker_row[0])
                    else:
                        all_tickers.add(ticker_row)
                print(f"DEBUG: Loaded {len(all_tickers)} tickers from database")
            finally:
                db.close()
        except Exception as e:
            print(f"Warning: Could not load tickers from database: {e}")
            import traceback
            traceback.print_exc()

        # If database is empty or query returned no results, use hardcoded ticker names
        if not all_tickers:
            all_tickers.update(self.ticker_names.keys())

        # Filter by query - check both ticker and company name
        matches = []
        for ticker in sorted(all_tickers):
            company_name = self.ticker_names.get(ticker, ticker)
            if query in ticker or query.upper() in company_name.upper():
                matches.append({
                    "ticker": ticker,
                    "name": company_name
                })

        return matches[:20]  # Limit to 20 results


constituents_service = ConstituentsService()
