from celery.result import AsyncResult
from common.messaging import celery

if __name__ == "__main__":
    async_result = AsyncResult("9812335c-49d1-463b-aa61-aaec373eca89", app=celery)
    result = async_result.result

    print(result)