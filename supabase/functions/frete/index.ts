// Cotação de frete pelo CEP para a sacola do site (Melhor Envio).
// Segredos: MELHORENVIO_TOKEN (obrigatório para cotar), MELHORENVIO_EMAIL, FRETE_CEP_ORIGEM (padrão 56600000),
// MELHORENVIO_URL (use https://sandbox.melhorenvio.com.br para testar).
import { cors, cotar, dados, json, soDigitos, validarItens } from "./envio.ts";

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors(req) });
  if (req.method !== "POST") return json(req, { erro: "use POST" }, 405);
  try {
    const b = await req.json();
    const cep = soDigitos(b.cep);
    if (cep.length !== 8) return json(req, { erro: "CEP inválido" }, 400);
    const d = await dados();
    const itens = validarItens(d, b.itens);
    const r = await cotar(d, cep, itens);
    return json(req, r);
  } catch (e) {
    const m = String((e as Error).message || e);
    console.error("frete", m);
    return json(req, { erro: m.startsWith("Melhor Envio") ? "Não foi possível calcular agora" : m }, m.startsWith("Melhor Envio") ? 502 : 400);
  }
});
