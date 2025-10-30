import os
import subprocess

TESTS_DIR = os.path.join(os.path.dirname(__file__), "tests")


def run_all_tests():
    for root, dirs, files in os.walk(TESTS_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Running: {file_path}")
                result = subprocess.run(
                    ["python", file_path], capture_output=True, text=True
                )
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)


if __name__ == "__main__":
    run_all_tests()
