import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from pathlib import Path
import json
from generator import ProjectGenerator
from deployer import Deployer

app = typer.Typer(help="Launch your SaaS MVP in minutes without coding")
console = Console()

@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Option("saas-basic", help="Template type: saas-basic, api-only, landing-only")
):
    """Initialize a new SaaS project from template"""
    console.print(f"[bold green]Creating project: {name}[/bold green]")
    
    project_path = Path(name)
    if project_path.exists():
        console.print(f"[red]Error: Directory {name} already exists[/red]")
        raise typer.Exit(1)
    
    generator = ProjectGenerator(name, template)
    generator.create_project()
    
    console.print(f"\n[bold green]✓ Project created successfully![/bold green]")
    console.print(f"\nNext steps:")
    console.print(f"  cd {name}")
    console.print(f"  mvp-launcher config")
    console.print(f"  mvp-launcher deploy")

@app.command()
def config(
    stripe_key: str = typer.Option(None, help="Stripe API key"),
    auth_secret: str = typer.Option(None, help="JWT secret for authentication")
):
    """Configure API keys and secrets"""
    config_file = Path(".mvp-config.json")
    config_data = {}
    
    if config_file.exists():
        with open(config_file) as f:
            config_data = json.load(f)
    
    if not stripe_key:
        stripe_key = Prompt.ask("Enter Stripe API key (or press Enter to skip)", default="")
    if not auth_secret:
        auth_secret = Prompt.ask("Enter JWT secret (or press Enter to generate)", default="")
    
    if stripe_key:
        config_data["stripe_key"] = stripe_key
    if auth_secret:
        config_data["auth_secret"] = auth_secret
    else:
        import secrets
        config_data["auth_secret"] = secrets.token_urlsafe(32)
    
    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=2)
    
    console.print("[bold green]✓ Configuration saved[/bold green]")

@app.command()
def deploy(
    platform: str = typer.Option("vercel", help="Platform: vercel, railway, render"),
    auto_confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Deploy project to cloud platform"""
    config_file = Path(".mvp-config.json")
    if not config_file.exists():
        console.print("[yellow]Warning: No configuration found. Run 'mvp-launcher config' first[/yellow]")
        if not Confirm.ask("Continue anyway?"):
            raise typer.Exit(0)
    
    if not auto_confirm:
        if not Confirm.ask(f"Deploy to {platform}?"):
            raise typer.Exit(0)
    
    console.print(f"[bold blue]Deploying to {platform}...[/bold blue]")
    
    deployer = Deployer(platform)
    result = deployer.deploy()
    
    if result["success"]:
        console.print(f"\n[bold green]✓ Deployment successful![/bold green]")
        console.print(f"URL: {result['url']}")
    else:
        console.print(f"[red]Deployment failed: {result['error']}[/red]")
        raise typer.Exit(1)

@app.command()
def templates():
    """List available project templates"""
    templates_list = [
        ("saas-basic", "Full SaaS with landing page, API, auth, and payments"),
        ("api-only", "Backend API with database and authentication"),
        ("landing-only", "Landing page with payment integration")
    ]
    
    console.print("[bold]Available Templates:[/bold]\n")
    for name, desc in templates_list:
        console.print(f"  [cyan]{name}[/cyan]: {desc}")

if __name__ == "__main__":
    app()
