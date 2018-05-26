echo 'Initialize python virutal environment'
python3 -m venv env
echo 'Installing requirements'
./env/bin/pip3 install -r requirements.txt -q
echo "Installation succeed!"
