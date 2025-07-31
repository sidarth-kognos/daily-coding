# ================================
# run_tests.py
"""
Test runner script
"""
import os
import sys
import subprocess
import structlog
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def print_colored(message: str, color: str = Fore.WHITE):
    """Print colored message"""
    print(f"{color}{message}{Style.RESET_ALL}")

def run_health_check():
    """Run basic health check"""
    print_colored("=== Running Health Check ===", Fore.CYAN)
    
    try:
        from client.db_client import DatabaseClient
        client = DatabaseClient()
        
        if not client.wait_for_server(max_wait_time=10):
            print_colored("❌ Health Check Failed: Server not available", Fore.RED)
            return False
        
        health = client.health_check()
        if health.get("healthy"):
            print_colored("✅ Health Check Passed", Fore.GREEN)
            return True
        else:
            print_colored(f"❌ Health Check Failed: {health.get('message')}", Fore.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Health Check Failed: {str(e)}", Fore.RED)
        return False

def run_pytest_tests():
    """Run pytest tests"""
    print_colored("=== Running Pytest Tests ===", Fore.CYAN)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "client/tests/", 
            "-v", 
            "--tb=short",
            "--color=yes", "-p", "no:langsmith"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print_colored(result.stderr, Fore.YELLOW)
        
        if result.returncode == 0:
            print_colored("✅ All tests passed", Fore.GREEN)
            return True
        else:
            print_colored("❌ Some tests failed", Fore.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Test execution failed: {str(e)}", Fore.RED)
        return False

def run_examples():
    """Run example scripts as modules"""
    print_colored("=== Running Examples ===", Fore.CYAN)
    
    examples = [
        ("Basic Usage", "client.examples.basic_usage"),
        ("Migration Example", "client.examples.migration_example"),
        ("Bulk Operations", "client.examples.bulk_operations")
    ]
    
    for name, module in examples:
        try:
            print_colored(f"Running {name}...", Fore.YELLOW)
            result = subprocess.run(
                [sys.executable, "-m", module],
                capture_output=True, text=True, timeout=30
            )
            
            print(result.stdout)
            if result.stderr:
                print_colored(result.stderr, Fore.YELLOW)
            
            if result.returncode == 0:
                print_colored(f"✅ {name} completed successfully", Fore.GREEN)
            else:
                print_colored(f"❌ {name} failed", Fore.RED)
        except subprocess.TimeoutExpired:
            print_colored(f"⏰ {name} timed out", Fore.YELLOW)
        except Exception as e:
            print_colored(f"❌ {name} failed: {str(e)}", Fore.RED)


def main():
    """Main test runner"""
    print_colored("🚀 Starting Database Client Test Suite", Fore.MAGENTA)
    print_colored("=" * 50, Fore.MAGENTA)
    
    # Check environment
    server_host = os.getenv("GRPC_SERVER_HOST", "localhost")
    server_port = os.getenv("GRPC_SERVER_PORT", "50051")
    print_colored(f"Testing server at {server_host}:{server_port}", Fore.CYAN)
    
    # Run health check first
    if not run_health_check():
        print_colored("❌ Cannot proceed without healthy server", Fore.RED)
        sys.exit(1)
    
    # Run tests
    tests_passed = run_pytest_tests()
    
    # Run examples
    run_examples()
    
    # Summary
    print_colored("=" * 50, Fore.MAGENTA)
    if tests_passed:
        print_colored("🎉 Test Suite Completed Successfully!", Fore.GREEN)
    else:
        print_colored("⚠️  Test Suite Completed with Issues", Fore.YELLOW)
        sys.exit(1)

if __name__ == "__main__":
    main()
 
