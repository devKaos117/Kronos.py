import json, logging, os, sys, traceback
from datetime import datetime
from typing import Dict, Any, Optional, Union

from .utils.http import format_http_response
from .utils.tracing import get_call_info, get_process_info


class Logger:
    """
    A comprehensive custom logger for Python applications that supports
    multiple output formats, destinations and special handling for HTTP requests.
    """
    
    # Log level constants
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    
    # Map level numbers to names
    LEVEL_NAMES = {
        CRITICAL: "CRITICAL",
        ERROR: "ERROR",
        WARNING: "WARNING",
        INFO: "INFO",
        DEBUG: "DEBUG",
        NOTSET: "NOTSET"
    }
    
    def __init__(self, level: Optional[int] = logging.INFO, console_level: Optional[int] = None, file_level: Optional[int] = None, log_directory: Optional[str] = None):
        """
        Initialize the logger
        
        Args:
            level: Initial logging level for both console and file if specific levels aren't provided
            console_level: Specific log level for console output (defaults to level if not provided)
            file_level: Specific log level for file output (defaults to level if not provided)
            log_directory: Directory where log files will be stored. If None, only console logging is enabled.
        """
        self._level = level
        self._console_level = console_level if console_level is not None else level
        self._file_level = file_level if file_level is not None else level
        self._log_directory = log_directory
        
        # Configure console handler
        self.console_handler = logging.StreamHandler(sys.stdout)
        
        # Configure file handler if log_directory is provided
        self.file_handler = None
        if log_directory:
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            log_file_path = os.path.join(log_directory, f"{timestamp}.log")
            self.file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    
    def _format_log_message(self, level: int, msg: str, module: str, filename: str, lineno: int, process_name: str, thread_name: str, process_id: int) -> str:
        """
        Format the log message according to the standard format
        
        Args:
            level: Log level
            msg: Message to log
            module: Module name
            filename: Filename
            lineno: Line number
            process_name: Process name
            thread_name: Thread name
            process_id: Process ID
            
        Returns:
            Formatted log message
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        level_name = self.LEVEL_NAMES.get(level, "UNKNOWN")
        
        return f"[{timestamp}] {level_name} - {process_name} / {thread_name} ({process_id}) - {module}:{filename}:{lineno} - {msg}"
    
    def _log(self, level: int, msg: Union[str, Exception], json_payload: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a message at the specified level
        
        Args:
            level: Log level
            msg: Message to log (can be an exception object)
            json_payload: Optional JSON payload for DEBUG level
        """
        # Check if we should log to console
        log_to_console = level >= self._console_level
        # Check if we should log to file
        log_to_file = self.file_handler is not None and level >= self._file_level
        
        if not (log_to_console or log_to_file):
            return
            
        if isinstance(msg, Exception):
            msg = f"{type(msg).__name__}: {str(msg)}"
            
        # Get call information
        module, filename, lineno = get_call_info()
        
        # Get process information
        process_name, thread_name, process_id = get_process_info()
        
        # Format the log message
        formatted_msg = self._format_log_message(level, msg, module, filename, lineno, process_name, thread_name, process_id)
        
        # Write to console
        if log_to_console:
            print(formatted_msg)
            
        # Write to file if enabled
        if log_to_file:
            self.file_handler.stream.write(formatted_msg + "\n")
            self.file_handler.stream.flush()
            
        # Add JSON payload for DEBUG level
        if level <= self.DEBUG and json_payload:
            json_str = json.dumps(json_payload, indent=2)
            if log_to_console:
                print(json_str)
            if log_to_file:
                self.file_handler.stream.write(json_str + "\n")
                self.file_handler.stream.flush()

    def log_http_response(self, response, message: str = "HTTP Response") -> None:
        """
        Log an HTTP response with all details at DEBUG level
        
        Args:
            response: HTTP response object (from requests library)
            message: Optional message to include with the log
        """
        if self._level <= self.DEBUG:
            http_details = format_http_response(response)
            self.debug(message, http_details)
    
    def debug(self, msg: Union[str, Exception], json_payload: Optional[Dict[str, Any]] = None) -> None:
        """Log a DEBUG level message."""
        self._log(self.DEBUG, msg, json_payload)
        
    def info(self, msg: Union[str, Exception]) -> None:
        """Log an INFO level message."""
        self._log(self.INFO, msg)
        
    def warning(self, msg: Union[str, Exception]) -> None:
        """Log a WARNING level message."""
        self._log(self.WARNING, msg)
        
    def error(self, msg: Union[str, Exception]) -> None:
        """Log an ERROR level message."""
        self._log(self.ERROR, msg)
        
    def critical(self, msg: Union[str, Exception]) -> None:
        """Log a CRITICAL level message."""
        self._log(self.CRITICAL, msg)

    def exception(self, msg: Union[str, Exception] = "Exception occurred") -> None:
        """
        Log an exception with traceback at ERROR level
        
        Args:
            msg: Message to log along with the exception
        """
        if isinstance(msg, Exception):
            exc_info = (type(msg), msg, None)
        else:
            exc_info = sys.exc_info()
            
        if exc_info[0] is not None:
            exception_msg = f"{msg}: {exc_info[0].__name__}: {str(exc_info[1])}"
            tb_str = "".join(traceback.format_exception(*exc_info))
            full_msg = f"{exception_msg}\n{tb_str}"
            self._log(self.ERROR, full_msg)
        else:
            self._log(self.ERROR, msg)