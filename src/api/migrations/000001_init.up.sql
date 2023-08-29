CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    api_key TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.jobs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT,
    created_at TIMESTAMP without time zone DEFAULT now(),
    logs TEXT,
    run_type TEXT NOT NULL,
    image TEXT,
    command TEXT,
    status TEXT
);
