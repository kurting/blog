import os
from app import create_app, db
from app.models import User, Post, Category
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app('default')
app.debug = True

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Category=Category)

#add command to script
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)

    live_server.watch('**/*.*')
    live_server.serve(open_url=False)


if __name__ == '__main__':
    manager.run()