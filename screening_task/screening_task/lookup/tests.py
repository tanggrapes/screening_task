import pytest
import json
from django.urls import reverse
from screening_task.lookup.models import *
from django.test import client

url = reverse("lookups-url")


@pytest.fixture
def db_setup():
    lookup = LookUp.objects.create(title="The Seven Deadly Sins")
    value = Value.objects.create(
        lookup_id=lookup.id,
        title="Pride",
        definition="is excessive belief in one's own abilities, that interferes with the individual's recognition of the grace of God. It has been called the sin from which all others arise. Pride is also known as Vanity.",
    )


@pytest.mark.django_db
def test_get_lookups(db_setup, client):
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_delete_lookups(db_setup, client):
    response = client.get(url)
    response = client.delete("{}{}/".format(url, response.json()[0].get("id")))
    assert response.status_code == 204


@pytest.mark.django_db
def test_update_lookups_value(db_setup, client):
    new_value = "new value"
    #  get current lookups
    response = client.get(url)
    #  update lookups value definition
    value_id = response.json()[0].get("values")[0]["id"]
    value = Value.objects.get(id=value_id)
    value.definition = new_value
    value.save()
    #  get again current lookups
    response = client.get(url)
    assert response.json()[0].get("values")[0]["definition"] == new_value


@pytest.mark.django_db
def test_add_lookups(client):
    response = client.post(
        url,
        {"title": "title", "values": [{"title": "cool", "definition": "word"}]},
        "application/json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_lookups_search(db_setup, client):
    response = client.get("{}?search=Seven".format(url))
    assert len(response.json()) == 1
    response = client.get("{}?search=The Seven".format(url))
    assert len(response.json()) == 1
    response = client.get("{}?search=Deadly".format(url))
    assert len(response.json()) == 1
    response = client.get("{}?search=anime".format(url))
    assert len(response.json()) == 0
