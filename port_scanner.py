import socket         
import argparse        
import sys             
import time           


def validate_host(host: str) -> str:
    allowed_hosts = {"127.0.0.1", "localhost", "scanme.nmap.org"}
    if host not in allowed_hosts:
        raise argparse.ArgumentTypeError(
            "Host must be 127.0.0.1, localhost, or scanme.nmap.org"
        )
    return host


def parse_ports(ports: str) -> list[int]:
    try:
        if "-" in ports:
            start, end = [int(p) for p in ports.split("-")]
            if start > end or start < 1 or end > 65535:
                raise ValueError
            return list(range(start, end + 1))
        else:
            p = int(ports)
            if not 1 <= p <= 65535:
                raise ValueError
            return [p]
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Port(s) must be 1-65535 or range format e.g. 20-80"
        )


def scan(host: str, ports: list[int], delay: float) -> None:
    open_ports: list[int] = []

    print(f"\n[*] Scanning {host} on ports: {ports}\n")

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)  # Short timeout keeps scan quick
            result = sock.connect_ex((host, port))

            if result == 0:
                print(f"[OPEN ] Port {port:>5}")
                open_ports.append(port)
            else:
                print(f"[CLOSED] Port {port:>5}")

        time.sleep(delay)  # Respectful delay (rate-limit friendly)


    print("\n──── Scan Complete ────")
    if open_ports:
        print(f"[+] Open ports: {open_ports}")
    else:
        print("[-] No open ports found.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simple TCP Port Scanner (CYB333 Midterm)"
    )
    parser.add_argument(
        "host",
        type=validate_host,
        help="Target host (127.0.0.1 | localhost | scanme.nmap.org)",
    )
    parser.add_argument(
        "ports",
        type=parse_ports,
        help="Port or range (e.g. 80  or  20-100)",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0.2,
        help="Delay between probes in seconds (default 0.2)",
    )
    args = parser.parse_args()

    try:
        scan(args.host, args.ports, args.delay)
    except socket.gaierror:
        print("[!] Host unreachable / DNS failure.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()