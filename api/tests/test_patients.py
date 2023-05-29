from httpx import AsyncClient, codes


async def test_create_patient(client: AsyncClient, user):
    base_response_data = {
        "full_name": "Пациент",
        "age": 0,
        "diagnosis": None,
        "complaints": None,
        "anamnesis": None,
        "heredity": None,
        "treatment_plan": None,
        "treatment_comments": None,
    }
    request_json = {}
    # 1
    res = await client.post(
        "/patient",
        json=request_json,
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    response_data = res.json()
    assert res.status_code == codes.OK
    assert response_data.pop("user_id") > 0
    assert response_data.pop("id") > 0
    assert response_data == {
        **base_response_data,
    }

    request_json["full_name"] = "denis"
    request_json["age"] = 20
    request_json["heredity"] = "Наследственность"

    # 2
    res = await client.post(
        "/patient",
        json=request_json,
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    response_data = res.json()
    assert res.status_code == codes.OK
    assert response_data.pop("user_id") > 0
    assert response_data.pop("id") > 0
    assert response_data == {
        **base_response_data,
        **request_json,
    }


async def test_bad_get_patient(client: AsyncClient, another_user):
    res = await client.get(
        "/patient",
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.get(
        "/patient",
        params={},
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.get(
        "/patient",
        params={"patient_id": 23133},
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.NOT_FOUND

    res = await client.get(
        "/patient",
        params={"patient_id": 1},
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.FORBIDDEN


async def test_good_get_patient(client: AsyncClient, user):
    res = await client.get(
        "/patient",
        params={"patient_id": 1},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert json["id"] == 1
    assert json["user_id"] > 0
    assert len(json["full_name"]) >= 3
    assert json["age"] >= 0


async def test_get_all_patients(client: AsyncClient, user, another_user):
    res = await client.get(
        "/patient/all",
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert len(json) == 2
    for patient in json:
        assert patient["user_id"] > 0
        assert len(patient["full_name"]) >= 3
        assert patient["age"] >= 0

    res = await client.get(
        "/patient/all",
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert len(json) == 0


async def test_bad_update_patient(client: AsyncClient, user, another_user):
    res = await client.patch(
        "/patient",
        params={"patient_id": 3432},
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.NOT_FOUND

    res = await client.patch(
        "/patient",
        params={"patient_id": 1},
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.FORBIDDEN

    res = await client.patch(
        "/patient",
        params={"patient_id": 1},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.patch(
        "/patient",
        params={"patient_id": 1},
        json={"full_name": ""},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY

    res = await client.patch(
        "/patient",
        params={"patient_id": 1},
        json={"age": "-10"},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    assert res.status_code == codes.UNPROCESSABLE_ENTITY


async def test_good_update_patient(client: AsyncClient, user):
    update_data = {
        "full_name": "Новое имя",
        "age": 30,
        "diagnosis": "Повседневная практика показывает, что сложившаяся структура организации позволяет оценить значение дальнейш",
        "complaints": "порядка, а также реализация намеченных плановых заданий обеспечивает широкому кругу (специалистов) участие в форми",
        "anamnesis": "рессивного развития. Значимость этих проблем настолько очевидна, что укрепление и развитие структуры представляет собой интересный эксперимент проверки форм развития. Равным образом новая модель организацио",
        "heredity": "кадров, соответствует насущным потребностям. Повседневная практика показывает, что начало повседневной работы по ",
        "treatment_plan": "Не следует, однако забывать, что новая модель организационной деятельности требуют определения и уточнения форм развития. ",
        "treatment_comments": " Таким образом консультация с широким активом влечет за собой процесс внедрения и модернизации соответствующий условий активизации. Таким образом рамки и место обучения кадров представляет собой интересный экспе",
    }
    res = await client.patch(
        "/patient",
        params={"patient_id": 1},
        json=update_data,
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert json.pop("id") == 1
    assert json.pop("user_id") > 0
    assert json == update_data


async def test_bad_delete_patient(client: AsyncClient, another_user):
    res = await client.delete(
        "/patient",
        params={"patient_id": 23133},
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.NOT_FOUND

    res = await client.delete(
        "/patient",
        params={"patient_id": 1},
        headers={"Authorization": f"Bearer {another_user.access_token}"},
    )
    assert res.status_code == codes.FORBIDDEN


async def test_good_delete_patient(client: AsyncClient, user):
    res = await client.delete(
        "/patient",
        params={"patient_id": 1},
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert json["deleted_patient_id"] == 1

    res = await client.get(
        "/patient/all",
        headers={"Authorization": f"Bearer {user.access_token}"},
    )
    json = res.json()
    assert res.status_code == codes.OK
    assert len(json) == 1
