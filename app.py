from back.web import app
import os

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
