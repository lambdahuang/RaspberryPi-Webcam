echo 'Initialize python virutal environment'
python3 -m venv env
echo 'Installing pre-requirements'
./env/bin/pip3 install -r pre-requirements.txt -q
echo 'Installing requirements'
./env/bin/pip3 install -r requirements.txt -q
echo "Installation succeed!"
