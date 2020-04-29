from flask_script import Manager

import config
from app import create_app

app = create_app(config)

manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
