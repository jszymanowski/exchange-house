import asyncio

from tortoise import Tortoise

from app.celery_app import celery_app
from app.core.database import TORTOISE_ORM
from app.core.dependencies import get_exchange_rate_service
from app.core.logger import logger
from app.services.exchange_rate_refresh import build_exchange_rate_refresh
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.services.healthcheck_service import NoURLSetError, healthcheck_service
from app.tasks.notifications import send_exchange_rate_refresh_email
from app.tasks.task_result import TaskResult, failure_result, success_result, warning_result


class RefreshException(Exception):
    pass


class SendEmailException(Exception):
    pass


class CheckInException(Exception):
    pass


async def _exchange_rate_refresh() -> TaskResult:
    async def _update_exchange_rates(exchange_rate_service: ExchangeRateServiceInterface) -> None:
        exchange_rate_refresh = build_exchange_rate_refresh(exchange_rate_service=exchange_rate_service)
        try:
            await exchange_rate_refresh.save()
        except Exception as e:
            raise RefreshException(e) from e

    async def _send_email(exchange_rate_service: ExchangeRateServiceInterface) -> None:
        try:
            await send_exchange_rate_refresh_email(exchange_rate_service=exchange_rate_service)
        except Exception as e:
            raise SendEmailException(e) from e

    async def _check_in() -> None:
        try:
            healthcheck_service.ping_refresh_completed()  # TODO: make this async
        except NoURLSetError as e:
            raise CheckInException("No check-in URL set") from e
        except Exception as e:
            raise CheckInException(e) from e

    await Tortoise.init(config=TORTOISE_ORM)
    try:
        exchange_rate_service = await get_exchange_rate_service()
        await _update_exchange_rates(exchange_rate_service=exchange_rate_service)
        await _send_email(exchange_rate_service=exchange_rate_service)
        await _check_in()
        return success_result()
    except RefreshException as e:
        logger.error(f"Refresh failed: {str(e)}")
        return failure_result(message=f"Refresh failed: {str(e)}")
    except SendEmailException as e:
        logger.warning(f"Send email failed: {str(e)}")
        return warning_result(message=f"Send email failed: {str(e)}")
    except CheckInException as e:
        logger.warning(f"Healthcheck failed: {str(e)}")
        return warning_result(message=f"Healthcheck failed: {str(e)}")
    except Exception as e:
        return failure_result(message=f"Unexpected error: {str(e)}")
    finally:
        await Tortoise.close_connections()


@celery_app.task(name="app.tasks.exchange_rate_refresh")
def exchange_rate_refresh() -> TaskResult:
    return asyncio.run(_exchange_rate_refresh())
