#!/usr/bin/env python3
# KuudereFetch for KuudereOS
# Берёт информацию из системы, как neofetch

import subprocess
import os
import platform

# Цвета
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[38;5;75m"
LIGHT_BLUE = "\033[38;5;117m"
WHITE = "\033[38;5;255m"
GRAY = "\033[38;5;245m"
DARK = "\033[38;5;238m"

LOGO = f"""{LIGHT_BLUE}
       ██╗  ██╗██╗   ██╗██╗   ██╗
       ██║ ██╔╝██║   ██║██║   ██║
       █████╔╝ ██║   ██║██║   ██║
       ██╔═██╗ ██║   ██║██║   ██║
       ██║  ██╗╚██████╔╝╚██████╔╝
       ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ 
{RESET}{BLUE}            KuudereOS{RESET}
"""

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except:
        return "?"

def get_info():
    info = []
    
    user = os.getenv("USER", "?")
    host = platform.node()
    info.append(f"{BLUE}{BOLD}{user}{RESET}@{BLUE}{BOLD}{host}{RESET}")
    info.append(f"{GRAY}{'─' * 30}{RESET}")
    
    # OS — читаем из /etc/os-release
    os_name = "KuudereOS"
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    os_name = line.split("=")[1].strip().strip('"')
                    break
    info.append(f"{BLUE}OS:{RESET} {WHITE}{os_name}{RESET}")
    
    # Kernel
    kernel = platform.release()
    info.append(f"{BLUE}Kernel:{RESET} {WHITE}{kernel}{RESET}")
    
    # Uptime
    uptime = run("uptime -p").replace("up ", "")
    if uptime:
        info.append(f"{BLUE}Uptime:{RESET} {WHITE}{uptime}{RESET}")
    
    # CPU
    cpu = run("grep -m1 'model name' /proc/cpuinfo | cut -d: -f2").strip()
    if cpu:
        info.append(f"{BLUE}CPU:{RESET} {WHITE}{cpu}{RESET}")
    
    # Resolution
    resolution = run("xrandr | grep '*' | head -1 | awk '{print $1}'")
    if resolution:
        info.append(f"{BLUE}Resolution:{RESET} {WHITE}{resolution}{RESET}")
    
    # Memory
    mem = run("LC_ALL=C free -h | awk '/^Mem:/ {print $3 \" / \" $2}'")
    info.append(f"{BLUE}Memory:{RESET} {WHITE}{mem}{RESET}")
    
    # Disk
    disk = run("df -h / | awk 'NR==2 {print $3 \" / \" $2}'")
    info.append(f"{BLUE}Disk:{RESET} {WHITE}{disk}{RESET}")
    
    # Packages
    packages = run("dpkg --list | wc -l")
    if packages and packages != "?":
        info.append(f"{BLUE}Packages:{RESET} {WHITE}{packages}{RESET}")
    
    # DE
    de = os.getenv("XDG_CURRENT_DESKTOP", "?")
    info.append(f"{BLUE}DE:{RESET} {WHITE}{de}{RESET}")
    
    # Theme
    theme = run("gsettings get org.cinnamon.theme name").strip("'")
    if theme and theme != "?":
        info.append(f"{BLUE}Theme:{RESET} {WHITE}{theme}{RESET}")
    
    # Shell
    shell = os.getenv("SHELL", "?").split("/")[-1]
    info.append(f"{BLUE}Shell:{RESET} {WHITE}{shell}{RESET}")
    
    # Terminal
    term = os.getenv("TERM", "?")
    info.append(f"{BLUE}Terminal:{RESET} {WHITE}{term}{RESET}")
    
    # Color blocks
    palette = (f"{DARK}███{RESET} {BLUE}███{RESET} {LIGHT_BLUE}███{RESET} "
               f"{WHITE}███{RESET} {GRAY}███{RESET}")
    info.append("")
    info.append(palette)
    
    return info

def main():
    info = get_info()
    logo_lines = LOGO.split("\n")
    
    max_lines = max(len(logo_lines), len(info))
    for i in range(max_lines):
        left = logo_lines[i] if i < len(logo_lines) else " " * 40
        right = info[i] if i < len(info) else ""
        print(f"{left}  {right}")

if __name__ == "__main__":
    main()
