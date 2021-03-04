from os import environ

import pytest

pytestmark = pytest.mark.asyncio

IRRD_MEMBEROF_EMPTY_RESPONSE = {"data": {"asSet": [], "autNum": []}}  # type: ignore

IRRD_MEMBEROF_VALID_RESPONSE = {
    "data": {
        "asSet": [
            {"rpslPk": "AS-DIRECT", "objectClass": "as-set", "source": "TEST"},
        ],
        "autNum": [
            {
                "rpslPk": "AS213279",
                "source": "TEST",
                "mntBy": ["TEST-MNT"],
                "memberOfObjs": [
                    {"rpslPk": "AS-VALID-MNTNER", "source": "TEST", "mbrsByRef": ["TEST-MNT"]},
                    {
                        "rpslPk": "AS-VALID-ANY",
                        "source": "TEST",
                        "mbrsByRef": [
                            "OTHER-MNT",
                            "ANY",
                        ],
                    },
                    {
                        "rpslPk": "AS-NOT-VALID-EXCLUDE",
                        "source": "TEST",
                        "mbrsByRef": ["OTHER-MNT"],
                    },
                ],
            }
        ],
    },
}


async def test_asn_invalid(client):
    response = await client.get("/api/sets/asn/invalid")
    assert response.status_code == 404


async def test_asn_valid(client, httpserver):
    environ["IRRD_ENDPOINT"] = httpserver.url_for("/graphql")
    httpserver.expect_request("/graphql").respond_with_json(IRRD_MEMBEROF_VALID_RESPONSE)

    response = await client.get("/api/sets/asn/64500")
    assert response.status_code == 200
    json = response.json()
    assert json["irrsSeen"] == ["TEST"]
    assert set(json["setsPerIrr"]["TEST"]) == {"AS-VALID-ANY", "AS-VALID-MNTNER", "AS-DIRECT"}


async def test_asn_no_data(client, httpserver):
    environ["IRRD_ENDPOINT"] = httpserver.url_for("/graphql")
    httpserver.expect_request("/graphql").respond_with_json(IRRD_MEMBEROF_EMPTY_RESPONSE)

    response = await client.get("/api/sets/asn/64500")
    assert response.status_code == 200

    expected = {"irrsSeen": [], "setsPerIrr": {}}
    assert response.json() == expected
