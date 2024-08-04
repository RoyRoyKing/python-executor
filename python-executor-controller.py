from flask import Flask, jsonify, request
from compilation_wrapper import PythonExecutor

app = Flask(__name__)


@app.route('/compile')
def compile_code():
    code_snippet = request.args.get('code')

    is_valid, compilation_error = PythonExecutor.check_code_validity_in_subprocess(code_snippet)

    return jsonify({'is_valid': is_valid, 'error': compilation_error})


@app.route('/execute')
def execute_code():
    code_snippet = request.args.get('code')

    code_output = PythonExecutor.execute_code_in_subprocess(code_snippet)

    return code_output


if __name__ == '__main__':
    app.run(debug=True)
