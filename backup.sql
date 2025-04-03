--
-- PostgreSQL database dump
--

-- Dumped from database version 13.20 (Debian 13.20-1.pgdg120+1)
-- Dumped by pg_dump version 13.20 (Debian 13.20-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    tg_id bigint NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    username character varying(255),
    phone_number character varying(20),
    payment_status boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    promocode text,
    promocode_usage_count integer NOT NULL,
    promocode_given boolean NOT NULL,
    promocode_is_active character varying(50),
    is_bot boolean NOT NULL,
    payment_date timestamp with time zone,
    last_check_date timestamp with time zone,
    achievement integer,
    id integer NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (tg_id, first_name, last_name, username, phone_number, payment_status, created_at, promocode, promocode_usage_count, promocode_given, promocode_is_active, is_bot, payment_date, last_check_date, achievement, id) FROM stdin;
1426355954	Михаил	Бабаев	\N	\N	f	2025-03-12 11:38:35.389519+00	SAFE-3abc-JGTFQC	0	f	\N	f	\N	\N	1	1
469259491	Lianna	Grigorian	lnxgr	\N	f	2025-03-12 12:59:23.877845+00	SAFE-d41e-B6X5OE	0	f	\N	f	\N	2025-03-12 12:59:45.181608+00	1	3
8131627994	Zugzwang	\N	shturmur	\N	f	2025-03-15 09:22:14.642502+00	SAFE-4fb0-18EAST	0	f	\N	f	\N	\N	1	4
6881974553	Дима	\N	\N	\N	f	2025-03-15 09:59:59.740006+00	SAFE-b60b-MA5NU5	0	f	\N	f	\N	\N	1	5
423275555	Evgeny	Babaev	eababaev	\N	f	2025-03-12 11:39:28.147484+00	SAFE-f415-1AGX06	0	f	\N	f	2025-03-15 10:13:57.286958+00	\N	1	2
5159202371	Дмитрий	Комендант	DMITRIY81KDN	\N	f	2025-03-15 10:04:52.845663+00	SAFE-cc57-TKC3ZC	0	f	\N	f	\N	2025-03-15 10:24:27.362648+00	1	6
6796654142	Евгений	\N	evgeny_second	\N	f	2025-03-15 10:22:45.47472+00	SAFE-9371-HQNH2L	0	f	\N	f	\N	2025-03-15 10:24:50.412882+00	1	7
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_promocode_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_promocode_key UNIQUE (promocode);


--
-- Name: users users_tg_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_tg_id_key UNIQUE (tg_id);


--
-- PostgreSQL database dump complete
--

