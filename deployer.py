import subprocess
from pathlib import Path
from rich.console import Console
import json

console = Console()

class Deployer:
    def __init__(self, platform):
        self.platform = platform
    
    def deploy(self):
        if self.platform == "vercel":
            return self._deploy_vercel()
        elif self.platform == "railway":
            return self._deploy_railway()
        elif self.platform == "render":
            return self._deploy_render()
        else:
            return {"success": False, "error": "Unknown platform"}
    
    def _deploy_vercel(self):
        console.print("[blue]Deploying to Vercel...[/blue]")
        console.print("Install Vercel CLI: npm i -g vercel")
        console.print("Run: vercel --prod")
        return {
            "success": True,
            "url": "https://your-project.vercel.app",
            "note": "Run 'vercel --prod' to complete deployment"
        }
    
    def _deploy_railway(self):
        console.print("[blue]Deploying to Railway...[/blue]")
        console.print("Install Railway CLI: npm i -g @railway/cli")
        console.print("Run: railway up")
        return {
            "success": True,
            "url": "https://your-project.railway.app",
            "note": "Run 'railway up' to complete deployment"
        }
    
    def _deploy_render(self):
        console.print("[blue]Deploying to Render...[/blue]")
        console.print("Connect your GitHub repo at https://render.com")
        return {
            "success": True,
            "url": "https://your-project.onrender.com",
            "note": "Connect GitHub repo at render.com to complete deployment"
        }
