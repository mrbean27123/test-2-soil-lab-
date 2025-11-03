class QueryParamParsingMixin:
    """
    Mixin providing helper methods for parsing and normalizing query parameter values.

    This mixin is designed for use in Specification classes that need to handle multi-value query
    parameters (e.g., for filtering or ordering).
    """

    @staticmethod
    def _extract_list_from_query_param(raw_value: str | None) -> list[str]:
        """
        Parses a comma-separated query parameter string into a list of unique, trimmed values
        preserving original order.

        Args:
            raw_value: The raw query parameter string (e.g., "1,2,3").

        Returns:
            list[str]: A list of unique, stripped strings extracted from the comma-separated query
            parameter.
        """
        if not raw_value:
            return []

        seen = set()
        result = []

        for token in raw_value.split(","):
            token = token.strip()

            if token and token not in seen:
                seen.add(token)
                result.append(token)

        return result
