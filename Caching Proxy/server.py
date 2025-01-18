from cachetools import TTLCache
from fastapi import FastAPI, Request, Response
import uvicorn
from typing import Optional
import requests

cache = TTLCache(maxsize=1024, ttl=60)

def start_server(port, origin):
    
    app = FastAPI()

    @app.api_route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
    async def proxy_request(request: Request, path: Optional[str] = ""):
        full_url = str(request.url)

        if full_url in cache:
            cached_data = cache[full_url]
            response = Response(
                content=cached_data["content"],
                status_code=cached_data["status_code"],
                headers=cached_data["headers"],
            )
            response.headers["X-Cache"] = "HIT"

        else:
            url = f'{origin}/{path}'
            if request.query_params:
                url += f"?{request.query_params}"

            headers = dict(request.headers)

            url_response = requests.request(
                method=request.method,
                url=full_url,
                headers=headers,
                data=await request.body(),
                allow_redirects=False,
            )
            cache[full_url] = {
                "content": url_response.content,
                "status_code": url_response.status_code,
                "headers": dict(url_response.headers),
            }

            response = Response(
                content=url_response.content,
                status_code=url_response.status_code,
                headers=dict(url_response.headers),
            )
            
            response.headers["X-Cache"] = "MISS"

        return response

    uvicorn.run(app, host="127.0.0.1", port=port)

def clear_cache():
    cache.clear()