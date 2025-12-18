import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_use_case_factory
from api.main import app
from core.factories.use_case_factory import UseCaseFactory
from core.infra.mocks import (
    MockOrderRepository,
    MockProductRepository,
    MockUserRepository,
)


# --- Mocks (Recriados a cada teste) ---
@pytest.fixture
def user_repository():
    return MockUserRepository()


@pytest.fixture
def product_repository():
    return MockProductRepository()


@pytest.fixture
def order_repository():
    return MockOrderRepository()


# --- Factory com Mocks ---
@pytest.fixture
def use_case_factory(user_repository, product_repository, order_repository):
    return UseCaseFactory(
        user_repository=user_repository,
        product_repository=product_repository,
        order_repository=order_repository,
    )


@pytest_asyncio.fixture
async def client(use_case_factory):
    app.dependency_overrides[get_use_case_factory] = lambda: use_case_factory

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer token_falso_para_teste"}
