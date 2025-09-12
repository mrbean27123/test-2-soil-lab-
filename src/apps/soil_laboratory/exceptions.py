from core.exceptions import ClientError


class MeasurementsReportGenerationError(ClientError):
    status_code = 404
    default_message = "Failed to generate measurements report"
