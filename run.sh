# Create folders if they do not exist

if [ ! -d uploads ]; then
  mkdir uploads
fi

if [ ! -d projects ]; then
  mkdir projects
fi

if [ ! -d jsons ]; then
  mkdir jsons
fi

# open the browser to http://localhost:5001

if which xdg-open > /dev/null; then
  xdg-open 'http://localhost:5001/'
else
  echo "Could not detect the web browser to use."
fi

# If the virtual environment exists activate it,
# run the server

if [ -d venv ]; then
  echo " *** venv found *** "
  source venv/bin/activate
  echo " *** Running the server *** "
  python server.py
fi

# If the virtual environment doesn't exist create it,
# install all of the dependencies,
# run the server

if [ ! -d venv ]; then
  echo " *** Setting up virtual environment *** "
  echo " *** This can take a while, please be patient *** "
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  echo " *** Running the server *** "
  python server.py
fi
