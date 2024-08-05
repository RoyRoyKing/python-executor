import os
import sys
import traceback
from typing import Optional
import multiprocessing

"""
NOTE
This code is quite Arabic. 
Might need refactor later, was written by a Python novice under some time pressure :)
"""


class PythonExecutor:
    EXEC_COMPILATION_FAILURE_ERRORS = (SyntaxError, NameError, AttributeError, ImportError, IndentationError)
    EXEC_FILENAME = 'shibutzim.py'
    PROCESS_OUTPUT_FILE_EXTENSION = '.out'

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

        relevant_exception_lines = [stack_trace_lines[0]] + stack_trace_lines[
                                                            first_relevant_frame_index:]  # "Traceback (most recent call last):" + {List of stack trace lines from inside the exec() function}
        return "".join(relevant_exception_lines)

    @staticmethod
    def _execute_code_snippet(snippet: str):
        compiled_snippet = compile(snippet, PythonExecutor.EXEC_FILENAME, 'exec')
        exec(compiled_snippet)

    @staticmethod
    def _is_code_valid(snippet: str) -> (bool, Optional[str]):
        try:
            PythonExecutor._execute_code_snippet(snippet)
            return True, None
        except PythonExecutor.EXEC_COMPILATION_FAILURE_ERRORS as e:
            return False, PythonExecutor._get_exec_stack_trace(e)

    @staticmethod
    def _change_stdout_and_check_code_validity(snippet: str):
        output_filename = str(os.getpid()) + PythonExecutor.PROCESS_OUTPUT_FILE_EXTENSION

        with open(output_filename, 'w') as output_file:
            is_code_valid, compilation_error = PythonExecutor._is_code_valid(snippet)

            print(is_code_valid)

            print(is_code_valid, file=output_file)
            if compilation_error:
                print(compilation_error, file=output_file)

    @staticmethod
    def check_code_validity_in_subprocess(snippet: str):
        subprocess = multiprocessing.Process(target=PythonExecutor._change_stdout_and_check_code_validity,
                                             args=(snippet,))
        subprocess.start()
        subprocess.join()

        process_output_filename = str(subprocess.pid) + PythonExecutor.PROCESS_OUTPUT_FILE_EXTENSION

        with open(process_output_filename, 'r') as process_output_file:
            is_file_valid = process_output_file.readline().strip() == 'True'
            compilation_error = process_output_file.read().strip()

        os.remove(process_output_filename)
        
        return is_file_valid, compilation_error

    @staticmethod
    def _change_stdout_and_execute_code(snippet: str):
        output_filename = str(os.getpid()) + PythonExecutor.PROCESS_OUTPUT_FILE_EXTENSION

        with open(output_filename, 'w') as output_file:
            try:
                sys.stdout = output_file
                sys.stderr = output_file

                PythonExecutor._execute_code_snippet(snippet)
            except Exception as e:
                print(PythonExecutor._get_exec_stack_trace(e), file=output_file)

    @staticmethod
    def execute_code_in_subprocess(snippet: str):
        subprocess = multiprocessing.Process(target=PythonExecutor._change_stdout_and_execute_code,
                                             args=(snippet,))
        subprocess.start()
        subprocess.join()

        process_output_filename = str(subprocess.pid) + PythonExecutor.PROCESS_OUTPUT_FILE_EXTENSION

        with open(process_output_filename, 'r') as process_output_file:
            process_output = process_output_file.read()
        
        os.remove(process_output_filename)

        return process_output