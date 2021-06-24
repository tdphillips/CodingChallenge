import argparse
import ast
import json
from json.decoder import JSONDecodeError
import sys

from employee import Employee

parser = argparse.ArgumentParser(description="Read employee data, display an org chart, and calculate total salary requirements.")
parser.add_argument('infile', metavar='FILENAME', nargs='?', type=argparse.FileType('r'),
                    help="the file to be read from; blank for stdin", default=sys.stdin)
args = parser.parse_args()

def format_org_chart(hierarchy, indent=0):
    prefix = ''
    if indent >= 2:
        prefix += ' ' * (indent-1)
    if indent >= 1:
        prefix += '├'
    for employee_doc in sorted(hierarchy, key=lambda item: item['employee'].first_name):
        print(f"{prefix}{employee_doc['employee'].first_name}")
        if employee_doc['manages']:
            format_org_chart(employee_doc['manages'], indent+1)


if __name__ == "__main__":
    # Only do work if this file is executed, not if it is imported
    employees = None
    infile = args.infile.read()
    # The documentation around the input file was slightly
    # unclear. JSON requires double quotes and Python's null
    # value is `None` so neither fit.
    # Try parsing as JSON; Try again as Python if that fails;
    # Log an error and quit if neither works.
    try:
        employees = json.loads(infile)
    except JSONDecodeError as e:
        try:
            # The file contents could be construed to be a Python
            # literal. Prefer `ast.literal_eval()` to `eval()` as
            # arbitrary code execution is bad.
            employees = ast.literal_eval(infile)
        except Exception:
            raise RuntimeError("Bad file format; Attempted JSON and Python\n")

    # Register all provided employees in our bespoke "ORM".
    for employee_doc in employees:
        Employee.register(**employee_doc)

    # Generate and display an org chart.
    org_chart = Employee.get_org_chart()
    format_org_chart(org_chart, 0)

    print()

    # Calculate and display the total salary requirements of
    # this organization.
    print(f"Total salary: {Employee.calculate_salary()}")