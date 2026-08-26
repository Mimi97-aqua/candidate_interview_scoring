CREATE TABLE candidates (
    id serial primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) unique not null,
    created_at timestamp default now(),
    updated_at timestamp
);

CREATE TYPE interview_status AS (
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
    communication_score int not null check (0 <= communication_score <= 5),
    problem_solving_score int not null check ( 0 <= problem_solving_score <= 5 ),
    technical_score int not null (0 <= technical_score <= 5),
    overall_score int not null (0 <= overall_score <= 5),
    communication_feedback text,
    created_at timestamp default now()
);