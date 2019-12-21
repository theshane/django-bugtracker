from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class MyAccountManager(BaseUserManager):
    def create_user(self, email=None, full_name=None, password=None):
        if not email:
            return ValueError("Users must have an email")

        if not full_name:
            return ValueError("Users must have a full name")

        user = self.model(
            email=self.normalize_email(email), full_name=full_name, password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        if not email:
            return ValueError("Users must have an email")

        if not full_name:
            return ValueError("Users must have a full name")

        user = self.create_user(email=email, full_name=full_name)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.full_name}(<{self.email}>)"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active


class Status(models.Model):
    display_text = models.CharField(max_length=50)
    is_open = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_in_progress = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_status_enums():
        return [
            {
                "display_text": "Open",
                "is_open": True,
                "is_closed": False,
                "is_in_progress": False,
                "is_blocked": False,
            },
            {
                "display_text": "Closed",
                "is_open": False,
                "is_closed": True,
                "is_in_progress": False,
                "is_blocked": False,
            },
            {
                "display_text": "In Progress",
                "is_open": False,
                "is_closed": False,
                "is_in_progress": True,
                "is_blocked": False,
            },
            {
                "display_text": "Blocked",
                "is_open": False,
                "is_closed": False,
                "is_in_progress": False,
                "is_blocked": True,
            },
        ]


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    project_status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="project_create_user",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "title": self.title,
            "project_status": self.project_status.id,
            "created_by": self.created_by.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class TicketType(models.Model):
    display_text: models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_ticket_type_enums():
        return ["Bug", "Story", "Epic"]


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=2000)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.DO_NOTHING)
    assigned_to = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="ticket_create_user",
    )
    project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    ticket_status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RelatedTickets(models.Model):
    ticket_one = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    ticket_two = models.ForeignKey(
        Ticket, on_delete=models.DO_NOTHING, related_name="realted_ticket"
    )
    is_epic = models.BooleanField()
