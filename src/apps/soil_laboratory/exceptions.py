from core.exceptions import ClientError


class SampleReportGenerationError(ClientError):
    status_code = 404
    default_message = "Failed to generate samples report"
