"""
EduOps Command Center - API Gateway
Flask REST API for identity and device automation
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'eduops'),
        user=os.getenv('POSTGRES_USER', 'eduops_user'),
        password=os.getenv('POSTGRES_PASSWORD', 'changeme123')
    )

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'api-gateway'
    }), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Get all users"""
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
    """Create student account"""
    data = request.json

    # Queue job in Redis
    job_id = f"job_{datetime.utcnow().timestamp()}"
    job_data = {
        'type': 'create_student',
        'data': data,
        'status': 'queued',
        'created_at': datetime.utcnow().isoformat()
    }
    redis_client.set(job_id, json.dumps(job_data))

    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'message': 'Student account creation queued'
    }), 202

@app.route('/api/v1/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    job_data = redis_client.get(job_id)
    if not job_data:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify(json.loads(job_data)), 200

@app.route('/api/v1/devices', methods=['GET'])
def get_devices():
    """Get all devices"""
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
