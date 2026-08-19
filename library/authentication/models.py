import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserRole(models.IntegerChoices):
    VISITOR = 0, "visitor"
    LIBRARIAN = 1, "librarian"


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", UserRole.LIBRARIAN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, default=None, null=True)
    last_name = models.CharField(max_length=20, default=None, null=True)
    middle_name = models.CharField(max_length=20, default=None, null=True)
    email = models.CharField(max_length=100, unique=True, default=None)

    # Виправлено: auto_now_add та auto_now замість виклику datetime.datetime.now()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.IntegerField(choices=UserRole.choices, default=UserRole.VISITOR)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Поля password та is_superuser видалено (успадковані від AbstractBaseUser та PermissionsMixin)
    id = models.AutoField(primary_key=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    # Виправлено: Явне оголошення Meta усуває конфлікт базових класів
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        created_ts = int(self.created_at.timestamp()) if self.created_at else 0
        updated_ts = int(self.updated_at.timestamp()) if self.updated_at else 0
        return (
            f"'id': {self.id}, 'first_name': '{self.first_name}', "
            f"'middle_name': '{self.middle_name}', 'last_name': '{self.last_name}', "
            f"'email': '{self.email}', 'created_at': {created_ts}, "
            f"'updated_at': {updated_ts}, 'role': {self.role}, 'is_active': {self.is_active}"
        )

    def __repr__(self):
        return f"{CustomUser.__name__}(id={self.id})"

    @property
    def username(self):
        return self.email

    @staticmethod
    def get_by_id(user_id):
        return CustomUser.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def delete_by_id(user_id):
        user_to_delete = CustomUser.objects.filter(id=user_id).first()
        if user_to_delete:
            user_to_delete.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        if (
            len(first_name or "") <= 20
            and len(middle_name or "") <= 20
            and len(last_name or "") <= 20
            and len(email) <= 100
            and "@" in email
            and not CustomUser.objects.filter(email=email).exists()
        ):
            # Виправлено: використання create_user для безпечного захешування пароля
            return CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": f"{self.first_name}",
            "middle_name": f"{self.middle_name}",
            "last_name": f"{self.last_name}",
            "email": f"{self.email}",
            "created_at": int(self.created_at.timestamp()) if self.created_at else None,
            "updated_at": int(self.updated_at.timestamp()) if self.updated_at else None,
            "role": self.role,
            "is_active": self.is_active,
        }

    def update(
        self,
        first_name=None,
        last_name=None,
        middle_name=None,
        password=None,
        role=None,
        is_active=None,
    ):
        if first_name is not None and len(first_name) <= 20:
            self.first_name = first_name
        if last_name is not None and len(last_name) <= 20:
            self.last_name = last_name
        if middle_name is not None and len(middle_name) <= 20:
            self.middle_name = middle_name
        if password is not None:
            self.set_password(password)  # Хешування нового пароля
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        return UserRole(self.role).label
