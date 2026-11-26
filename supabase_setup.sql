-- DE men — banco do site (Supabase). Contas, favoritos, interesses, avaliações e SAC.
-- Rodar uma vez no SQL Editor do Supabase (já aplicado no projeto demen-loja).

create table if not exists public.perfis (
  id uuid primary key references auth.users(id) on delete cascade,
  nome text check (char_length(nome) <= 80),
  whatsapp text check (char_length(whatsapp) <= 20),
  cidade text check (char_length(cidade) <= 60),
  criado_em timestamptz not null default now()
);

create table if not exists public.favoritos (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  produto text not null check (char_length(produto) <= 160),
  criado_em timestamptz not null default now(),
  unique (user_id, produto)
);

create table if not exists public.interesses (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  produto text not null check (char_length(produto) <= 160),
  marca text check (char_length(marca) <= 60),
  tamanho text check (char_length(tamanho) <= 10),
  qtd int not null default 1 check (qtd between 1 and 50),
  origem text check (origem in ('pedir','sacola')),
  criado_em timestamptz not null default now()
);

create table if not exists public.avaliacoes (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  produto text not null check (char_length(produto) <= 160),
  produto_nome text check (char_length(produto_nome) <= 160),
  nota int not null check (nota between 1 and 5),
  texto text not null check (char_length(texto) between 3 and 1000),
  nome text check (char_length(nome) <= 60),
  cidade text check (char_length(cidade) <= 60),
  aprovado boolean not null default false,
  criado_em timestamptz not null default now(),
  unique (user_id, produto)
);

create table if not exists public.chamados (
  id bigint generated always as identity primary key,
  protocolo text not null unique check (char_length(protocolo) <= 20),
  user_id uuid default auth.uid() references auth.users(id) on delete set null,
  nome text not null check (char_length(nome) between 2 and 80),
  contato text not null check (char_length(contato) between 5 and 120),
  assunto text not null check (char_length(assunto) <= 60),
  pedido text check (char_length(pedido) <= 40),
  mensagem text not null check (char_length(mensagem) between 5 and 2000),
  status text not null default 'aberto' check (status in ('aberto','em andamento','resolvido')),
  resposta text check (char_length(resposta) <= 2000),
  criado_em timestamptz not null default now()
);

create index if not exists favoritos_user_idx on public.favoritos (user_id);
create index if not exists interesses_user_idx on public.interesses (user_id);
create index if not exists avaliacoes_produto_idx on public.avaliacoes (produto) where aprovado;
create index if not exists avaliacoes_user_idx on public.avaliacoes (user_id);
create index if not exists chamados_user_idx on public.chamados (user_id);

alter table public.perfis enable row level security;
alter table public.favoritos enable row level security;
alter table public.interesses enable row level security;
alter table public.avaliacoes enable row level security;
alter table public.chamados enable row level security;

-- Perfis: cada um vê e edita só o seu
create policy "perfil proprio - ler" on public.perfis for select to authenticated using ((select auth.uid()) = id);
create policy "perfil proprio - editar" on public.perfis for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

-- Favoritos e interesses: só do próprio usuário
create policy "favoritos proprios - ler" on public.favoritos for select to authenticated using ((select auth.uid()) = user_id);
create policy "favoritos proprios - criar" on public.favoritos for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "favoritos proprios - apagar" on public.favoritos for delete to authenticated using ((select auth.uid()) = user_id);
create policy "interesses proprios - ler" on public.interesses for select to authenticated using ((select auth.uid()) = user_id);
create policy "interesses proprios - criar" on public.interesses for insert to authenticated with check ((select auth.uid()) = user_id);

-- Avaliações: público vê as aprovadas; cliente vê as suas; entra sempre como não aprovada
create policy "avaliacoes aprovadas - ler" on public.avaliacoes for select to anon, authenticated using (aprovado = true);
create policy "avaliacoes proprias - ler" on public.avaliacoes for select to authenticated using ((select auth.uid()) = user_id);
create policy "avaliacoes proprias - criar" on public.avaliacoes for insert to authenticated with check ((select auth.uid()) = user_id and aprovado = false);
create policy "avaliacoes proprias - apagar" on public.avaliacoes for delete to authenticated using ((select auth.uid()) = user_id);

-- SAC: qualquer um abre chamado; logado vê os seus. A loja responde pelo painel do Supabase.
create policy "chamados - abrir" on public.chamados for insert to anon, authenticated
  with check (status = 'aberto' and resposta is null and (user_id is null or user_id = (select auth.uid())));
create policy "chamados proprios - ler" on public.chamados for select to authenticated using ((select auth.uid()) = user_id);

-- Cria o perfil quando a conta é criada
create or replace function public.criar_perfil() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.perfis (id, nome, whatsapp)
  values (new.id,
          left(coalesce(new.raw_user_meta_data->>'nome', new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'), 80),
          left(new.raw_user_meta_data->>'whatsapp', 20))
  on conflict (id) do nothing;
  return new;
end $$;
revoke execute on function public.criar_perfil() from public, anon, authenticated;
drop trigger if exists ao_criar_usuario on auth.users;
create trigger ao_criar_usuario after insert on auth.users for each row execute function public.criar_perfil();

-- ===== Avise-me quando chegar =====
create table if not exists public.avisos (
  id bigint generated always as identity primary key,
  produto text not null check (char_length(produto) <= 160), produto_nome text check (char_length(produto_nome) <= 160),
  tamanho text check (char_length(tamanho) <= 10), nome text check (char_length(nome) <= 80),
  contato text not null check (char_length(contato) between 5 and 120),
  user_id uuid default auth.uid() references auth.users(id) on delete set null,
  avisado boolean not null default false, criado_em timestamptz not null default now()
);
alter table public.avisos enable row level security;
create policy "avisos - pedir" on public.avisos for insert to anon, authenticated with check (avisado = false and (user_id is null or user_id = (select auth.uid())));
create policy "avisos proprios - ler" on public.avisos for select to authenticated using ((select auth.uid()) = user_id);
-- (gatilho limitar_avisos: 15 por contato/dia e 500/dia no total; execução revogada do público)

-- ===== Pedidos pagos online (só a função "pagamento" grava; a loja vê no painel) =====
create table if not exists public.pedidos (
  id bigint generated always as identity primary key, codigo text not null unique, itens jsonb not null,
  subtotal numeric(10,2) not null, frete numeric(10,2) not null default 0, frete_desc text, total numeric(10,2) not null,
  cliente_nome text, cliente_contato text, cep text, endereco text,
  status text not null default 'aguardando_pagamento', mp_preferencia text, mp_pagamento text,
  criado_em timestamptz not null default now(), atualizado_em timestamptz not null default now()
);
alter table public.pedidos enable row level security;
