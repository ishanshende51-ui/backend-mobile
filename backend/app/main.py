from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from app.routes.auth import router as auth_router
from app.routes.trips import router as trips_router
from app.routes.itinerary import router as itinerary_router
from app.routes.expenses import router as expenses_router
from app.routes.documents import router as documents_router

app = FastAPI(title="Smart Travel Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from collections import defaultdict
import time

# Simple in-memory rate limiter (e.g., 100 requests per minute per IP)
RATE_LIMIT = 100
RATE_LIMIT_WINDOW = 60
ip_requests = defaultdict(list)

@app.middleware("http")
async def security_and_logging_middleware(request: Request, call_next):
    # Basic Rate Limiting
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    
    # Clean up old requests
    ip_requests[client_ip] = [req_time for req_time in ip_requests[client_ip] if req_time > current_time - RATE_LIMIT_WINDOW]
    
    if len(ip_requests[client_ip]) >= RATE_LIMIT:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})
        
    ip_requests[client_ip].append(current_time)

    # Logging and executing request
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    print(f"[API] {request.method} {request.url.path} - {response.status_code} ({process_time:.2f}ms)")
    
    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

app.include_router(auth_router)
app.include_router(trips_router)
app.include_router(itinerary_router)
app.include_router(expenses_router)
app.include_router(documents_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "Smart Travel Planner API"}
