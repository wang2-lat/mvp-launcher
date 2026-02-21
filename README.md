# MVP Launcher

Launch your SaaS MVP in minutes without coding.

## Installation


## Usage

### 1. Create a new project


Available templates:
- `saas-basic` - Full SaaS with landing page, API, auth, and payments
- `api-only` - Backend API with database and authentication
- `landing-only` - Landing page with payment integration

### 2. Configure API keys


Enter your Stripe API key and JWT secret when prompted.

### 3. Deploy to cloud


Supported platforms:
- `vercel` - Free tier with automatic HTTPS
- `railway` - Free tier with database included
- `render` - Free tier with auto-deploy from Git

## Commands

- `init <name>` - Create new project
- `config` - Configure API keys
- `deploy` - Deploy to cloud platform
- `templates` - List available templates

## Example


## Features

- Landing page with pricing plans
- User authentication (signup/login)
- Stripe payment integration
- One-click deployment
- No coding required

## Requirements

- Python 3.8+
- Stripe account (for payments)
- Vercel/Railway/Render account (for deployment)
pip install -r requirements.txt
python main.py init my-startup
cd my-startup
python ../main.py config  # 输入 Stripe key
python ../main.py deploy --platform vercel