from datetime import datetime

class Formatter:
    """
    A class to format strings
    """

    @staticmethod
    def fmt_date(str):
        """
        Format a iso date into d-m-Y
        """
        return datetime.fromisoformat(str).strftime("%d/%m/%Y")