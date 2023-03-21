# Open AI powered chatbot for your internal confluence docs

## Steps to Run:

Install `python3` and `pip3`

Then run following commands:
```python
# Create virtual environment with python3
pip3 install virtualenv
virtualenv -p python3 venv

# Activate the virtual environment
source venv/bin/activate

# Install all the required dependencies
pip install -r requirements.txt

# Copy sample config and the update configs accordingly
cp config.env.sample config.env

# Populate environment variables from config
source config.env

# Save your internal confluence docs to pdf [Remove any secret doc if present]
python bot/confluence.py

# Start the app
python bot/app.py
```