#!/usr/bin/env python3
"""
Test runner script with convenient options
Usage: python run_tests.py [options]
"""
import sys
import argparse
import subprocess
from pathlib import Path


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")


def run_command(cmd, description):
    print(f"{Colors.BLUE}▶ {description}...{Colors.END}")
    print(f"{Colors.YELLOW}Command: {' '.join(cmd)}{Colors.END}\n")

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n{Colors.GREEN}✓ {description} completed successfully!{Colors.END}\n")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.RED}✗ {description} failed with exit code {e.returncode}{Colors.END}\n")
        return False
    except FileNotFoundError:
        print(f"\n{Colors.RED}✗ Command not found. Make sure pytest is installed.{Colors.END}\n")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="API Automation Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --mock               # Run mock tests only
  python run_tests.py --integration        # Run integration tests
  python run_tests.py --all                # Run all tests
  python run_tests.py --parallel           # Run all tests in parallel
  python run_tests.py --allure             # Run all tests + Allure report
  python run_tests.py tests/integration/test_cropservice_get_api.py
        """
    )

    # Test selection options
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument('--all', action='store_true', help='Run all tests')
    test_group.add_argument('--mock', action='store_true', help='Run mock tests only')
    test_group.add_argument('--integration', action='store_true', help='Run integration tests')
    test_group.add_argument('--unit', action='store_true', help='Run unit tests')

    # Execution options
    parser.add_argument('--parallel', action='store_true', help='Run tests in parallel')
    parser.add_argument('-n', '--workers', type=int, help='Number of parallel workers (default: auto)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet output')

    # Reporting options
    parser.add_argument('--allure', action='store_true', help='Generate Allure report')

    # Other options
    parser.add_argument('--rerun', type=int, help='Rerun failed tests N times')
    parser.add_argument('path', nargs='?', help='Specific test file or directory')

    args = parser.parse_args()

    # Build pytest command
    cmd = ['pytest']

    # Add test path or default to tests/
    if args.path:
        cmd.append(args.path)
    else:
        cmd.append('tests/')

    # Add markers / paths
    if args.mock:
        cmd.extend(['-m', 'mock'])
        description = "Running Mock Tests"
    elif args.integration:
        cmd.extend(['-m', 'integration'])
        description = "Running Integration Tests"
    elif args.unit:
        cmd.append('tests/unit/')
        description = "Running Unit Tests"
    elif args.all:
        description = "Running All Tests"
    else:
        description = "Running All Tests"

    # Parallel execution
    if args.parallel:
        if args.workers:
            cmd.extend(['-n', str(args.workers)])
        else:
            cmd.extend(['-n', 'auto'])
        description += " (Parallel)"

    # Verbosity
    if args.verbose:
        cmd.append('-vv')
    elif args.quiet:
        cmd.append('-q')
    else:
        cmd.append('-v')

    # Rerun failures
    if args.rerun:
        cmd.extend(['--reruns', str(args.rerun)])
        description += f" (Rerun: {args.rerun})"

    # Allure
    if args.allure:
        cmd.extend(['--alluredir=./reports/allure-results'])
        description += " + Allure"

    # Create directories if needed
    Path('./reports/allure-results').mkdir(parents=True, exist_ok=True)
    Path('./logs').mkdir(parents=True, exist_ok=True)

    # Run tests
    print_header(description)
    success = run_command(cmd, description)

    # Open Allure report if requested
    if args.allure and success:
        print_header("Generating Allure Report")
        subprocess.run(['allure', 'serve', './reports/allure-results'])

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
