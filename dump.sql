--
-- PostgreSQL database dump
--

-- Dumped from database version 13.6
-- Dumped by pg_dump version 14.2

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

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: database_user
--

COPY public.users (id, first_name, last_name, email) FROM stdin;
dfe82062-bd69-4d68-8d08-4a17a8bdb48e	Иван	Иванов	ivan@test.com
7a224cad-a851-48e5-9c3f-0c82158eb972	Петр	Петров	petr@test.com
2a513f43-f4b5-4a23-a796-c3cae84f99f8	Сергей	Сергеев	serg@test.com
a555dfb8-3c59-4ad4-8ca5-ea6de86e74d3	Василий	Васильев	vasya@test.com
27796a4f-6437-41d6-b536-179d3de00fd1	Антон	Антонов	anton@test.com
\.


--
-- PostgreSQL database dump complete
--

