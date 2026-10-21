"""Application exceptions with useful traceback context for MLOps logs."""

from __future__ import annotations

import sys
import traceback
from types import TracebackType
from typing import Any


class CustomException(Exception):
    """Wrap an exception with its source location and retain the original cause.

    Backward-compatible with calls of the form ``CustomException(exc, sys)``.
    Prefer raising it with exception chaining::

        except Exception as exc:
            raise CustomException(exc, sys) from exc
    """

    def __init__(
        self,
        error_message: object,
        error_detail: Any = None,
    ) -> None:
        
        self.original_exception = error_message
        self.message = str(error_message)

        exc_type, exc_value, exc_tb = self._get_exception_info(error_detail)
        self.error_type = (
            exc_type.__name__ if exc_type is not None else type(error_message).__name__
        )
        
        self.traceback = exc_tb
        self.frames = traceback.extract_tb(exc_tb) if exc_tb is not None else []
        self.filename = self.frames[-1].filename if self.frames else None
        self.lineno = self.frames[-1].lineno if self.frames else None
        self.function = self.frames[-1].name if self.frames else None

        super().__init__(self.__str__())

    @staticmethod
    def _get_exception_info(
        error_detail: Any,
    ) -> tuple[type[BaseException] | None, BaseException | None, TracebackType | None]:
        """Accept the historical ``sys`` argument or an explicit exc_info tuple."""
        if isinstance(error_detail, tuple) and len(error_detail) == 3:
            return error_detail

        if error_detail is not None and callable(
            getattr(error_detail, "exc_info", None)
        ):
            info = error_detail.exc_info()
            if isinstance(info, tuple) and len(info) == 3:
                return info

        return sys.exc_info()

    def __str__(self) -> str:
        if self.filename is None:
            location = "location unavailable"
        else:
            location = (
                f"{self.filename}:{self.lineno} in {self.function}"
            )
        return f"{self.error_type} at {location}: {self.message}"

    def to_dict(self) -> dict[str, str | int | None]:
        """Return structured, log-friendly error fields."""
        return {
            "error_type": self.error_type,
            "message": self.message,
            "filename": self.filename,
            "lineno": self.lineno,
            "function": self.function,
        }
