"""
Service for querying historical patterns
"""

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
from app.services.data_service import data_service
from app.models.schemas import QueryRequest, PatternInstance, QueryResponse


class QueryService:
    """Service for querying historical patterns and calculating forward returns"""

    async def execute_query(self, query: QueryRequest) -> QueryResponse:
        """
        Execute a historical pattern query

        Args:
            query: QueryRequest with ticker, condition, and parameters

        Returns:
            QueryResponse with instances and statistics
        """
        # Fetch historical data
        data = await data_service.fetch_historical_data(query.ticker)

        # Find dates matching the condition
        matching_dates = self._find_matching_dates(data, query)

        # Calculate forward returns for each matching date
        horizons_map = {"1d": 1, "1w": 5, "1m": 21, "1y": 252}
        filtered_horizons = {
            k: v for k, v in horizons_map.items() if k in query.time_horizons
        }

        instances = []
        for match_date in matching_dates:
            forward_returns = data_service.get_forward_returns(
                data, match_date, filtered_horizons
            )
            instances.append(
                PatternInstance(date=match_date, forward_returns=forward_returns)
            )

        # Calculate summary statistics
        summary_stats = self._calculate_summary_statistics(
            instances, query.time_horizons
        )

        # Check if this is an indicator
        reference_ticker = None
        if data_service.is_indicator(query.ticker):
            reference_ticker = data_service.get_reference_ticker(query.ticker)

        return QueryResponse(
            ticker=query.ticker,
            condition=self._format_condition(query),
            reference_ticker=reference_ticker,
            instances=instances,
            summary_statistics=summary_stats,
            total_occurrences=len(instances),
        )

    def _find_matching_dates(
        self, data: pd.DataFrame, query: QueryRequest
    ) -> List[datetime]:
        """Find all dates where the condition is met"""
        # Calculate percentage changes
        pct_changes = data_service.calculate_percentage_change(data)

        # Apply the condition
        if query.condition_type == "percentage_change":
            if query.operator == "gt":
                mask = pct_changes > query.threshold
            elif query.operator == "lt":
                mask = pct_changes < query.threshold
            elif query.operator == "gte":
                mask = pct_changes >= query.threshold
            elif query.operator == "lte":
                mask = pct_changes <= query.threshold
            elif query.operator == "eq":
                mask = pct_changes == query.threshold
            else:
                raise ValueError(f"Unknown operator: {query.operator}")
        elif query.condition_type == "absolute_threshold":
            # Use the absolute close value
            if query.operator == "gt":
                mask = data["Close"] > query.threshold
            elif query.operator == "lt":
                mask = data["Close"] < query.threshold
            elif query.operator == "gte":
                mask = data["Close"] >= query.threshold
            elif query.operator == "lte":
                mask = data["Close"] <= query.threshold
            elif query.operator == "eq":
                mask = data["Close"] == query.threshold
            else:
                raise ValueError(f"Unknown operator: {query.operator}")
        else:
            raise ValueError(f"Unknown condition type: {query.condition_type}")

        # Return matching dates (exclude first row which has NaN)
        matching_dates = data[mask].index.tolist()
        return [d for d in matching_dates if pd.notna(d)]

    def _calculate_summary_statistics(
        self, instances: List[PatternInstance], horizons: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate summary statistics for each time horizon"""
        stats = {}

        for horizon in horizons:
            returns = [
                instance.forward_returns.get(horizon)
                for instance in instances
                if instance.forward_returns.get(horizon) is not None
            ]

            if returns:
                returns_series = pd.Series(returns)
                stats[horizon] = {
                    "mean": float(returns_series.mean()),
                    "median": float(returns_series.median()),
                    "std": float(returns_series.std()),
                    "min": float(returns_series.min()),
                    "max": float(returns_series.max()),
                    "win_rate": float((returns_series > 0).sum() / len(returns_series)),
                    "count": len(returns),
                }
            else:
                stats[horizon] = {
                    "mean": 0.0,
                    "median": 0.0,
                    "std": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "win_rate": 0.0,
                    "count": 0,
                }

        return stats

    def _format_condition(self, query: QueryRequest) -> str:
        """Format condition for display"""
        op_symbols = {
            "gt": ">",
            "lt": "<",
            "gte": ">=",
            "lte": "<=",
            "eq": "=",
        }
        op = op_symbols.get(query.operator, query.operator)

        if query.condition_type == "percentage_change":
            return f"{query.ticker} changed {op} {query.threshold}%"
        else:
            return f"{query.ticker} {op} {query.threshold}"


query_service = QueryService()
