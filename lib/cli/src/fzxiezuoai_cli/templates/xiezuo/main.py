#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from {{folder_name}}.xiezuo import {{xiezuo_name}}

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the xiezuo.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }

    try:
        {{xiezuo_name}}().xiezuo().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the xiezuo: {e}")


def train():
    """
    Train the xiezuo for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        {{xiezuo_name}}().xiezuo().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the xiezuo: {e}")

def replay():
    """
    Replay the xiezuo execution from a specific task.
    """
    try:
        {{xiezuo_name}}().xiezuo().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the xiezuo: {e}")

def test():
    """
    Test the xiezuo execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        {{xiezuo_name}}().xiezuo().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the xiezuo: {e}")

def run_with_trigger():
    """
    Run the xiezuo with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "fzxiezuoai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = {{xiezuo_name}}().xiezuo().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the xiezuo with trigger: {e}")
