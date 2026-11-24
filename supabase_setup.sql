-- Banco de dados das contas de clientes da DE men (Supabase)
-- Cada cliente só enxerga e altera os próprios dados (Row Level Security).

create table if not exists public.perfis (
  id uuid primary key references auth.users (id) on delete cascade,
  nome text,
  whatsapp text,
  cidade text,
  criado_em timestamptz not null default now()
);

create table if not exists public.favoritos (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  produto text not null,
  criado_em timestamptz not null default now(),
  unique (user_id, produto)
);

create table if not exists public.interesses (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  produto text not null,
  marca text,
  criado_em timestamptz not null default now()
);

alter table public.perfis     enable row level security;
alter table public.favoritos  enable row level security;
alter table public.interesses enable row level security;

create policy "perfil: ver o meu"      on public.perfis for select to authenticated using ((select auth.uid()) = id);
create policy "perfil: editar o meu"   on public.perfis for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

create policy "favoritos: ver os meus"    on public.favoritos for select to authenticated using ((select auth.uid()) = user_id);
create policy "favoritos: criar os meus"  on public.favoritos for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "favoritos: apagar os meus" on public.favoritos for delete to authenticated using ((select auth.uid()) = user_id);

create policy "interesses: ver os meus"   on public.interesses for select to authenticated using ((select auth.uid()) = user_id);
create policy "interesses: criar os meus" on public.interesses for insert to authenticated with check ((select auth.uid()) = user_id);

create index if not exists favoritos_user_idx  on public.favoritos (user_id);
create index if not exists interesses_user_idx on public.interesses (user_id);

-- cria o perfil automaticamente quando o cliente se cadastra
create or replace function public.criar_perfil()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.perfis (id, nome, whatsapp)
  values (new.id, new.raw_user_meta_data ->> 'nome', new.raw_user_meta_data ->> 'whatsapp');
  return new;
end;
$$;

drop trigger if exists ao_criar_usuario on auth.users;
create trigger ao_criar_usuario
  after insert on auth.users
  for each row execute function public.criar_perfil();
