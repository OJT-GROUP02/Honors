--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

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
-- Name: change_sum_of_grades_award(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.change_sum_of_grades_award() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF (SELECT classification FROM student WHERE student.student_id = old.student_id) = 'Regular'
        THEN
            IF (new.sum_of_grades / (old.total_units)) <= 1.75 AND (new.sum_of_grades / (old.total_units)) > 1.45 THEN new.award_id = 3;
            ELSIF (new.sum_of_grades / (old.total_units)) <= 1.45 AND (new.sum_of_grades / (old.total_units)) > 1.25 THEN new.award_id = 2;
            ELSIF(new.sum_of_grades / (old.total_units)) <= 1.25 THEN new.award_id = 1;
            ELSE new.award_id = NULL;
            END IF;
    ELSIF (SELECT classification FROM student WHERE student.student_id = old.student_id) = 'Irregular'
        THEN
            IF (new.sum_of_grades / (old.total_units)) <= 1.75
                THEN
                    new.award_id = 4;
            ELSE
                new.award_id = NULL;
            END IF;
    END IF;

    RETURN new;
END;
$$;


ALTER FUNCTION public.change_sum_of_grades_award() OWNER TO postgres;

--
-- Name: change_total_units_award(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.change_total_units_award() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF (SELECT classification FROM student WHERE student.student_id = old.student_id) = 'Regular'
        THEN
            IF (old.sum_of_grades / (new.total_units)) <= 1.75 AND (old.sum_of_grades / (new.total_units)) > 1.45 THEN new.award_id = 3;
            ELSIF (old.sum_of_grades / (new.total_units)) <= 1.45 AND (old.sum_of_grades / (new.total_units)) > 1.25 THEN new.award_id = 2;
            ELSIF(old.sum_of_grades / (new.total_units)) <= 1.25 THEN new.award_id = 1;
            ELSE new.award_id = NULL;
            END IF;
    ELSIF (SELECT classification FROM student WHERE student.student_id = old.student_id) = 'Irregular'
        THEN
            IF (old.sum_of_grades / (new.total_units)) <= 1.75
                THEN
                    new.award_id = 4;
            ELSE
                new.award_id = NULL;
            END IF;
    END IF;

    RETURN new;
END;
$$;


ALTER FUNCTION public.change_total_units_award() OWNER TO postgres;

--
-- Name: generate_award(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.generate_award() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF (SELECT classification FROM student WHERE student.student_id = new.student_id) = 'Regular'
        THEN
            IF (new.sum_of_grades / (new.total_units)) <= 1.75 AND (new.sum_of_grades / (new.total_units)) > 1.45 THEN new.award_id = 3;
            ELSIF (new.sum_of_grades / (new.total_units)) <= 1.45 AND (new.sum_of_grades / (new.total_units)) > 1.25 THEN new.award_id = 2;
            ELSIF(new.sum_of_grades / (new.total_units)) <= 1.25 THEN new.award_id = 1;
            END IF;
    ELSIF (SELECT classification FROM student WHERE student.student_id = new.student_id) = 'Irregular'
        THEN
            new.award_id = 4;
    END IF;

    RETURN new;
END;
$$;


ALTER FUNCTION public.generate_award() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: awards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.awards (
    award_id integer NOT NULL,
    award_title character varying(30) NOT NULL
);


ALTER TABLE public.awards OWNER TO postgres;

--
-- Name: awards_award_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.awards_award_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.awards_award_id_seq OWNER TO postgres;

--
-- Name: awards_award_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.awards_award_id_seq OWNED BY public.awards.award_id;


--
-- Name: college; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.college (
    college_id integer NOT NULL,
    college_name character varying(200) NOT NULL,
    college_address character varying(200) NOT NULL
);


ALTER TABLE public.college OWNER TO postgres;

--
-- Name: college_college_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.college_college_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.college_college_id_seq OWNER TO postgres;

--
-- Name: college_college_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.college_college_id_seq OWNED BY public.college.college_id;


--
-- Name: committee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.committee (
    committee_id integer NOT NULL,
    position_id integer,
    full_name character varying(150) NOT NULL,
    professional_title character varying(15),
    office_position character varying(150),
    college_id integer
);


ALTER TABLE public.committee OWNER TO postgres;

--
-- Name: committee_committee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.committee_committee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.committee_committee_id_seq OWNER TO postgres;

--
-- Name: committee_committee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.committee_committee_id_seq OWNED BY public.committee.committee_id;


--
-- Name: committee_position; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.committee_position (
    position_id integer NOT NULL,
    hierarchy_id integer NOT NULL,
    position_name character varying(50) NOT NULL
);


ALTER TABLE public.committee_position OWNER TO postgres;

--
-- Name: committee_position_position_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.committee_position_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.committee_position_position_id_seq OWNER TO postgres;

--
-- Name: committee_position_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.committee_position_position_id_seq OWNED BY public.committee_position.position_id;


--
-- Name: dean; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dean (
    dean_id integer NOT NULL,
    dean_name character varying(150) NOT NULL,
    professional_title character varying(30),
    college_id integer
);


ALTER TABLE public.dean OWNER TO postgres;

--
-- Name: dean_dean_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dean_dean_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dean_dean_id_seq OWNER TO postgres;

--
-- Name: dean_dean_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dean_dean_id_seq OWNED BY public.dean.dean_id;


--
-- Name: grade; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grade (
    grade_id bigint NOT NULL,
    student_id integer NOT NULL,
    total_units integer,
    sum_of_grades real,
    final_gwa numeric(5,4) GENERATED ALWAYS AS ((sum_of_grades / (total_units)::double precision)) STORED,
    award_id integer
);


ALTER TABLE public.grade OWNER TO postgres;

--
-- Name: grade_grade_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grade_grade_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.grade_grade_id_seq OWNER TO postgres;

--
-- Name: grade_grade_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grade_grade_id_seq OWNED BY public.grade.grade_id;


--
-- Name: header; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.header (
    header_id bigint NOT NULL,
    college_id integer NOT NULL,
    semester character varying(20) NOT NULL,
    academic_year character varying(10) NOT NULL
);


ALTER TABLE public.header OWNER TO postgres;

--
-- Name: header_header_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.header_header_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.header_header_id_seq OWNER TO postgres;

--
-- Name: header_header_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.header_header_id_seq OWNED BY public.header.header_id;


--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    student_id bigint NOT NULL,
    last_name character varying(50) NOT NULL,
    first_name character varying(50) NOT NULL,
    middle_name character varying(50),
    gender character(1) NOT NULL,
    classification character varying(20)
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Name: student_student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_student_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_student_id_seq OWNER TO postgres;

--
-- Name: student_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_student_id_seq OWNED BY public.student.student_id;


--
-- Name: awards award_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.awards ALTER COLUMN award_id SET DEFAULT nextval('public.awards_award_id_seq'::regclass);


--
-- Name: college college_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.college ALTER COLUMN college_id SET DEFAULT nextval('public.college_college_id_seq'::regclass);


--
-- Name: committee committee_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.committee ALTER COLUMN committee_id SET DEFAULT nextval('public.committee_committee_id_seq'::regclass);


--
-- Name: committee_position position_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.committee_position ALTER COLUMN position_id SET DEFAULT nextval('public.committee_position_position_id_seq'::regclass);


--
-- Name: dean dean_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dean ALTER COLUMN dean_id SET DEFAULT nextval('public.dean_dean_id_seq'::regclass);


--
-- Name: grade grade_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade ALTER COLUMN grade_id SET DEFAULT nextval('public.grade_grade_id_seq'::regclass);


--
-- Name: header header_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.header ALTER COLUMN header_id SET DEFAULT nextval('public.header_header_id_seq'::regclass);


--
-- Name: student student_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student ALTER COLUMN student_id SET DEFAULT nextval('public.student_student_id_seq'::regclass);


--
-- Data for Name: awards; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.awards (award_id, award_title) FROM stdin;
1	Summa Cum Laude
2	Magna Cum Laude
3	Cum Laude
4	with Academic Distinction
\.


--
-- Data for Name: college; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.college (college_id, college_name, college_address) FROM stdin;
1	College of Arts and Letters	Legazpi City, Albay
2	College of Education	Daraga, Albay
3	College of Nursing	Legazpi City, Albay
5	College of Business, Economics, and Management	Daraga, Albay
6	College of Social Sciences and Philosophy	Daraga, Albay
7	College of Engineering	Legazpi City, Albay
8	Institute of Architecture	Legazpi City, Albay
9	College of Industrial Technology	Legazpi City, Albay
10	College of Agriculture and Forestry	Guinobatan, Albay
11	Polangui Campus	Polangui, Albay
12	Tabaco Campus	Tabaco, Albay
13	Gubat Campus	Gubat, Sorsogon
14	College of Science	Legazpi City, Albay
4	Institute of Physical Education, Sports, and Recreation	Daraga, Albay
\.


--
-- Data for Name: committee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.committee (committee_id, position_id, full_name, professional_title, office_position, college_id) FROM stdin;
8	2	Mark Francis G. Ng	\N	Department Chair	5
9	1	Salvador M. Abiño	\N	Registrar II	5
6	3	Christina U. Ballesteros	\N	Faculty In-Charge for Guidance Services	5
7	3	Edna B. Mata	M.Econ	Coordinator of Student Services	5
\.


--
-- Data for Name: committee_position; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.committee_position (position_id, hierarchy_id, position_name) FROM stdin;
1	1	Chairperson
2	2	Co-Chairperson
3	3	Member
\.


--
-- Data for Name: dean; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dean (dean_id, dean_name, professional_title, college_id) FROM stdin;
1	Eddie S. See	Ed.D.	5
\.


--
-- Data for Name: grade; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grade (grade_id, student_id, total_units, sum_of_grades, award_id) FROM stdin;
3	3	234	339.5	3
4	4	234	350.1	3
5	5	234	352.1	3
6	6	234	355.1	3
7	7	234	355.3	3
8	8	234	359.6	3
9	9	234	362.2	3
10	10	234	366.8	3
11	11	234	378.4	3
12	12	234	378.4	3
13	13	234	378.5	3
14	14	234	378.6	3
15	15	234	378.8	3
16	16	234	381.7	3
17	17	234	382.6	3
18	18	234	383.1	3
19	19	234	385.1	3
20	20	234	385.1	3
21	21	234	386.8	3
22	22	234	387.4	3
23	23	234	387.5	3
24	24	234	390.1	3
25	25	234	391	3
26	26	234	391.3	3
27	27	234	391.5	3
28	28	234	393.1	3
29	29	234	394.2	3
30	30	234	395.5	3
31	31	234	395.7	3
32	32	234	396.7	3
34	34	234	398.3	3
35	35	234	398.7	3
36	36	234	399.3	3
37	37	234	400.3	3
38	38	234	401.1	3
39	39	234	401.3	3
40	40	234	401.4	3
41	41	234	401.9	3
42	42	234	401.9	3
43	43	234	401.9	3
44	44	234	402	3
47	47	234	404.9	3
48	48	234	405.3	3
49	49	234	405.5	3
50	50	234	405.7	3
51	51	234	406.3	3
52	52	234	407.3	3
53	53	234	407.6	3
54	54	234	407.7	3
55	55	234	408.2	3
56	56	234	408.3	3
57	57	234	408.8	3
58	58	234	409.1	3
59	59	234	411.7	\N
60	60	234	412	\N
61	61	234	412.5	\N
62	62	234	412.8	\N
63	63	234	417.3	\N
64	64	234	422.2	\N
65	65	234	417.9	\N
66	66	234	418.2	\N
67	67	234	419	\N
68	68	234	420	\N
69	69	234	420.1	\N
70	70	234	420.9	\N
71	71	234	421.3	\N
72	72	234	422.9	\N
73	73	216	363	\N
74	74	234	425.6	\N
75	75	234	426.5	\N
76	76	234	427.2	\N
77	77	234	430.2	\N
78	78	234	430.6	\N
79	79	234	431.8	\N
80	80	234	432.3	\N
81	81	234	433.5	\N
82	82	234	439.2	\N
83	83	234	440.4	\N
84	84	234	456.6	\N
85	85	\N	\N	\N
33	33	234	397.6	3
45	45	234	402.5	3
46	46	234	402.7	4
1	1	234	414.3	\N
2	2	234	330.9	2
\.


--
-- Data for Name: header; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.header (header_id, college_id, semester, academic_year) FROM stdin;
1	5	2nd Semester	2019-2020
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (student_id, last_name, first_name, middle_name, gender, classification) FROM stdin;
1	Biñas	Jhon Christian	Grimpluma	M	\N
2	Carizo	Bethany Jayne	Ibañez	F	Regular
3	Pispis	Arvin Joehn	Misolas	M	Regular
4	Jerusalem	Emmanuel	Zaragosa	M	Regular
5	Rempillo	John Kenneth	Rodriguez	M	Regular
6	Wong	May Ann	Maralit	F	Regular
7	Serrano	Christian	Malagueño	M	Regular
8	Nobleza	Mark Anthony	Sanchez	M	Regular
9	Labalan	Mary Dimple	Navera	F	Regular
10	Guardian	Julius Ian	Buatin	M	Regular
11	Garcia	Janne Nicole	Priagola	F	Regular
12	Tanay	Michael Salvador	Osi	M	Regular
13	Basilla	Sheila	Bataller	F	Regular
14	Apuli	Viviene Mae	Resare	F	Regular
15	Abadesa	Nicole	Casulla	F	Regular
16	Olayta	Carlo	Pincaro	M	Regular
17	Soneja	Shenaren	Alapide	F	Regular
18	Abo	Abby Gail	Ativo	F	Regular
19	Razal	Melrose	Nota	F	Regular
20	Campita	Noemi	Sumalde	F	Regular
21	Puenlabrada	Kristel Anne	Bonayon	F	Regular
22	Belen	Shienalyn Joy	Vargas	F	Regular
23	Estropia	Estelle Jonna	Jao	F	Regular
24	Fortes	Rhyssa Mari Angela	Gacosta	F	Regular
25	Antiquera	Christine May	Maralit	F	Regular
26	Lacayanga	Danica Hazel	Almasco	F	Regular
27	Ragas	Krisha Mae	Raro	F	Regular
28	Atacador	Pia May	Zara	F	Regular
29	Ferrer	Jendy Rose	Federico	F	Regular
30	Lolo	Trizia Anne	Morota	F	Regular
31	Moico	Geraldine	Reblora	F	Regular
32	De Vera	Jazreel	Sadio	F	Regular
33	Malejana	Bea	Ativo	F	Regular
34	Nuñez	Rowena	Mendez	F	Regular
35	Belleza	Irish Diane	Buates	F	Regular
36	Escalante	Angelica	Dichoso	F	Regular
37	Babasa	Catherine	Belgica	F	Regular
38	Dayto	Aira Vianca	Vibar	F	Regular
39	Evangelio	Veronica	Supeña	F	Regular
40	Aspe	Kathleen Alexa	Dasco	F	Regular
41	Callo	Norlissa Rose	Vargas	F	Regular
42	Pagarigan	Airene	Mesina	F	Regular
43	Nota	Oscar	Calag	M	Regular
44	Tolosa	Walter	Nebreja	M	Regular
45	Perez	Ana Margarita	Pollante	F	Regular
46	Go	Gerald	Jebulan	M	Irregular
47	Arnado	Lizelle Anne	Magno	F	Regular
48	Tee	Virgette Mae	Leosala	F	Regular
49	Salivio	April Cyron	Borromeo	F	Regular
50	Miranda	Trixy Quinn	Serrano	F	Regular
51	Gonzales	Jaymee Rose	Chan	F	Regular
52	Hipolito	Tessa Denissa	Gelua	F	Regular
53	Maloles	Syra	Tomagan	F	Regular
54	Millena	Bernardine Ella	Tolosa	F	Regular
55	Reparip	Mary Joy	Rebellon	F	Regular
56	Carretero	Mark Joseph	Granadillos	M	Regular
57	Lozada	Joceline Ann	Ayende	F	Regular
58	Aviso	Kate Louise	Cadag	F	Regular
59	Llaneta	Ian	Mediavillo	M	\N
60	Baroso	Charlene	Bellen	F	\N
61	Fullente	Lyka Marie	Escurel	F	\N
62	Relorcasa	Diana	Alcaldeza	F	\N
63	Salando	Alizza May	Cantillo	F	\N
64	Catorce	Merari Deborah	Falabi	F	\N
65	Barela	Carla Jae	Bitancur	F	\N
66	Guerrero	Stacy Kate	Yuson	F	\N
67	Daria	Justine	Lorilla	F	\N
68	Apurado	Cianiah Kaela	Mimay	F	\N
69	Imperial	Hans Christian	Gonzales	M	\N
70	Abejo	Ma. Elaine	Jacob	F	\N
71	Suruiz	Ella Mae	Patiño	F	\N
72	Goyena	China	Araya	F	\N
73	Consuelo	Joanne Karla	Caldit	F	\N
74	Deona	Christine Joy	Belano	F	\N
75	Juaquera	Ignacio	Rodriguez	M	\N
76	Leosala	Vanessa	Alemania	F	\N
77	Cañete	Vanessa Mae	Sia	F	\N
78	Calisin	Jazmin Shane	Adlaon	F	\N
79	Pavilando	Rev	Neo	M	\N
80	Naparam	Glenn Homer	Polo	M	\N
81	Paguio	Christine	Reocasa	F	\N
82	Camposano	Renee Lynne	Maquiñiana	F	\N
83	Balilo	Pauline Anne	Vibar	F	\N
84	Cellona	Francis Edrian	Bien	M	\N
85	Dela Cruz	Johann Patrick	Beli	M	\N
\.


--
-- Name: awards_award_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.awards_award_id_seq', 4, true);


--
-- Name: college_college_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.college_college_id_seq', 14, true);


--
-- Name: committee_committee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.committee_committee_id_seq', 9, true);


--
-- Name: committee_position_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.committee_position_position_id_seq', 3, true);


--
-- Name: dean_dean_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dean_dean_id_seq', 1, true);


--
-- Name: grade_grade_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grade_grade_id_seq', 85, true);


--
-- Name: header_header_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.header_header_id_seq', 1, true);


--
-- Name: student_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_student_id_seq', 85, true);


--
-- Name: awards awards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.awards
    ADD CONSTRAINT awards_pkey PRIMARY KEY (award_id);


--
-- Name: college college_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.college
    ADD CONSTRAINT college_pkey PRIMARY KEY (college_id);


--
-- Name: committee committee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.committee
    ADD CONSTRAINT committee_pkey PRIMARY KEY (committee_id);


--
-- Name: committee_position committee_position_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.committee_position
    ADD CONSTRAINT committee_position_pkey PRIMARY KEY (position_id);


--
-- Name: dean dean_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dean
    ADD CONSTRAINT dean_pkey PRIMARY KEY (dean_id);


--
-- Name: grade grade_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade
    ADD CONSTRAINT grade_pkey PRIMARY KEY (grade_id);


--
-- Name: header header_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.header
    ADD CONSTRAINT header_pkey PRIMARY KEY (header_id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (student_id);


--
-- Name: grade change_sum_of_grades_update; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER change_sum_of_grades_update BEFORE UPDATE OF sum_of_grades ON public.grade FOR EACH ROW EXECUTE FUNCTION public.change_sum_of_grades_award();


--
-- Name: grade change_total_units_update; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER change_total_units_update BEFORE UPDATE OF total_units ON public.grade FOR EACH ROW EXECUTE FUNCTION public.change_total_units_award();


--
-- Name: grade generate_award_insert; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER generate_award_insert BEFORE INSERT ON public.grade FOR EACH ROW EXECUTE FUNCTION public.generate_award();


--
-- Name: committee committee_college_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.committee
    ADD CONSTRAINT committee_college_id_fkey FOREIGN KEY (college_id) REFERENCES public.college(college_id);


--
-- Name: committee committee_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.committee
    ADD CONSTRAINT committee_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.committee_position(position_id);


--
-- Name: dean dean_college_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dean
    ADD CONSTRAINT dean_college_id_fkey FOREIGN KEY (college_id) REFERENCES public.college(college_id);


--
-- Name: grade grade_award_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade
    ADD CONSTRAINT grade_award_id_fkey FOREIGN KEY (award_id) REFERENCES public.awards(award_id);


--
-- Name: grade grade_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade
    ADD CONSTRAINT grade_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(student_id);


--
-- Name: header header_college_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.header
    ADD CONSTRAINT header_college_id_fkey FOREIGN KEY (college_id) REFERENCES public.college(college_id);


--
-- PostgreSQL database dump complete
--

