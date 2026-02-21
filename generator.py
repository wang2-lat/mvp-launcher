from pathlib import Path
from jinja2 import Template
from rich.console import Console

console = Console()

class ProjectGenerator:
    def __init__(self, name, template):
        self.name = name
        self.template = template
        self.project_path = Path(name)
    
    def create_project(self):
        self.project_path.mkdir(parents=True)
        
        if self.template == "saas-basic":
            self._create_full_saas()
        elif self.template == "api-only":
            self._create_api_only()
        elif self.template == "landing-only":
            self._create_landing_only()
        
        self._create_deployment_files()
        console.print(f"[green]✓ Generated {self.template} template[/green]")
    
    def _create_full_saas(self):
        # Frontend
        frontend_dir = self.project_path / "frontend"
        frontend_dir.mkdir()
        
        (frontend_dir / "index.html").write_text(self._get_landing_template())
        (frontend_dir / "styles.css").write_text(self._get_styles_template())
        (frontend_dir / "app.js").write_text(self._get_frontend_js_template())
        
        # Backend
        backend_dir = self.project_path / "backend"
        backend_dir.mkdir()
        
        (backend_dir / "main.py").write_text(self._get_api_template())
        (backend_dir / "auth.py").write_text(self._get_auth_template())
        (backend_dir / "payments.py").write_text(self._get_payments_template())
        (backend_dir / "requirements.txt").write_text("fastapi>=0.104.0\nuvicorn>=0.24.0\nstripe>=7.0.0\npyjwt>=2.8.0\nsqlalchemy>=2.0.0")
    
    def _create_api_only(self):
        backend_dir = self.project_path / "backend"
        backend_dir.mkdir()
        
        (backend_dir / "main.py").write_text(self._get_api_template())
        (backend_dir / "auth.py").write_text(self._get_auth_template())
        (backend_dir / "requirements.txt").write_text("fastapi>=0.104.0\nuvicorn>=0.24.0\npyjwt>=2.8.0\nsqlalchemy>=2.0.0")
    
    def _create_landing_only(self):
        frontend_dir = self.project_path / "frontend"
        frontend_dir.mkdir()
        
        (frontend_dir / "index.html").write_text(self._get_landing_template())
        (frontend_dir / "styles.css").write_text(self._get_styles_template())
        (frontend_dir / "app.js").write_text(self._get_frontend_js_template())
    
    def _create_deployment_files(self):
        (self.project_path / "vercel.json").write_text('{"version": 2, "builds": [{"src": "backend/main.py", "use": "@vercel/python"}]}')
        (self.project_path / "railway.json").write_text('{"build": {"builder": "NIXPACKS"}, "deploy": {"startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"}}')
        (self.project_path / "render.yaml").write_text('services:\n  - type: web\n    name: api\n    env: python\n    buildCommand: pip install -r backend/requirements.txt\n    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT')
    
    def _get_landing_template(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your SaaS Product</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Launch Your Product Fast</h1>
        <p>Start earning passive income today</p>
    </header>
    <main>
        <section class="pricing">
            <div class="plan">
                <h2>Starter</h2>
                <p class="price">$29/month</p>
                <button onclick="subscribe('starter')">Get Started</button>
            </div>
            <div class="plan featured">
                <h2>Pro</h2>
                <p class="price">$99/month</p>
                <button onclick="subscribe('pro')">Get Started</button>
            </div>
        </section>
        <section class="auth">
            <input type="email" id="email" placeholder="Email">
            <input type="password" id="password" placeholder="Password">
            <button onclick="login()">Login</button>
            <button onclick="signup()">Sign Up</button>
        </section>
    </main>
    <script src="app.js"></script>
</body>
</html>'''
    
    def _get_styles_template(self):
        return '''* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: #f5f5f5; }
header { text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
header h1 { font-size: 48px; margin-bottom: 20px; }
.pricing { display: flex; justify-content: center; gap: 30px; padding: 60px 20px; }
.plan { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
.plan.featured { transform: scale(1.05); border: 3px solid #667eea; }
.price { font-size: 36px; font-weight: bold; margin: 20px 0; color: #667eea; }
button { background: #667eea; color: white; border: none; padding: 15px 30px; border-radius: 5px; cursor: pointer; font-size: 16px; }
button:hover { background: #5568d3; }
.auth { text-align: center; padding: 40px; }
.auth input { display: block; margin: 10px auto; padding: 12px; width: 300px; border: 1px solid #ddd; border-radius: 5px; }'''
    
    def _get_frontend_js_template(self):
        return '''const API_URL = '/api';

async function subscribe(plan) {
    const response = await fetch(`${API_URL}/create-checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan })
    });
    const data = await response.json();
    window.location.href = data.url;
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    if (data.token) {
        localStorage.setItem('token', data.token);
        alert('Login successful!');
    }
}

async function signup() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const response = await fetch(`${API_URL}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    alert(data.message);
}'''
    
    def _get_api_template(self):
        return '''from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auth import create_token, verify_token, hash_password, verify_password
from payments import create_checkout_session
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}

class User(BaseModel):
    email: str
    password: str

class Plan(BaseModel):
    plan: str

@app.post("/api/signup")
async def signup(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.email] = hash_password(user.password)
    return {"message": "User created successfully"}

@app.post("/api/login")
async def login(user: User):
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(user.password, users_db[user.email]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.email)
    return {"token": token}

@app.post("/api/create-checkout")
async def create_checkout(plan: Plan):
    prices = {"starter": 2900, "pro": 9900}
    session = create_checkout_session(prices.get(plan.plan, 2900))
    return {"url": session["url"]}

@app.get("/api/health")
async def health():
    return {"status": "ok"}'''
    
    def _get_auth_template(self):
        return '''import jwt
import hashlib
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-change-this"

def create_token(email: str) -> str:
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed'''
    
    def _get_payments_template(self):
        return '''import stripe
import os

stripe.api_key = os.getenv("STRIPE_KEY", "sk_test_...")

def create_checkout_session(amount: int):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Subscription"},
                    "unit_amount": amount,
                    "recurring": {"interval": "month"}
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url="https://yourdomain.com/success",
            cancel_url="https://yourdomain.com/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        return {"url": "#", "error": str(e)}'''
