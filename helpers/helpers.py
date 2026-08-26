"""
Helper functions for db setup and scoring logic
"""
import os
import random

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

COMPETENCIES = ['communication', 'technical', 'problem_solving']


def get_db_connection():
    """
    Establishes a connection to the Postgres database
    :return: psycopg connection object
    """
    return psycopg.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        row_factory=dict_row
    )


def generate_competency_score(competency: str):
    """
    Generates score and feedback based on competency
    :param competency: competency type
    :return: score and feedback as tuple
    """
    if competency not in COMPETENCIES:
        raise ValueError('Invalid competency. Must be either communication or technical or problem_solving')

    score = random.randrange(0, 6)

    if 0 <= score <= 2:
        feedback = 'Needs improvement'
    elif 2 <= score <= 3:
        feedback = 'Good performance'
    else:
        feedback = 'Excellent clarity'

    return score, feedback


def compute_overall_score(
        communication_score: int,
        technical_score: int,
        problem_solving_score: int
):
    """
    Computes overall score average
    :param communication_score: Communication score
    :param technical_score: Technical score
    :param problem_solving_score: Problem solving score
    :return:
    """
    return (communication_score + technical_score + problem_solving_score) / 3
