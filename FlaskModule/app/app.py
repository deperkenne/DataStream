from config1 import create_app
from  config_tweeter import create_app_tweeter

app = create_app()
app_tweeter = create_app_tweeter()

if __name__ == '__main__':
    # run flask application on port 5002
    #app.run(debug=True, host="0.0.0.0", port=5002)
    # run flask_tweeter application on port 5003
    app_tweeter.run(debug=True, host="0.0.0.0", port=5003)

