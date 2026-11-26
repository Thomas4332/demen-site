// Partes comuns de frete e pagamento da DE men (copiado nas funções "frete" e "pagamento").
// Os preços SEMPRE saem do produtos.json publicado no site, nunca do navegador do cliente.

export type Prod = { id: string; nome: string; marca: string; cat: string; sub: string; preco: string; tam: string[]; foto: string; esgotados?: string[]; semEstoque?: boolean };
export type Dados = { loja: any; produtos: Prod[] };
export type Opcao = { id: string; nome: string; empresa: string; preco: number; prazo: number | null };

const env = (k: string) => Deno.env.get(k) ?? "";
export const SITE = env("SITE_URL") || "https://demen-loja.github.io/";
const ORIGENS = [SITE.replace(/\/$/, ""), "http://127.0.0.1:8800", "http://localhost:8800"];

export function cors(req: Request) {
  const o = req.headers.get("origin") || "";
  return {
    "Access-Control-Allow-Origin": ORIGENS.includes(o) ? o : ORIGENS[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, apikey, authorization, x-client-info",
    "Vary": "Origin",
  };
}
export const json = (req: Request, corpo: unknown, status = 200) =>
  new Response(JSON.stringify(corpo), { status, headers: { ...cors(req), "Content-Type": "application/json" } });

let cache: { em: number; d: Dados } | null = null;
export async function dados(): Promise<Dados> {
  if (cache && Date.now() - cache.em < 5 * 60_000) return cache.d;
  const r = await fetch(SITE + "produtos.json?t=" + Date.now());
  if (!r.ok) { if (cache) return cache.d; throw new Error("produtos.json " + r.status); }
  cache = { em: Date.now(), d: await r.json() };
  return cache.d;
}

export const precoNum = (t: string) => {
  const m = String(t || "").match(/(\d{1,3}(?:\.\d{3})*|\d+),(\d{2})/);
  return m ? Number(m[1].replace(/\./g, "") + "." + m[2]) : null;
};
export const soDigitos = (s: string) => String(s || "").replace(/\D/g, "");

// Medidas da embalagem por categoria (cm e kg). Ajuste conforme as caixas da loja.
const CAIXAS: Record<string, [number, number, number, number]> = {
  "Calçados": [33, 22, 13, 1.1], "Sandálias": [30, 20, 10, 0.6], "Casacos": [32, 26, 8, 0.9], "Calças": [30, 25, 6, 0.7],
  "Bermudas": [28, 22, 5, 0.45], "Camisas": [28, 22, 4, 0.35], "Cuecas": [20, 15, 5, 0.25], "Acessórios": [22, 16, 8, 0.35],
};
const caixa = (cat: string) => CAIXAS[cat] || [25, 20, 6, 0.5];

export type Item = { id: string; tam?: string; qtd: number };

export function validarItens(d: Dados, itens: Item[]) {
  if (!Array.isArray(itens) || !itens.length || itens.length > 30) throw new Error("itens inválidos");
  return itens.map((i) => {
    const p = d.produtos.find((x) => x.id === String(i.id));
    const qtd = Math.floor(Number(i.qtd));
    if (!p) throw new Error("produto não encontrado: " + i.id);
    if (!(qtd >= 1 && qtd <= 10)) throw new Error("quantidade inválida");
    const tam = String(i.tam || "");
    if (tam && !p.tam.includes(tam)) throw new Error("tamanho inválido: " + p.nome);
    if (p.semEstoque || (tam && (p.esgotados || []).includes(tam))) throw new Error("esgotado: " + p.nome + (tam ? " " + tam : ""));
    return { p, tam, qtd, preco: precoNum(p.preco) };
  });
}

export async function cotar(d: Dados, cep: string, itens: ReturnType<typeof validarItens>): Promise<{ configurado: boolean; opcoes: Opcao[] }> {
  const token = env("MELHORENVIO_TOKEN");
  if (!token) return { configurado: false, opcoes: [] };
  const base = env("MELHORENVIO_URL") || "https://melhorenvio.com.br";
  const corpo = {
    from: { postal_code: soDigitos(env("FRETE_CEP_ORIGEM") || "56600000") },
    to: { postal_code: cep },
    products: itens.map(({ p, qtd, preco }, n) => {
      const [w, l, h, kg] = caixa(p.cat);
      return { id: String(n + 1), width: w, length: l, height: h, weight: kg, insurance_value: preco ?? 0, quantity: qtd };
    }),
    options: { receipt: false, own_hand: false },
  };
  const r = await fetch(base + "/api/v2/me/shipment/calculate", {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json", Authorization: "Bearer " + token, "User-Agent": "DE men site (" + (env("MELHORENVIO_EMAIL") || "contato@demen") + ")" },
    body: JSON.stringify(corpo),
  });
  if (!r.ok) throw new Error("Melhor Envio " + r.status + " " + (await r.text()).slice(0, 200));
  const lista = await r.json();
  const opcoes: Opcao[] = (Array.isArray(lista) ? lista : []).filter((o: any) => !o.error && (o.custom_price ?? o.price))
    .map((o: any) => ({
      id: String(o.id), nome: `${o.company?.name || ""} ${o.name || ""}`.trim(), empresa: o.company?.name || "",
      preco: Math.round(Number(o.custom_price ?? o.price) * 100) / 100,
      prazo: Number(o.custom_delivery_time ?? o.delivery_time) || null,
    }))
    .filter((o: Opcao) => o.preco > 0)
    .sort((a: Opcao, b: Opcao) => a.preco - b.preco)
    .slice(0, 6);
  return { configurado: true, opcoes };
}
