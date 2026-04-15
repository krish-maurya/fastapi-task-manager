import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), reraise=True)
async def ping_external_service() -> dict:
    # Timeout + retry protect availability when downstream services are flaky.
    timeout = httpx.Timeout(connect=2.0, read=4.0, write=4.0, pool=4.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(settings.external_api_url)
        response.raise_for_status()
        logger.info("external_api_success", extra={"status": response.status_code})
        return {"status": "ok", "code": response.status_code}
