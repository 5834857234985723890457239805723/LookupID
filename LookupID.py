import requests
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

console = Console()

API_URL = 'https://discordlookup.mesalytic.moe/v1/user/'

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_user_info(user_id):
    try:
        response = requests.get(API_URL + str(user_id))
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as ex:
        console.print(f'[red]Error: {ex}[/red]')
        return None

def format_user_info(data):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Field", style="dim", width=20)
    table.add_column("Value")

    def add_rows(data, parent_key=""):
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{parent_key}.{key}" if parent_key else key
                add_rows(value, new_key)
        elif isinstance(data, list):
            table.add_row(parent_key, ", ".join(str(v) for v in data))
        else:
            table.add_row(parent_key, str(data))
    
    add_rows(data)
    return table

def main():
    clear()
    console.print(Panel.fit(Text.from_markup("[bold purple]Discord id lookup by Ես գալիս եմ Կավկազից [/bold purple]"), title="Bienvenue", subtitle="Entrez l'id discord", border_style="purple"))

    try:
        user_id = int(console.input("[bold cyan]Entrez l'id discord: [/bold cyan]"))
    except ValueError:
        console.print("[red]ID discord invalide choississez un numéro.[/red]")
        return
    
    user_info = get_user_info(user_id)
    if user_info:
        table = format_user_info(user_info)
        console.print(table)
        input("Appuyez sur entrée pour quitter")
    else:
        console.print("[red]Impossible de récupérer les informations de l'utilisateur.[/red]")

if __name__ == '__main__':
    main()
