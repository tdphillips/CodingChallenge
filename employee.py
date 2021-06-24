# Requires Python 3.7+
from __future__ import annotations

from collections import defaultdict
from functools import reduce
import typing

# In the context of approximating an ORM, this is roughly analogous to making "id" our primary key...
_employees: typing.Dict[int, Employee] = {}
# ... and this a one-to-many relation between managers and their subordinates
_managerOf: typing.Dict[int, typing.Set[Employee]] = defaultdict(set)

class Employee(typing.NamedTuple):
    """
    Roughly approximate an ORM by leveraging a NamedTuple subclass
    """
    # Type hints are to assist programmers; they carry no
    # data validation on their own.
    id: int
    first_name: str
    salary: int
    manager: typing.Optional[int]

    def __str__(self) -> str:
        return f"Employee(id={self.id}, first_name={self.first_name}, salary={self.salary}, manager={self.manager})"
    
    def __eq__(self, obj: typing.Any) -> bool:
        return isinstance(obj, Employee) and obj.id == self.id

    @staticmethod
    def register(id: int, first_name: str, salary: int, manager: typing.Optional[int]) -> Employee:
        """
        Instantiates an Employee instance using the standard
        NamedTuple constructor before registering its "indexes"
        for ease of use later.
        """
        errors = []
        if not isinstance(id, int):
            errors.append(f'ID must be an integer, not {type(id)} ({str(id)})')
        if not isinstance(first_name, str):
            errors.append(f'First name must be a string, not {type(first_name)} ({first_name})')
        if not isinstance(salary, int):
            errors.append(f'Salary must be an integer, not {type(salary)} ({str(salary)})')
        if not (isinstance(manager, int) or manager is None):
            errors.append(f'Manager must be None or an int, not {type(manager)} ({manager})')
        if errors:
            raise ValueError("\n".join(errors))

        if salary < 0:
            salary = 0
            print(f'Employee {id} ({first_name}) had negative salary; charitably assume that they\'re an intern or volunteer.')
        if manager == id:
            raise ValueError(f'Employee {id} ({first_name}) is their own manager; fix input file and try again')

        employee = Employee(id, first_name, salary, manager)
        _employees[id] = employee
        if manager is not None:
            _managerOf[manager].add(employee)
        return employee

    @staticmethod
    def calculate_salary() -> int:
        """
        Calculates the total salary requriements of the organization.
        In other languages, integer overflow would be a concern.
        """
        return reduce(lambda salary, employee: salary + employee.salary, _employees.values(), 0)

    @staticmethod
    def get_top_managers() -> typing.List[Employee]:
        """
        Retrieve what could be the organization's C-level staff.
        """
        return [_employees.get(id) for id in _managerOf.keys() if _employees.get(id).manager is None]

    @classmethod
    def parse_org_chart_branch(cls, startEmployee: Employee) -> typing.Optional[typing.List]:
        """
        Recursively constructs an organization tree until we reach
        all leaf nodes (employees with no direct reports).
        """
        branch = None
        if startEmployee.id in _managerOf:
            branch = [{'employee': employee,
                       'manages': _managerOf.get(employee.id)} for employee in _managerOf.get(startEmployee.id)]
            for employee_doc in branch:
                if employee_doc['manages']:
                    employee_doc['manages'] = cls.parse_org_chart_branch(employee_doc['employee'])
        return branch

    @classmethod
    def get_org_chart(cls) -> typing.List[typing.Dict]:
        """
        Fills out the C-level of our organization tree before
        leveraging `parse_org_chart_branch` to fill out each branch.
        """
        org_chart = []
        top_managers = cls.get_top_managers()
        for top_manager in top_managers:
            org_chart.append({'employee': top_manager, 'manages': cls.parse_org_chart_branch(top_manager)})
        return org_chart


# Guard against star imports polluting the namespace that
# they're importing into
__all__ = ['Employee']