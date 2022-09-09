CREATE TABLE IF NOT EXISTS public.books
(
    id SERIAL NOT NULL,
    title VARCHAR NOT NULL,
    rating double precision NOT NULL,
    fk_username VARCHAR ( 50 ),
	CONSTRAINT books_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.accounts (
  id serial PRIMARY KEY,
  username VARCHAR ( 50 ) UNIQUE NOT NULL,
  password VARCHAR ( 50 ) NOT NULL
);


TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.books
    OWNER to postgres;

ALTER TABLE IF EXISTS public.accounts
    OWNER to postgres;