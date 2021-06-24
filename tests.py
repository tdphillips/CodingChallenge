import unittest

import employee


class TestEmployeeORM(unittest.TestCase):
    def tearDown(self):
        employee._employees.clear()
        employee._managerOf.clear()

    def test_later_identical_ids_win(self):
        employee.Employee.register(0, 'name1', 0, None)
        emp = employee.Employee.register(0, 'name2', 0, None)
        self.assertEqual(len(employee._employees), 1)
        self.assertEqual(employee._employees[0].first_name, emp.first_name)

    def test_employee_salary_bounds(self):
        num_employees = 0
        salaries = [0, 100, -300]
        for idx, salary in enumerate(salaries):
            emp = employee.Employee.register(idx, 'firstname', salary, None)
            if salary == salaries[-1]:
                self.assertEqual(emp.salary, 0)
        self.assertEqual(len(employee._employees), num_employees+3)

        employee._employees.clear()
        for salary in [None, 'a', 1.3]:
            with self.assertRaises(ValueError):
                employee.Employee.register(0, 'firstname', salary, None)
        self.assertEqual(len(employee._employees), 0)

    def test_cannot_manage_self(self):
        id = 100
        with self.assertRaises(ValueError):
            employee.Employee.register(id, 'firstname', 0, id)

    def test_total_salary_calculation(self):
        salaries = list(range(100))
        for idx, salary in enumerate(salaries):
            employee.Employee.register(idx, 'firstname', salary, None)
        
        total_salary = employee.Employee.calculate_salary()
        self.assertEqual(total_salary, sum(salaries))

if __name__ == '__main__':
    unittest.main()