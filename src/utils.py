# Author: Michał Kostyk for Smartschool Inc.
# Date: 2023
# Version: 1.0.0
# Description: Utility functions and constants used in other scripts.

FAIL = '\033[91m'
ENDC = '\033[0m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
BOLD = '\033[1m'

def print_ok(msg):
    print(OKGREEN + msg + ENDC)

def print_generic(msg):
    print(BOLD + msg + ENDC)

def fatal(msg):
    print(FAIL + BOLD + "FATAL ERROR: " + msg)
    exit(1)

def print_err(msg):
    print(FAIL + BOLD + "Error: " + msg + ENDC)

def print_warn(msg):
    print(WARNING + BOLD + "Warning: " + msg + ENDC)