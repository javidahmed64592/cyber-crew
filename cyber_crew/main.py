"""Main entry point for the Cyber Crew application."""

import argparse
import logging
import os
import warnings

from cyber_crew.crew import CyberCrew
from cyber_crew.shell import InteractiveShell
from cyber_crew.tools.utils import get_shell, set_global_vars

# Configure logging
logging.basicConfig(format="[*] (%(asctime)s) %(message)s", datefmt="%H:%M:%S", level=logging.INFO)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the interactive shell connection."""
    parser = argparse.ArgumentParser(description="Interactive shell connection to remote system")
    parser.add_argument("--username", "-u", required=True, help="Username for authentication")
    parser.add_argument("--password", "-p", required=True, help="Password for authentication")
    parser.add_argument("--prompt", "-m", required=True, help="Mission prompt to initiate the crew")
    parser.add_argument("--config", "-c", default="config.yaml", help="Path to the config.yaml file")
    parser.add_argument("--n_iterations", "-n", default=1, type=int, help="Number of training iterations")
    parser.add_argument("--filename", "-f", default="training_data.json", help="Path to the training data file")
    return parser.parse_args()


def get_context_dictionary(args: argparse.Namespace) -> dict[str, str]:
    """Get the context dictionary for the crew."""
    return {
        "mission_prompt": args.prompt,
    }


def create_shell(username: str, password: str) -> None:
    """Create a shell session with the given username and password."""
    logger.info("Establishing shell connection...")
    shell = InteractiveShell(username=username, password=password)
    set_global_vars(shell=shell)


def run() -> None:
    """Run the crew."""
    args = parse_args()
    context = get_context_dictionary(args)
    cyber_crew = CyberCrew()
    set_global_vars(manager_agent=cyber_crew.manager_agent)

    try:
        logger.info("Kicking off mission...")
        result = cyber_crew.crew().kickoff(inputs=context)
        logger.info(f"Mission result: {result}")
    except Exception as e:
        msg = f"An error occurred while running the crew: {e}"
        logger.exception(msg)
        raise
    finally:
        logger.info("Closing shell session...")
        get_shell().close()
        logger.info("Complete!")


def train() -> None:
    """Train the crew for a given number of iterations."""
    args = parse_args()
    context = get_context_dictionary(args)
    cyber_crew = CyberCrew()
    set_global_vars(manager_agent=cyber_crew.manager_agent)

    try:
        logger.info(f"Training the crew for {args.n_iterations} iterations...")
        cyber_crew.crew().train(n_iterations=int(args.n_iterations), filename=args.filename, inputs=context)
        logger.info(f"Training completed. Data saved to {args.filename}")
    except Exception as e:
        msg = f"An error occurred while training the crew: {e}"
        logger.exception(msg)
        raise
    finally:
        logger.info("Closing shell session...")
        get_shell().close()
        logger.info("Complete!")


def replay() -> None:
    """Replay the crew execution from a specific task."""
    args = parse_args()
    cyber_crew = CyberCrew()
    set_global_vars(manager_agent=cyber_crew.manager_agent)

    try:
        logger.info(f"Replaying crew execution for task ID: {args.task_id}")
        cyber_crew.crew().replay(task_id=args.task_id)
    except Exception as e:
        msg = f"An error occurred while replaying the crew: {e}"
        logger.exception(msg)
        raise
    finally:
        logger.info("Closing shell session...")
        get_shell().close()
        logger.info("Complete!")


def test() -> None:
    """Test the crew execution and returns the results."""
    args = parse_args()
    context = get_context_dictionary(args)
    cyber_crew = CyberCrew()
    set_global_vars(manager_agent=cyber_crew.manager_agent)

    try:
        logger.info(f"Testing the crew with {args.n_iterations} iterations using {os.environ.get('MODEL')}...")
        cyber_crew.crew().test(n_iterations=int(args.n_iterations), eval_llm=os.environ.get("MODEL"), inputs=context)
    except Exception as e:
        msg = f"An error occurred while testing the crew: {e}"
        logger.exception(msg)
        raise
    finally:
        logger.info("Closing shell session...")
        get_shell().close()
        logger.info("Complete!")
