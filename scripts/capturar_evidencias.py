#!/usr/bin/env python3
"""Verifique o HTML por HTTP local e capture telas reais, depois de cortar a rede."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    payload = json.loads((ROOT / "data/vendas-sanitizadas.json").read_text())
    rows = [r for r in payload["vendas"] if r["status_entrega"] != "Cancelled"]
    destination = ROOT / "docs/img"
    destination.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"))
            context = browser.new_context(viewport={"width": 1440, "height": 1100}, device_scale_factor=1)
            page = context.new_page()
            errors, external = [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
            page.on("request", lambda request: external.append(request.url)
                    if request.url.startswith(("https://", "http://")) and not request.url.startswith("http://127.0.0.1:") else None)
            response = page.goto(f"http://127.0.0.1:{server.server_port}/index.html")
            assert response.status == 200, "O servidor local não entregou o HTML."
            assert response.body() == (ROOT / "index.html").read_bytes(), "A resposta não corresponde ao arquivo entregue."
            context.set_offline(True)
            initial = page.evaluate("PorscheDashboard.getSummary()")
            assert initial["count"] == len(rows)
            assert initial["totalCents"] == sum(r["preco_centavos"] for r in rows if r["preco_centavos"] is not None)
            page.screenshot(path=str(destination / "visao-geral.png"), full_page=True)
            page.select_option("#filter-estado", "CA")
            california = [r for r in rows if r["estado"] == "CA"]
            selected = page.evaluate("PorscheDashboard.getSummary()")
            assert selected["count"] == len(california)
            assert selected["totalCents"] == sum(r["preco_centavos"] for r in california if r["preco_centavos"] is not None)
            page.screenshot(path=str(destination / "filtro-aplicado.png"), full_page=True)
            page.locator("#clear-filters").click()
            page.set_viewport_size({"width": 360, "height": 900})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Rolagem horizontal no documento móvel."
            page.screenshot(path=str(destination / "mobile.png"), full_page=True)
            assert not errors, errors
            assert not external, external
            print(json.dumps({"http": 200, "html_identico": True, "rede_desativada_apos_carga": True,
                              "inicial": initial, "filtro_CA": selected, "erros_js_console": errors,
                              "requisicoes_externas": external, "chromium": browser.version,
                              "capturas": ["visao-geral.png", "filtro-aplicado.png", "mobile.png"]}, ensure_ascii=False, indent=2))
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)


if __name__ == "__main__":
    main()
