from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("budget_requests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create a Blueprint for budget request routes
budget_bp = Blueprint('budget', __name__, url_prefix='/api/budget')

# Mock database (in a real project, you'd use a proper database)
budget_requests = []

# Budget request statuses
STATUS_PENDING = 'pending'
STATUS_APPROVED = 'approved'
STATUS_REJECTED = 'rejected'


# Create Flask application
def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Get configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(budget_bp)

    return app


# Helper functions
def generate_request_id():
    """Generate a unique ID for budget requests"""
    return str(uuid.uuid4())


def validate_budget_data(data):
    """Validate the budget request data"""
    errors = []

    if not data:
        errors.append("No data provided")
        return errors

    # Check required fields
    required_fields = ['amount', 'description', 'department', 'requester']
    for field in required_fields:
        if field not in data:
            errors.append(f"Field '{field}' is required")

    # Validate amount
    if 'amount' in data:
        try:
            amount = float(data['amount'])
            if amount <= 0:
                errors.append("Amount must be greater than zero")
        except ValueError:
            errors.append("Amount must be a valid number")

    # Validate description
    if 'description' in data and len(data['description'].strip()) == 0:
        errors.append("Description cannot be empty")

    return errors


# Budget request routes
@budget_bp.route('/request', methods=['POST'])
def create_budget_request():
    """Create a new budget request"""
    try:
        data = request.get_json()

        # Validate input data
        errors = validate_budget_data(data)
        if errors:
            return jsonify({'errors': errors}), 400

        # Create new budget request
        current_time = datetime.now().isoformat()
        budget_request = {
            'id': generate_request_id(),
            'amount': float(data['amount']),
            'description': data['description'],
            'department': data['department'],
            'requester': data['requester'],
            'category': data.get('category', 'Uncategorized'),
            'priority': data.get('priority', 'Medium'),
            'justification': data.get('justification', ''),
            'attachments': data.get('attachments', []),
            'status': STATUS_PENDING,
            'created_at': current_time,
            'updated_at': current_time,
            'comments': []
        }

        budget_requests.append(budget_request)
        logger.info(f"Budget request created: {budget_request['id']}")
        return jsonify({
            'message': 'Budget request created successfully',
            'data': budget_request
        }), 201

    except Exception as e:
        logger.error(f"Error creating budget request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@budget_bp.route('/requests', methods=['GET'])
def get_budget_requests():
    """Get all budget requests with optional filtering"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        department = request.args.get('department')
        requester = request.args.get('requester')

        # Filter budget requests
        filtered_requests = budget_requests

        if status:
            filtered_requests = [req for req in filtered_requests if req['status'] == status]

        if department:
            filtered_requests = [req for req in filtered_requests if req['department'] == department]

        if requester:
            filtered_requests = [req for req in filtered_requests if req['requester'] == requester]

        return jsonify({'data': filtered_requests}), 200

    except Exception as e:
        logger.error(f"Error retrieving budget requests: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@budget_bp.route('/request/<string:request_id>', methods=['GET'])
def get_budget_request(request_id):
    """Get a specific budget request by ID"""
    try:
        # Find the budget request
        budget_request = next((req for req in budget_requests if req['id'] == request_id), None)

        if not budget_request:
            return jsonify({'error': 'Budget request not found'}), 404

        return jsonify({'data': budget_request}), 200

    except Exception as e:
        logger.error(f"Error retrieving budget request {request_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@budget_bp.route('/request/<string:request_id>', methods=['PUT'])
def update_budget_request(request_id):
    """Update a budget request"""
    try:
        data = request.get_json()

        # Find the budget request
        budget_request = next((req for req in budget_requests if req['id'] == request_id), None)

        if not budget_request:
            return jsonify({'error': 'Budget request not found'}), 404

        # Update only allowed fields
        allowed_updates = [
            'description', 'amount', 'category', 'priority',
            'justification', 'attachments'
        ]

        for field in allowed_updates:
            if field in data:
                if field == 'amount':
                    try:
                        budget_request[field] = float(data[field])
                    except ValueError:
                        return jsonify({'error': 'Amount must be a valid number'}), 400
                else:
                    budget_request[field] = data[field]

        # Update the timestamp
        budget_request['updated_at'] = datetime.now().isoformat()

        logger.info(f"Budget request updated: {request_id}")
        return jsonify({
            'message': 'Budget request updated successfully',
            'data': budget_request
        }), 200

    except Exception as e:
        logger.error(f"Error updating budget request {request_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@budget_bp.route('/request/<string:request_id>/status', methods=['PUT'])
def update_budget_request_status(request_id):
    """Update the status of a budget request (approve/reject)"""
    try:
        data = request.get_json()

        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400

        status = data['status']
        if status not in [STATUS_APPROVED, STATUS_REJECTED]:
            return jsonify({'error': 'Invalid status. Must be "approved" or "rejected"'}), 400

        # Find the budget request
        budget_request = next((req for req in budget_requests if req['id'] == request_id), None)

        if not budget_request:
            return jsonify({'error': 'Budget request not found'}), 404

        # Update status
        budget_request['status'] = status
        budget_request['updated_at'] = datetime.now().isoformat()

        # Add reviewer information if provided
        if 'reviewer' in data:
            budget_request['reviewer'] = data['reviewer']

        # Add review comments if provided
        if 'comment' in data:
            comment = {
                'text': data['comment'],
                'author': data.get('reviewer', 'System'),
                'timestamp': datetime.now().isoformat()
            }
            budget_request['comments'].append(comment)

        logger.info(f"Budget request {request_id} status updated to {status}")
        return jsonify({
            'message': f'Budget request {status} successfully',
            'data': budget_request
        }), 200

    except Exception as e:
        logger.error(f"Error updating status for budget request {request_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@budget_bp.route('/request/<string:request_id>/comment', methods=['POST'])
def add_comment(request_id):
    """Add a comment to a budget request"""
    try:
        data = request.get_json()

        if not data or 'text' not in data or 'author' not in data:
            return jsonify({'error': 'Comment text and author are required'}), 400

        # Find the budget request
        budget_request = next((req for req in budget_requests if req['id'] == request_id), None)

        if not budget_request:
            return jsonify({'error': 'Budget request not found'}), 404

        # Create and add the comment
        comment = {
            'text': data['text'],
            'author': data['author'],
            'timestamp': datetime.now().isoformat()
        }

        budget_request['comments'].append(comment)
        budget_request['updated_at'] = datetime.now().isoformat()

        logger.info(f"Comment added to budget request {request_id}")
        return jsonify({
            'message': 'Comment added successfully',
            'data': comment
        }), 201

    except Exception as e:
        logger.error(f"Error adding comment to budget request {request_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@budget_bp.route('/stats', methods=['GET'])
def get_budget_stats():
    """Get statistics about budget requests"""
    try:
        total_requests = len(budget_requests)
        total_amount = sum(req['amount'] for req in budget_requests)
        pending_requests = sum(1 for req in budget_requests if req['status'] == STATUS_PENDING)
        approved_requests = sum(1 for req in budget_requests if req['status'] == STATUS_APPROVED)
        rejected_requests = sum(1 for req in budget_requests if req['status'] == STATUS_REJECTED)

        approved_amount = sum(req['amount'] for req in budget_requests if req['status'] == STATUS_APPROVED)

        # Group by department
        departments = {}
        for req in budget_requests:
            dept = req['department']
            if dept not in departments:
                departments[dept] = 0
            departments[dept] += req['amount']

        stats = {
            'total_requests': total_requests,
            'total_amount': total_amount,
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'rejected_requests': rejected_requests,
            'approved_amount': approved_amount,
            'departments': departments
        }

        return jsonify({'data': stats}), 200

    except Exception as e:
        logger.error(f"Error generating budget stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
