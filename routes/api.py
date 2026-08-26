"""
Interviews API
- Create interview with scorinng pipeline initialized
- Fetch interview(s)
"""
import datetime

from flask import Blueprint, jsonify, request

from helpers.helpers import *

interviews = Blueprint('interviews', __name__, url_prefix='/api')


@interviews.route('/interviews', methods=['POST'])
def create_interview():
    """
    Create an interview
    :return:
    """
    # get necessary data
    data = request.get_json()
    required_fields = ['candidate_id', 'interview_date', 'interview_transcript']

    if not all(field in data for field in required_fields):
        return jsonify({
            'status': 'error',
            'message': f"All required fields are required: {required_fields}"
        }), 400

    candidate_id = data['candidate_id']
    interview_transcript = data['interview_transcript']

    try:
        interview_date = datetime.datetime.strptime(data['interview_date'], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': f"Invalid interview_date: {data['interview_date']}. Expected format YYYY-MM-DD"
        }), 400

    # verify that date is valid
    if interview_date < datetime.date.today():
        return jsonify({
            'status': 'error',
            'message': f"Invalid interview date: {interview_date}. Must be in the present or future"
        }), 400

    # scoring pipeline
    competencies = ['communication', 'technical', 'problem_solving']
    competency_score_results = []
    for item in competencies:
        result = generate_competency_score(item)
        competency_score_results.append(result)

    communication = competency_score_results[0]
    technical = competency_score_results[1]
    problem_solving = competency_score_results[2]

    overall_score = compute_overall_score(communication[0], technical[0], problem_solving[0])

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # check that candidate ID is valid
            cursor.execute("""
                select 1
                from candidates
                    where id = %s
            """, (candidate_id,))

            result = cursor.fetchone()
            if not result:
                return jsonify({
                    'status': 'error',
                    'message': 'Candidate not found'
                }), 404

            # insert interview data into interviews table
            cursor.execute("""
                insert into interviews (candidate_id, interview_date, transcript, status)
                    values (%s, %s, %s, %s)
                returning id, status
            """, (candidate_id, interview_date, interview_transcript, 'processing'))
            interview_result = cursor.fetchone()
            interview_id = interview_result[0]

            if not interview_result:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to create interview'
                }), 400

            try:
                # insert scoring data into scores table
                cursor.execute("""
                               insert into scores (interview_id, communication_score, technical_score,
                                                   problem_solving_score,
                                                   overall_score, communication_feedback)
                               values (%s, %s, %s, %s, %s, %s)
                               """, (
                                   interview_id,
                                   communication[0],
                                   technical[0],
                                   problem_solving[0],
                                   overall_score,
                                   communication[1]
                               ))

            except psycopg.errors.Error:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to create scores for interview'
                }), 400

            # update interviews table with new state
            cursor.execute("""
                update interviews
                set status = 'completed'
                    where id = %s
            """, (interview_id,))

    return jsonify({
        'status': 'success',
        'message': 'Successfully created interview',
        'interview_id': interview_id,
        'interview_status': 'processing'
    }), 200
