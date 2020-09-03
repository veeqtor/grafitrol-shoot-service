"""API Entry Module"""

import os
from main import create_app


# gets the current environment and creates a flask app instance
ENV = os.getenv('FLASK_ENV')
app = create_app(ENV)

if __name__ == '__main__':
    app.run()
