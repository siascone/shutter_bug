# Setup and run commands
# 1. execute . /setup.sh in active venv to setup flask environment variables
# 2. execute flask --app app.py run to start server

echo "Setting up flask env variables..."
sleep 0.2

export FLASK_APP=app.py
echo "Set FLASK_APP as app.py"
sleep 0.2

export FLASK_RUN_PORT=3308
echo "Set server port as 5000"
sleep 0.2

export FLASK_DEBUG=1
export FLASK_ENV=development
echo "Set development environment"
sleep 0.2

export PYTHONPATH='.'
echo "Set python path as root directory"
sleep 0.2

echo "Setup complete!"