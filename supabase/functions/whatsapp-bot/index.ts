// Robô de WhatsApp da DE men (Supabase Edge Function + API oficial do WhatsApp da Meta).
// Segredos (Supabase > Edge Functions > Secrets):
//   WHATSAPP_TOKEN         token de acesso permanente da Meta
//   WHATSAPP_PHONE_ID      ID do número no WhatsApp Manager
//   WHATSAPP_VERIFY_TOKEN  palavra combinada para a Meta validar o webhook
//   WHATSAPP_APP_SECRET    chave secreta do app da Meta (confere a assinatura das mensagens)
//   ANTHROPIC_API_KEY      (opcional) liga as respostas com IA
//   IA_LIMITE_DIA          (opcional) respostas de IA por cliente por dia. Padrão 20
import { createClient } from "npm:@supabase/supabase-js@2";
import { menu, responder, type Dados, type Saida } from "./bot.ts";

const env = (k: string) => Deno.env.get(k) ?? "";
const GRAPH = "https://graph.facebook.com/v23.0";
const DADOS_URL = env("DADOS_URL") || "https://demen-loja.github.io/produtos.json";
const sb = createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });

let cache: { em: number; dados: Dados } | null = null;
async function dados(): Promise<Dados> {
  if (cache && Date.now() - cache.em < 5 * 60_000) return cache.dados;
  const r = await fetch(DADOS_URL + "?t=" + Date.now());
  if (!r.ok) { if (cache) return cache.dados; throw new Error("produtos.json " + r.status); }
  cache = { em: Date.now(), dados: await r.json() };
  return cache.dados;
}

async function assinaturaValida(corpo: string, cab: string | null) {
  const segredo = env("WHATSAPP_APP_SECRET");
  if (!segredo) return false;
  if (!cab?.startsWith("sha256=")) return false;
  const chave = await crypto.subtle.importKey("raw", new TextEncoder().encode(segredo), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = new Uint8Array(await crypto.subtle.sign("HMAC", chave, new TextEncoder().encode(corpo)));
  const hex = [...sig].map((b) => b.toString(16).padStart(2, "0")).join("");
  const rec = cab.slice(7);
  if (rec.length !== hex.length) return false;
  let dif = 0; for (let i = 0; i < hex.length; i++) dif |= hex.charCodeAt(i) ^ rec.charCodeAt(i);
  return dif === 0;
}

async function graph(corpo: unknown) {
  const r = await fetch(`${GRAPH}/${env("WHATSAPP_PHONE_ID")}/messages`, {
    method: "POST", headers: { Authorization: `Bearer ${env("WHATSAPP_TOKEN")}`, "Content-Type": "application/json" }, body: JSON.stringify(corpo),
  });
  if (!r.ok) console.error("Graph", r.status, await r.text());
  return r.ok;
}

function payload(para: string, s: Saida) {
  const base = { messaging_product: "whatsapp", recipient_type: "individual", to: para };
  if (s.tipo === "texto") return { ...base, type: "text", text: { body: s.texto, preview_url: true } };
  if (s.tipo === "imagem") return { ...base, type: "image", image: { link: s.url, caption: s.legenda } };
  if (s.tipo === "botoes") return { ...base, type: "interactive", interactive: { type: "button", ...(s.imagem ? { header: { type: "image", image: { link: s.imagem } } } : {}), body: { text: s.corpo.slice(0, 1024) },
    action: { buttons: s.botoes.slice(0, 3).map((b) => ({ type: "reply", reply: { id: b.id.slice(0, 256), title: b.titulo.slice(0, 20) } })) } } };
  return { ...base, type: "interactive", interactive: { type: "list", body: { text: s.corpo.slice(0, 1024) },
    action: { button: s.botao.slice(0, 20), sections: s.secoes.map((sec) => ({ title: sec.titulo.slice(0, 24),
      rows: sec.linhas.map((l) => ({ id: l.id.slice(0, 200), title: l.titulo.slice(0, 24), ...(l.desc ? { description: l.desc.slice(0, 72) } : {}) })) })) } } };
}
const textoDe = (s: Saida) => s.tipo === "texto" ? s.texto : s.tipo === "imagem" ? s.legenda : s.corpo;

async function ia(sistema: string, mensagens: { role: "user" | "assistant"; content: string }[]) {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": env("ANTHROPIC_API_KEY"), "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: env("IA_MODELO") || "claude-haiku-5-5", max_tokens: 400, system: sistema, messages: mensagens }),
  });
  if (!r.ok) throw new Error("IA " + r.status + " " + (await r.text()).slice(0, 200));
  const j = await r.json();
  return (j.content || []).filter((c: any) => c.type === "text").map((c: any) => c.text).join("\n");
}

async function processar(msg: any, contato: any) {
  const tel: string = msg.from;
  const respostaId = msg.interactive?.list_reply?.id || msg.interactive?.button_reply?.id || msg.button?.payload || "";
  const texto = msg.text?.body || msg.interactive?.list_reply?.title || msg.interactive?.button_reply?.title || msg.button?.text || "";

  // grava a mensagem; se já existe (a Meta reenviou), não responde de novo
  const { error: dup } = await sb.from("whatsapp_mensagens").insert({ wa_id: msg.id, telefone: tel, direcao: "entrada", tipo: msg.type, texto: texto.slice(0, 4000) });
  if (dup) { if (dup.code === "23505") return; console.error("log", dup.message); }
  graph({ messaging_product: "whatsapp", status: "read", message_id: msg.id }).catch(() => {});

  if (!["text", "interactive", "button"].includes(msg.type)) {
    // foto, áudio, figurinha… o robô não entende: oferece o menu
    await enviar(tel, [menu(await dados(), "Recebi! Por aqui eu entendo só texto 🙂")]);
    return;
  }

  const hoje = new Date().toISOString().slice(0, 10);
  const { data: conv } = await sb.from("whatsapp_conversas").select("*").eq("telefone", tel).maybeSingle();
  const usos = conv && conv.ia_dia === hoje ? conv.ia_usos_hoje : 0;
  const { data: hist } = await sb.from("whatsapp_mensagens").select("direcao, texto").eq("telefone", tel).order("criado_em", { ascending: false }).limit(9);

  const r = await responder(
    { telefone: tel, nome: contato?.profile?.name, texto, respostaId },
    { dados: await dados(), pausadoAte: conv?.pausado_ate ? new Date(conv.pausado_ate) : null, agora: new Date(),
      historico: (hist || []).slice(1).reverse().filter((h: any) => h.texto), ia: env("ANTHROPIC_API_KEY") ? ia : undefined,
      iaUsosHoje: usos, iaLimiteDia: +(env("IA_LIMITE_DIA") || 20) },
  );

  await sb.from("whatsapp_conversas").upsert({
    telefone: tel, nome: contato?.profile?.name?.slice(0, 80) || conv?.nome || null, atualizado_em: new Date().toISOString(),
    pausado_ate: r.pausarHoras ? new Date(Date.now() + r.pausarHoras * 3600_000).toISOString() : r.despausar ? null : conv?.pausado_ate ?? null,
    ia_dia: hoje, ia_usos_hoje: usos + (r.usouIA ? 1 : 0),
  });
  await enviar(tel, r.saidas);
}

async function enviar(tel: string, saidas: Saida[]) {
  for (const s of saidas) {
    const ok = await graph(payload(tel, s));
    await sb.from("whatsapp_mensagens").insert({ telefone: tel, direcao: "saida", tipo: s.tipo + (ok ? "" : ":erro"), texto: textoDe(s).slice(0, 4000) });
  }
}

Deno.serve(async (req) => {
  const url = new URL(req.url);
  if (req.method === "GET") {
    // a Meta confirma o webhook
    const ok = url.searchParams.get("hub.mode") === "subscribe" && env("WHATSAPP_VERIFY_TOKEN") && url.searchParams.get("hub.verify_token") === env("WHATSAPP_VERIFY_TOKEN");
    return ok ? new Response(url.searchParams.get("hub.challenge") ?? "", { status: 200 }) : new Response("proibido", { status: 403 });
  }
  if (req.method !== "POST") return new Response("ok");
  const corpo = await req.text();
  if (!(await assinaturaValida(corpo, req.headers.get("x-hub-signature-256")))) return new Response("assinatura inválida", { status: 401 });

  let j: any; try { j = JSON.parse(corpo); } catch { return new Response("ok"); }
  const tarefas: Promise<void>[] = [];
  for (const ent of j.entry || []) for (const ch of ent.changes || []) {
    const v = ch.value || {};
    if (v.metadata?.phone_number_id && v.metadata.phone_number_id !== env("WHATSAPP_PHONE_ID")) continue;
    for (const m of v.messages || []) tarefas.push(processar(m, (v.contacts || []).find((c: any) => c.wa_id === m.from)).catch((e) => console.error("processar", e)));
  }
  // responde 200 rápido para a Meta e termina o trabalho em segundo plano
  const tudo = Promise.all(tarefas).then(() => {});
  // @ts-ignore EdgeRuntime existe no Supabase
  if (typeof EdgeRuntime !== "undefined") EdgeRuntime.waitUntil(tudo); else await tudo;
  return new Response("ok");
});
