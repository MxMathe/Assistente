"""Localiza e abre programas instalados no Windows."""

import glob
import json
import os
import subprocess

from Config import ALIASES
from Texto import limpar_inicio
from Voz import falar

# Cache dos programas instalados (preenchido na primeira vez que for preciso)
_cache_programas = None


def listar_apps_windows():
    """Aplicativos do Windows (inclui Microsoft Store) via PowerShell."""
    try:
        resultado = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-StartApps | ConvertTo-Json -Compress"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=20,
        )

        if resultado.returncode != 0 or not resultado.stdout.strip():
            return []

        apps = json.loads(resultado.stdout)

        # Com um único app, o PowerShell devolve um objeto em vez de lista
        return [apps] if isinstance(apps, dict) else apps

    except Exception as erro:
        print(f"Erro ao pesquisar aplicativos do Windows: {erro}")
        return []


def listar_atalhos():
    """Atalhos (.lnk) do Menu Iniciar."""
    locais = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"),
    ]

    atalhos = []
    for local in locais:
        if os.path.exists(local):
            atalhos.extend(
                glob.glob(os.path.join(local, "**", "*.lnk"), recursive=True)
            )

    return atalhos


def carregar_programas():
    """Monta (uma única vez) o dicionário nome -> como abrir."""
    global _cache_programas

    if _cache_programas is not None:
        return _cache_programas

    programas = {}

    for app in listar_apps_windows():
        nome = app.get("Name", "").lower().strip()
        if nome:
            programas[nome] = {"tipo": "windows_app", "app_id": app.get("AppID")}

    # setdefault: se já existe como app do Windows, o atalho não sobrescreve
    for atalho in listar_atalhos():
        nome = os.path.splitext(os.path.basename(atalho))[0].lower().strip()
        programas.setdefault(nome, {"tipo": "atalho", "caminho": atalho})

    _cache_programas = programas
    return programas


def encontrar_programa(nome):
    """Busca exata primeiro; depois parcial, preferindo o nome mais curto."""
    nome = ALIASES.get(nome, nome)
    programas = carregar_programas()

    if nome in programas:
        return nome, programas[nome]

    candidatos = [n for n in programas if nome in n]
    if candidatos:
        melhor = min(candidatos, key=len)
        return melhor, programas[melhor]

    return None, None


def abrir_programa(nome_falado):
    nome_falado = limpar_inicio(nome_falado)
    nome, programa = encontrar_programa(nome_falado)

    if not programa:
        falar(f"Não encontrei o programa {nome_falado}.")
        return

    try:
        if programa["tipo"] == "windows_app":
            subprocess.Popen(
                ["explorer.exe", f"shell:AppsFolder\\{programa['app_id']}"]
            )
        else:
            os.startfile(programa["caminho"])

        falar(f"Abrindo {nome}")

    except Exception as erro:
        print(f"Erro ao abrir programa: {erro}")
        falar(f"Não consegui abrir o {nome}.")