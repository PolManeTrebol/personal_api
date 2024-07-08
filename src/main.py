import sys
import traceback
import os
from injector import Injector, UnsatisfiedRequirement, CircularDependency, UnknownProvider, CallError
from werkzeug.exceptions import HTTPException

from src.server import configure, create_app


def run_test() -> None:
    print('This is a test run.')
    sys.exit(0)


if __name__ == "__main__":
    if 'DO_TEST_RUN' in os.environ and os.environ['DO_TEST_RUN'] == 'True':
        run_test()

    # Host MUST be 0.0.0.0
    try:
        injector = Injector([configure])
        app = create_app(injector=injector)
        app.run(host="0.0.0.0", port=app.config["FLASK_PORT"])  # nosec B104

    except KeyboardInterrupt:
        print("Server interrupted by user, shutting down.")
    except UnsatisfiedRequirement as e:
        print(f"Dependency injection error: {e}")
        traceback.print_exc()
    except CircularDependency as e:
        print(f"Circular dependency detected: {e}")
        traceback.print_exc()
    except UnknownProvider as e:
        print(f"Unknown provider error: {e}")
        traceback.print_exc()
    except CallError as e:
        print(f"Call error: {e}")
        traceback.print_exc()
    except HTTPException as e:
        print(f"HTTP exception: {e}")
        traceback.print_exc()
    except Exception as e:  # pylint: disable=broad-except
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
