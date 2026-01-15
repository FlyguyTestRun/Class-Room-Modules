"""
EduOps Command Center - API Gateway
Flask REST API with PowerShell integration
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import redis
import os
import json
import logging
from datetime import datetime
from powershell_executor import create_student_account, create_staff_account

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'eduops'),
        user=os.getenv('POSTGRES_USER', 'eduops_user'),
        password=os.getenv('POSTGRES_PASSWORD', 'changeme123')
    )

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'api-gateway'
    }), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, user_type, first_name, last_name, email, username, is_active FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
        'users': [
            {
                'id': u[0],
                'type': u[1],
                'first_name': u[2],
                'last_name': u[3],
                'email': u[4],
                'username': u[5],
                'is_active': u[6]
            } for u in users
        ]
    }), 200

@app.route('/api/v1/users/student', methods=['POST'])
def create_student():
    """Create student account via PowerShell"""
    data = request.json

    # Validate input
    required = ['student_id', 'first_name', 'last_name', 'grade_level', 'graduation_year']
    if not all(k in data for k in required):
        return jsonify({'error': f'Missing required fields: {required}'}), 400

    job_id = f"job_{datetime.utcnow().timestamp()}"

    try:
        # Execute PowerShell
        result = create_student_account(
            student_id=data['student_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            grade_level=data['grade_level'],
            graduation_year=data['graduation_year']
        )

        if result['success']:
            # Store in PostgreSQL
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (user_type, student_id, first_name, last_name, email, username, grade_level, graduation_year, is_active)
                VALUES ('student', %s, %s, %s, %s, %s, %s, %s, TRUE)
                RETURNING id
            """, (
                data['student_id'],
                data['first_name'],
                data['last_name'],
                result['output'].get('Email'),
                result['output'].get('Username'),
                data['grade_level'],
                data['graduation_year']
            ))
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()

            # Store job result
            job_data = {
                'job_id': job_id,
                'type': 'create_student',
                'status': 'completed',
                'user_id': user_id,
                'result': result['output'],
                'completed_at': datetime.utcnow().isoformat()
            }
            redis_client.set(job_id, json.dumps(job_data), ex=3600)

            return jsonify(job_data), 201
        else:
            job_data = {
                'job_id': job_id,
                'type': 'create_student',
                'status': 'failed',
                'error': result.get('error'),
                'completed_at': datetime.utcnow().isoformat()
            }
            redis_client.set(job_id, json.dumps(job_data), ex=3600)
            return jsonify(job_data), 500

    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/users/staff', methods=['POST'])
def create_staff():
    """Create staff account via PowerShell"""
    data = request.json

    required = ['employee_id', 'first_name', 'last_name', 'department', 'role']
    if not all(k in data for k in required):
        return jsonify({'error': f'Missing required fields: {required}'}), 400

    job_id = f"job_{datetime.utcnow().timestamp()}"

    try:
        result = create_staff_account(
            employee_id=data['employee_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            department=data['department'],
            role=data['role']
        )

        if result['success']:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (user_type, employee_id, first_name, last_name, email, username, department, role, is_active)
                VALUES ('staff', %s, %s, %s, %s, %s, %s, %s, TRUE)
                RETURNING id
            """, (
                data['employee_id'],
                data['first_name'],
                data['last_name'],
                result['output'].get('Email'),
                result['output'].get('Username'),
                data['department'],
                data['role']
            ))
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()

            job_data = {
                'job_id': job_id,
                'type': 'create_staff',
                'status': 'completed',
                'user_id': user_id,
                'result': result['output'],
                'completed_at': datetime.utcnow().isoformat()
            }
            redis_client.set(job_id, json.dumps(job_data), ex=3600)
            return jsonify(job_data), 201
        else:
            return jsonify({'error': result.get('error')}), 500

    except Exception as e:
        logger.error(f"Error creating staff: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    job_data = redis_client.get(job_id)
    if not job_data:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(json.loads(job_data)), 200

@app.route('/api/v1/devices', methods=['GET'])
def get_devices():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, device_id, device_name, device_type, compliance_status FROM devices')
    devices = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
        'devices': [
            {
                'id': d[0],
                'device_id': d[1],
                'device_name': d[2],
                'device_type': d[3],
                'compliance_status': d[4]
            } for d in devices
        ]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
