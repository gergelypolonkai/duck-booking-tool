#!/usr/bin/env python3

import connexion
from flask_login import LoginManager

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml',
            arguments={
                'title': 'Rubber Duck Booking Tool'
            })

login_manager = LoginManager()
#login_manager.init_app(app)

if __name__ == '__main__':
    app.run(port=8080)
