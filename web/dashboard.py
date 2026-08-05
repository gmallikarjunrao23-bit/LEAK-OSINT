"""
Admin Web Dashboard — FastAPI
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from repositories.payment_repo import PaymentRepository
from repositories.user_repo import UserRepository
from repositories.query_repo import QueryRepository
from services.payment_service import PaymentService
from config.settings import settings
import os

app = FastAPI(title="LeakOSINT Pro — Admin")
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# === HARDCODE YOUR ADMIN ID HERE ===
ADMIN_IDS = [6345778491]  # Ne ID

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login_post(request: Request, telegram_id: int = Form(...)):
    if is_admin(telegram_id):
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie("admin_id", str(telegram_id))
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid admin ID"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    admin_id = request.cookies.get("admin_id")
    if not admin_id or not is_admin(int(admin_id)):
        return RedirectResponse(url="/")
    
    async for session in get_db():
        payment_repo = PaymentRepository(session)
        user_repo = UserRepository(session)
        query_repo = QueryRepository(session)
        
        total_users = await user_repo.count()
        premium_users = await user_repo.count(is_premium=True)
        global_stats = await query_repo.get_global_stats()
        payment_stats = await PaymentService(session).get_payment_stats()
        pending = await PaymentService(session).get_pending_payments()
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "stats": {
                "total_users": total_users,
                "premium_users": premium_users,
                "total_searches": global_stats['total_searches'],
                "total_found": global_stats['total_found'],
                "pending_payments": payment_stats['pending']
            },
            "pending_payments": pending
        })

@app.post("/admin/approve/{payment_id}")
async def approve_payment(request: Request, payment_id: int):
    admin_id = request.cookies.get("admin_id")
    if not admin_id or not is_admin(int(admin_id)):
        return {"error": "Unauthorized"}
    
    async for session in get_db():
        payment_service = PaymentService(session)
        result = await payment_service.approve_payment(payment_id, int(admin_id))
        return result

@app.post("/admin/reject/{payment_id}")
async def reject_payment(request: Request, payment_id: int, reason: str = Form(...)):
    admin_id = request.cookies.get("admin_id")
    if not admin_id or not is_admin(int(admin_id)):
        return {"error": "Unauthorized"}
    
    async for session in get_db():
        payment_service = PaymentService(session)
        result = await payment_service.reject_payment(payment_id, int(admin_id), reason)
        return result
