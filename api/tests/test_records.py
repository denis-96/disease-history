import logging
from datetime import datetime

from httpx import AsyncClient, codes


async def test_bad_create_record(client: AsyncClient, user, another_user):
    res = await client.post("/record")
    assert res.status_code == codes.UNAUTHORIZED

    res = await client.post(
        "/record", headers={"Authorization": f"Bearer {user.access_token}"}
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.post(
        "/record",
        json={"title": ""},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.post(
        "/record",
        json={"title": "Запись"},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.post(
        "/record",
        json={"title": "Запись", "rubrics": [{"description": "", "rubric_id": 30}]},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.post(
        "/record",
        json={
            "title": "Запись",
            "rubrics": [
                {"description": "Changes", "rubric_id": 10},
                {"description": "Changes", "rubric_id": 10},
            ],
            "patient_id": 10,
        },
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.post(
        "/record",
        json={
            "title": "Запись",
            "rubrics": [{"description": "Changes", "rubric_id": 30}],
            "patient_id": 10,
        },
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.NOT_FOUND
    assert "patient_id" in res.json()["detail"][0]["loc"]

    patient_id = (
        await client.post(
            "/patient",
            json={},
            headers={"Authorization": f"Bearer {user.access_token}"},
        )
    ).json()["id"]
    res = await client.post(
        "/record",
        json={
            "title": "Запись",
            "rubrics": [{"description": "Changes", "rubric_id": 10}],
            "patient_id": patient_id,
        },
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.NOT_FOUND
    assert "rubric_id" in res.json()["detail"][0]["loc"]

    res = await client.post(
        "/record",
        json={
            "title": "Запись",
            "rubrics": [{"description": "Changes", "rubric_id": 10}],
            "patient_id": patient_id,
        },
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.FORBIDDEN


async def test_good_create_record(client: AsyncClient, user):
    record_data = {
        "title": "Запись",
        "rubrics": [{"description": "Changes", "rubric_id": 1}],
        "patient_id": 3,
    }
    res = await client.post(
        "/record",
        json=record_data,
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert json["id"] == 1
    assert json["title"] == record_data["title"]
    assert json["patient_id"] == record_data["patient_id"]
    assert (
        datetime.strptime(json["date"].split("T")[0], "%Y-%m-%d").day
        == datetime.today().day
    )
    assert json["rubrics"][0] == {
        "description": "Changes",
        "id": 1,
        "rubric": {"id": 1, "section_id": 1, "title": "Желудок"},
    }


async def test_good_update_record(client: AsyncClient, user):
    update_data = {
        "rubrics": [
            {"description": "Изменения", "rubric_id": 1},
            {"description": "Новые изменения", "rubric_id": 2},
        ]
    }
    res = await client.patch(
        "/record",
        params={"record_id": 1},
        json=update_data,
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert len(json["rubrics"]) == 2
    prev_rubric_id = 0
    for rubric in json["rubrics"]:
        assert prev_rubric_id < rubric["id"]
        prev_rubric_id = rubric["id"]

    update_data = {
        "rubrics": [
            {"description": "Новые изменения 2", "rubric_id": 2},
        ]
    }
    res = await client.patch(
        "/record",
        params={"record_id": 1},
        json=update_data,
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert len(json["rubrics"]) == 2
    prev_rubric_id = 0
    for rubric in json["rubrics"]:
        assert prev_rubric_id < rubric["id"]
        prev_rubric_id = rubric["id"]
