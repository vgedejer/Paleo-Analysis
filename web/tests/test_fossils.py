"""v1 fossils endpoint tests."""


def test_list_fossils(client, seed_fossil):
    r = client.get("/api/v1/fossils")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Fossil"] == "Tyrannosaurus rex"


def test_filter_fossils_by_species(client, seed_fossil):
    r = client.get("/api/v1/fossils", params={"species": "Tyrannosaurus rex"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Country"] == "USA"
    # filter endpoint returns detail shape
    assert body[0]["County"] == "Garfield"


def test_filter_fossils_by_genus(client, seed_fossil):
    r = client.get("/api/v1/fossils", params={"genus": "Tyrannosaurus"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1


def test_filter_fossils_by_genus_missing_returns_404(client, seed_fossil):
    r = client.get("/api/v1/fossils", params={"genus": "Brontosaurus"})
    assert r.status_code == 404


def test_get_fossil_by_id(client, seed_fossil):
    r = client.get(f"/api/v1/fossils/{seed_fossil.id}")
    assert r.status_code == 200
    body = r.json()
    assert body["Fossil"] == "Tyrannosaurus rex"
    assert body["PaleoModel"] == "Scotese"


def test_get_fossil_by_id_missing_returns_404(client, seed_fossil):
    """Was previously broken: services/fossils.py:32 returned HTTPException
    instead of raising. Now yields a proper 404."""
    r = client.get("/api/v1/fossils/9999")
    assert r.status_code == 404
    assert "detail" in r.json()


def test_list_fossils_handles_null_coordinates(client, db):
    """Previously crashed because constants.INVALID_COORDINATE was referenced
    but not defined. Now unified under INVALID_FLOAT."""
    from models.fossil import Fossil

    db.add(Fossil(id=50, Fossil="PartialFossil"))  # all other columns null
    db.commit()
    r = client.get("/api/v1/fossils")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Longitude"] == -999.99
    assert body[0]["Country"] == "NOT SPECIFIED"
