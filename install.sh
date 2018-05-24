echo 'Creating virtual environment...'
python3 -m venv env
source env/bin/activate
echo 'Installing pre-requirements'
pip3 install -r pre-requirements.txt -q
echo 'Installing requirements'
pip3 install -r requirements.txt -q
echo "Installation succeed!"
