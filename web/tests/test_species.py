"""v1 species endpoint tests."""


def test_list_species(client, seed_species):
    r = client.get("/api/v1/species")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Species"] == "Tyrannosaurus rex"


def test_filter_species_by_name(client, seed_species):
    r = client.get("/api/v1/species", params={"name": "Tyrannosaurus rex"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Species"] == "Tyrannosaurus rex"


def test_filter_species_by_genus(client, seed_species):
    r = client.get("/api/v1/species", params={"genus": "Tyrannosaurus"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["Genus"] == "Tyrannosaurus"


def test_filter_species_by_genus_missing_returns_404(client, seed_species):
    r = client.get("/api/v1/species", params={"genus": "Brontosaurus"})
    assert r.status_code == 404


def test_get_species_by_id(client, seed_species):
    r = client.get(f"/api/v1/species/{seed_species.id}")
    assert r.status_code == 200
    assert r.json()["Species"] == "Tyrannosaurus rex"


def test_get_species_by_id_missing_returns_404(client, seed_species):
    r = client.get("/api/v1/species/9999")
    assert r.status_code == 404
