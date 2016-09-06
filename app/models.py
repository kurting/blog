# --*-- coding: utf-8 --*--
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from markdown import markdown
import bleach

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('passoword is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    count = db.Column(db.Integer,default=1)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return '<Category %r>' %self.tag



# 文章提交数据模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    summary = db.Column(db.Text)
    summary_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 时间戳
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # transform html to markdown
    @staticmethod
    def on_changed_body(target, value, old, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote', 'em', 'i',
                        'strong', 'li', 'ol', 'pre', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True)
        )

    @staticmethod
    def on_changed_summary(target, value, old, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote', 'em', 'i',
                        'strong', 'li', 'ol', 'pre', 'ul', 'h1', 'h2', 'h3', 'p']
        target.summary_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True)
        )

    def __init__(self, title, body, summary, category):
        self.title = title
        self.body = body
        self.summary = summary
        self.category = category

    def __repr__(self):
        return '<Post.title %r>' %self.title

db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.summary, 'set', Post.on_changed_summary)

