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
subprocess.run(["node", str(RAIZ / "dados_bot.js")], check=True)  # lista de produtos para o robô do WhatsApp
subprocess.run([sys.executable, str(RAIZ / "seo.py")], check=True)  # SEO: webp, páginas de produto, sitemap, robots (LIBERAR_GOOGLE=1 libera)
