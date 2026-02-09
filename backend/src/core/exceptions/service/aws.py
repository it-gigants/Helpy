from src.core.exceptions.service.base import AppError


class AwsError(AppError):
    message = "AWS error"


class InvalidFileTypeError(AwsError):
    message = "Invalid file type"


class InvalidUrlError(AwsError):
    message = "Invalid url"


class UploadFileError(AwsError):
    message = "Error while uploading file"


class DeleteFileError(AwsError):
    message = "Error while deleting file"
