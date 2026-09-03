-- AudioAZ System Designer: 회원 온라인 설계 저장 (① 백엔드 채팅이 Supabase SQL Editor에서 실행)
-- 프로젝트: lkbbenyvchddsjsihofv (기존 계정 시스템 재사용)
create table if not exists public.designs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  title text not null default '제목없음',
  ver text not null default 'v.1',
  state jsonb not null,                 -- 도구의 _state 전체 (S)
  updated_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);
create index if not exists designs_user_idx on public.designs(user_id, updated_at desc);
alter table public.designs enable row level security;
create policy "own designs select" on public.designs for select using (auth.uid() = user_id);
create policy "own designs insert" on public.designs for insert with check (auth.uid() = user_id);
create policy "own designs update" on public.designs for update using (auth.uid() = user_id);
create policy "own designs delete" on public.designs for delete using (auth.uid() = user_id);
-- 용량 보호: 사용자당 최대 50개 (초과 시 도구가 오래된 것 삭제 안내)
