CREATE TABLE candidates (
    id serial primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) unique not null,
    created_at timestamp default now(),
    updated_at timestamp
);

CREATE TYPE interview_status AS ENUM (
    'processing', -- still processing
    'completed', -- interview successfully processed
    'failed' -- there was an issue processing the interview
    );

CREATE TABLE interviews (
    id serial primary key,
    candidate_id int references candidates(id) not null,
    interview_date date not null,
    status interview_status not null,
    transcript text not null,
    created_at timestamp default now()
);

CREATE TABLE scores (
    id serial primary key,
    interview_id int references interviews(id) not null,
    communication_score int not null check (communication_score between 0 and 5),
    problem_solving_score int not null check (problem_solving_score between 0 and 5),
    technical_score int not null check (technical_score between 0 and 5),
    overall_score int not null check (overall_score between 0 and 5),
    communication_feedback text,
    graded_at timestamp default now()
);