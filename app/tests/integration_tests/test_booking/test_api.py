import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    *[(2, '2030-08-15', '2030-08-24', 200)]*3
])
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.post('/bookings/', params={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to,
    })
    assert response.status_code == status_code
