from django.test import TestCase, Client
import bugtracker.models as models
from django.urls import reverse
import json
from django.core.management import call_command


class TestProjectApi(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = "/api/project"
        self.user = models.Account.objects.create_user(
            email="test_user@shaneburgess.net", full_name="Test User", password="test"
        )
        self.client.login(email="test_user@shaneburgess.net", password="test")
        call_command("init_db", "--quiet=true")
        self.test_projects = [
            {
                "title": "Test Project 1",
                "description": "Test Project 1 Description",
                "project_status": 1,
            },
            {
                "title": "Test Project 2",
                "description": "Test Project 2 Description",
                "project_status": 1,
            },
        ]

    def add_project_to_db(self):
        new_project = models.Project(
            title=self.test_projects[0]["title"],
            description=self.test_projects[0]["description"],
            project_status=models.Status.objects.get(id=1),
            created_by=self.user,
        )
        new_project.save()
        return new_project

    def test_project_post(self):
        self.add_project_to_db()
        response = self.client.post(self.base_url, data=self.test_projects[0])
        self.assertEqual(response.status_code, 200)
        ret_data = json.loads(response.content.decode("utf8"))
        self.assertEqual(
            ret_data["title"],
            self.test_projects[0]["title"],
            "Project Titles do not match",
        )
        self.assertEqual(
            ret_data["created_by"], self.user.id, "Created by is not the logged in user"
        )
        project_from_db = models.Project.objects.get(id=ret_data["id"])
        self.assertEqual(
            project_from_db.id,
            ret_data["id"],
            "The project returned from api is not in the database",
        )

    def test_project_get_list(self):
        self.add_project_to_db()
        response = self.client.get("/api/projects", data=self.test_projects[0])
        self.assertEqual(response.status_code, 200)
        ret_data = json.loads(response.content.decode("utf8"))
        self.assertEqual(
            ret_data[0]["title"],
            self.test_projects[0]["title"],
            "Test project was not in the list",
        )

    def test_project_update(self):
        test_project = self.add_project_to_db()
        updated_project = self.test_projects[0].copy()
        updated_project["title"] = "Updated"
        updated_project["project_status"] = 2
        response = self.client.post(
            "{0}/{1}".format(self.base_url, test_project.id), data=updated_project
        )
        self.assertEqual(response.status_code, 200)
        ret_data = json.loads(response.content.decode("utf8"))
        self.assertEqual(ret_data["title"], "Updated", "Project title not updated")
        self.assertEqual(ret_data["project_status"], 2, "Project status not updated")
        project_from_db = models.Project.objects.get(id=ret_data["id"])
        self.assertEqual(
            project_from_db.project_status.id,
            2,
            "The project was not updated in the db",
        )
