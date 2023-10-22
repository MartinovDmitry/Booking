import pytest
from httpx import AsyncClient

from app.users.dao import UserDAO


@pytest.mark.parametrize('model_id, email, is_present', [
    (1, "fedor@moloko.ru", True),
    (2, "sharik@moloko.ru", True),
    (4, "sharik@moloko.ru", False),
])
async def test_get_user_by_id(model_id, email, is_present):
    response = await UserDAO.get_by_id(model_id)
    if is_present:
        assert response
        assert response.id == model_id
        assert response.email.strip() == email
    else:
        assert not response
