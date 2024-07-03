# Fumblemore

**Warning: The code is immature and can harm the computer. Use at your own risk.**
**Running this Programm can generate arbitrary but syntactically correct code that might be executed on your Computer with unpredictable results.**
**If you like risks run it under an unprivileged account in a sandboxed environment.**

## Project Description

Fumblemore is intended to become a general-purpose agentic workflow system. It is in a very early development state.

## Prerequisites

- Open Interpreter: https://github.com/OpenInterpreter/open-interpreter
- Uvicorn: https://www.uvicorn.org/

### Installation Procedure for Prerequisites

1. Create a Python virtual environment.
2. Navigate to the virtual environment directory.
3. Install Open Interpreter by running `pip install open-interpreter`.
4. Install Uvicorn by running `pip install uvicorn`.

## Installing the Software

1. Clone the repository using `git clone https://github.com/samsingw/fumblemore.git`.
2. Navigate to the `fumblemore` directory.
3. Copy the `server.py` file to the `bin` directory of the previously created virtual environment.

## Invocation

1. Start the FastAPI server:
   - Activate the virtual environment.
   - Run `uvicorn server:app --reload`.
2. Run the main script:
   - Execute `python3 ./fumblemore.py`.
