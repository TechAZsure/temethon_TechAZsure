from django.db import models
from django.contrib.auth.hashers import make_password

class BankBranch(models.Model):
    branch_name = models.CharField(max_length=100, unique=True)
    bank_name = models.CharField(max_length=100)
    manager_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    branch_code = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)  # Hashed password

    def set_password(self, raw_password):
        """Hash the password before saving."""
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.bank_name} - {self.branch_name}"
