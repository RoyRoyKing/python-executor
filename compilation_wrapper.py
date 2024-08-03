import traceback
from typing import Optional


class PythonExecutor:
    EXEC_COMPILATION_FAILURE_ERRORS = (SyntaxError, NameError, AttributeError, ImportError, IndentationError)
    EXEC_FILENAME = 'shibutzim.py'

    @staticmethod
    def _get_exec_stack_trace(e: Exception) -> str:
        """
        Gets the stack trace only from inside the exec() function.
        Does this by collecting only the stack frames that start with the filename we ran exec() from - which is defined
        in PythonExecutor.EXEC_COMPILATION_FAILURE_ERRORS.
        @param e: The exception to get the stacktrace of.
        @return: The formatted stacktrace string.
        """
        stack_trace_lines = traceback.format_exception(e)
        first_relevant_frame_index = next((frame_index for frame_index, frame_line in enumerate(stack_trace_lines) if
                                           f'File "{PythonExecutor.EXEC_FILENAME}",' in frame_line), -1)

        # "Traceback (most recent call last):" + {List of stack trace lines from inside the exec() function}
        relevant_exception_lines = [stack_trace_lines[0]] + stack_trace_lines[first_relevant_frame_index:]
        return "".join(relevant_exception_lines)

    @staticmethod
    def _execute_code_snippet(snippet: str):
        compiled_snippet = compile(snippet, PythonExecutor.EXEC_FILENAME, 'exec')
        exec(compiled_snippet)

    @staticmethod
    def is_code_valid(snippet: str) -> (bool, Optional[str]):
        try:
            PythonExecutor._execute_code_snippet(snippet)
            return True, None
        except PythonExecutor.EXEC_COMPILATION_FAILURE_ERRORS as e:
            return False, PythonExecutor._get_exec_stack_trace(e)
