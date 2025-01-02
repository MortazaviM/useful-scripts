import requests
import argparse
import socket
from rich.console import Console

console = Console()

def fetch_data(ip):
    url = f"https://internetdb.shodan.io/{ip}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            console.print(f"[bold red][!] Error fetching data: {response.status_code}[/bold red]")
            exit(1)
    except requests.RequestException as e:
        console.print(f"[bold red][!] Request failed: {e}[/bold red]")
        exit(1)
        
def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        console.print(f"[bold red][!] Unable to resolve domain: {domain}[/bold red]") 
        exit(1)
        
def main():
    parser = argparse.ArgumentParser(description="Ultimate Cves Hunting Tool")
    parser.add_argument("-d", "--domain", help="IP address or domain to scan")
    parser.add_argument("-o", "--output", help="Output file to store the results (e.g., result.txt)", type=str)
    args = parser.parse_args()

    if args.output:
        output_file = open(args.output, "w", encoding="utf-8")
        banner(output_file)
    else:
        output_file = None
        banner()

    if not args.domain:
        input_data = sys.stdin.read().strip()  # Read the piped input
        if not input_data:
            console.print("[bold red][!] No input provided via pipe or argument.[/bold red]")
            exit(1)
        target = input_data
    else:
        target = args.domain

    if not target.replace(".", "").isdigit():
        console.print(f"[bold yellow][+] Resolving domain {target} to IP...[/bold yellow]")
        target = resolve_domain(target)
        console.print(f"[bold green][+] Resolved IP: {target}[/bold green]")

    console.print(f"[bold cyan][+] Fetching data for IP: {target}...[/bold cyan]")
    data = fetch_data(target)

    #display_hostnames(data.get("hostnames", []), output_file)
    #display_ports(data.get("ports", []), output_file)
    #display_cves(data.get("vulns", []), output_file)

    #if output_file:
    #    output_file.close()

if __name__ == "__main__":
    main()