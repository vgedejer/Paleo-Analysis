"""v1 genera endpoint tests."""


def test_list_genera(client, seed_genus):
    r = client.get("/api/v1/genera")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Genus"] == "Tyrannosaurus"
    # list returns basic shape — TaxonSize is detail-only
    assert "TaxonSize" not in body[0]


def test_filter_genera_by_name(client, seed_genus):
    r = client.get("/api/v1/genera", params={"name": "Tyrannosaurus"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Genus"] == "Tyrannosaurus"


def test_filter_genera_by_name_missing_returns_404(client, seed_genus):
    r = client.get("/api/v1/genera", params={"name": "Diplodocus"})
    assert r.status_code == 404


def test_get_genus_by_id_full_default(client, seed_genus):
    r = client.get(f"/api/v1/genera/{seed_genus.id}")
    assert r.status_code == 200
    body = r.json()
    assert body["Genus"] == "Tyrannosaurus"
    assert body["TaxonSize"] == 12  # detail only


def test_get_genus_by_id_basic(client, seed_genus):
    r = client.get(f"/api/v1/genera/{seed_genus.id}", params={"detail": "basic"})
    assert r.status_code == 200
    body = r.json()
    assert body["Genus"] == "Tyrannosaurus"
    assert "TaxonSize" not in body


def test_get_genus_by_id_missing_returns_404(client, seed_genus):
    r = client.get("/api/v1/genera/9999")
    assert r.status_code == 404


def test_sanitization_fills_null_fields(client, db):
    """Basic genus response should fill null columns with NOT_SPECIFIED."""
    from models.genus import Genus

    db.add(Genus(id=99, Genus="Weirdosaurus"))
    db.commit()

    r = client.get("/api/v1/genera", params={"name": "Weirdosaurus"})
    assert r.status_code == 200
    body = r.json()[0]
    assert body["Family"] == "NOT SPECIFIED"
    assert body["Diet"] == "NOT SPECIFIED"
