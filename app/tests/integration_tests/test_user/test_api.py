import pytest
import pytest_asyncio
from httpx import AsyncClient


def abc():
    assert 1 == 1


@pytest.mark.parametrize('email, password, status_code', [
    # ('cot@pes.com', 'kotopes1', 200),
    # ('cot@pes.com', 'kotopes2', 409),
    ('cotpes', 'kotopes3', 422),
])
async def test_register_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post('/auth/register', json={
        'email': email,
        'password': password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ('Pavel@example.com', 'PavelLL', 401),
    ('Pavelll@example.com', 'Pavel', 401),
    ('Pavel@example.com', 'Pavel', 200),
])
async def test_login_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post('/auth/login', json={
        'email': email,
        'password': password,
    })
    assert response.status_code == status_code
