# -*- coding: utf-8 -*-
# Copyright 2024 Alejandro Olano <Github@alejo-code>

from odoo.tests import TransactionCase


class TestEmployeeProject(TransactionCase):

    def setUp(self):
        # Este método se ejecuta antes de cada prueba
        super(TestEmployeeProject, self).setUp()

        self.employee = self.env["hr.employee"].create(
            {
                "name": "John Doe",
                "job_id": self.env.ref("hr.job_all").id,
            }
        )

    def test_create_employee_project(self):

        project = self.env["employee.project"].create(
            {
                "name": "Project A",
                "employee_id": self.employee.id,
                "description": "Test project description",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
            }
        )

        self.assertEqual(project.name, "Project A")
        self.assertEqual(project.employee_id, self.employee)
        self.assertEqual(project.description, "Test project description")
        self.assertEqual(project.start_date, "2024-01-01")
        self.assertEqual(project.end_date, "2024-12-31")

    def test_employee_project_validation(self):

        with self.assertRaises(Exception):
            self.env["employee.project"].create(
                {
                    "name": "",
                    "employee_id": self.employee.id,
                }
            )

    def test_project_dates(self):

        project = self.env["employee.project"].create(
            {
                "name": "Project B",
                "employee_id": self.employee.id,
                "start_date": "2024-05-01",
                "end_date": "2024-08-01",
            }
        )

        # Verificamos las fechas
        self.assertEqual(project.start_date, "2024-05-01")
        self.assertEqual(project.end_date, "2024-08-01")

    def test_project_no_end_date(self):

        project = self.env["employee.project"].create(
            {
                "name": "Project C",
                "employee_id": self.employee.id,
                "start_date": "2024-06-01",
            }
        )

        # Verificamos que la fecha de finalización sea None (no definida)
        self.assertIsNone(project.end_date)
