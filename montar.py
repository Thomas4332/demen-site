"""Monta o site: fonte.html + contas.py -> index.html (principal) e teste/index.html (com efeitos).
Uso: python3 montar.py"""
import os, pathlib, subprocess, sys
RAIZ = pathlib.Path(__file__).parent
s = (RAIZ / "fonte.html").read_text(encoding="utf-8")
def troca(a, b, n=1):
    global s
    if a not in s:
        raise SystemExit(f"Âncora não encontrada: {a[:80]!r}")
    s = s.replace(a, b, n)
PREFIXO = ""
if not os.environ.get("SEM_CONTAS"):  # SEM_CONTAS=1 publica sem contas/SAC/avaliações
    exec((RAIZ / "contas.py").read_text(encoding="utf-8"))
(RAIZ / "index.html").write_text(s, encoding="utf-8")
print("index.html ok", len(s))
subprocess.run([sys.executable, str(RAIZ / "gerar_teste.py")], check=True)
