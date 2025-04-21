import pytest
from django.core.management import call_command

@pytest.fixture(autouse=True)
def reset_db(db, django_db_blocker):
    django_db_blocker.unblock()
    call_command("flush", "--no-input")

