"""
Sentilytics — Application Entry Point
Run this file to start the Flask development server.

Usage:
    python run.py
"""

from app.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
