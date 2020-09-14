
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

CREATE TABLE public.feed_items (
    id integer NOT NULL,
    url character varying(2000),
    title character varying(100),
    description character varying(5000),
    feed_id integer,
    published timestamp with time zone
);

ALTER TABLE public.feed_items OWNER TO postgres;

CREATE SEQUENCE public.feed_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.feed_items_id_seq OWNER TO postgres;

ALTER SEQUENCE public.feed_items_id_seq OWNED BY public.feed_items.id;

CREATE TABLE public.feeds (
    id integer NOT NULL,
    url character varying(2000),
    parser character varying(20),
    time_format character varying(50),
    last_updated timestamp with time zone
);

ALTER TABLE public.feeds OWNER TO postgres;

CREATE SEQUENCE public.feeds_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.feeds_id_seq OWNER TO postgres;

ALTER SEQUENCE public.feeds_id_seq OWNED BY public.feeds.id;

CREATE TABLE public.follows (
    id integer NOT NULL,
    username character varying,
    feed_id integer
);

ALTER TABLE public.follows OWNER TO postgres;

CREATE SEQUENCE public.follows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.follows_id_seq OWNER TO postgres;

ALTER SEQUENCE public.follows_id_seq OWNED BY public.follows.id;

CREATE TABLE public.reads (
    id integer NOT NULL,
    username character varying,
    item_id integer,
    feed_id integer
);

ALTER TABLE public.reads OWNER TO postgres;

CREATE SEQUENCE public.reads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.reads_id_seq OWNER TO postgres;

ALTER SEQUENCE public.reads_id_seq OWNED BY public.reads.id;

CREATE TABLE public.unreads (
    id integer NOT NULL,
    username character varying,
    item_id integer,
    feed_id integer
);

ALTER TABLE public.unreads OWNER TO postgres;

CREATE SEQUENCE public.unreads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.unreads_id_seq OWNER TO postgres;

ALTER SEQUENCE public.unreads_id_seq OWNED BY public.unreads.id;

CREATE TABLE public.users (
    username character varying(256) NOT NULL,
    password character varying(128)
);

ALTER TABLE public.users OWNER TO postgres;
ALTER TABLE ONLY public.feed_items ALTER COLUMN id SET DEFAULT nextval('public.feed_items_id_seq'::regclass);
ALTER TABLE ONLY public.feeds ALTER COLUMN id SET DEFAULT nextval('public.feeds_id_seq'::regclass);
ALTER TABLE ONLY public.follows ALTER COLUMN id SET DEFAULT nextval('public.follows_id_seq'::regclass);
ALTER TABLE ONLY public.reads ALTER COLUMN id SET DEFAULT nextval('public.reads_id_seq'::regclass);
ALTER TABLE ONLY public.unreads ALTER COLUMN id SET DEFAULT nextval('public.unreads_id_seq'::regclass);

ALTER TABLE ONLY public.feed_items
    ADD CONSTRAINT feed_items_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.feeds
    ADD CONSTRAINT feeds_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.reads
    ADD CONSTRAINT reads_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.unreads
    ADD CONSTRAINT unreads_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);
ALTER TABLE ONLY public.feed_items
    ADD CONSTRAINT feed_items_feed_id_fkey FOREIGN KEY (feed_id) REFERENCES public.feeds(id);
ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_feed_id_fkey FOREIGN KEY (feed_id) REFERENCES public.feeds(id);
ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_username_fkey FOREIGN KEY (username) REFERENCES public.users(username);
ALTER TABLE ONLY public.reads
    ADD CONSTRAINT reads_feed_id_fkey FOREIGN KEY (feed_id) REFERENCES public.feeds(id);
ALTER TABLE ONLY public.reads
    ADD CONSTRAINT reads_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.feed_items(id);
ALTER TABLE ONLY public.reads
    ADD CONSTRAINT reads_username_fkey FOREIGN KEY (username) REFERENCES public.users(username);
ALTER TABLE ONLY public.unreads
    ADD CONSTRAINT unreads_feed_id_fkey FOREIGN KEY (feed_id) REFERENCES public.feeds(id);
ALTER TABLE ONLY public.unreads
    ADD CONSTRAINT unreads_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.feed_items(id);
ALTER TABLE ONLY public.unreads
    ADD CONSTRAINT unreads_username_fkey FOREIGN KEY (username) REFERENCES public.users(username);


INSERT INTO feeds
VALUES
    (1, "https://feeds.feedburner.com/tweakers/mixed", "html5lib", "%a, %d %b %Y %H:%M:%S %Z", "2020-09-01 00:00:00-00"),
    (2, "http://www.nu.nl/rss/Algemeen", "lxml", "%a, %d %b %Y %H:%M:%S %z", "2020-09-01 00:00:00-00");
