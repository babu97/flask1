import os
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
basedir= os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kipkulei'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] =True
app.config['MAIL_USERNAME'] = 'benkaimugul@gmail.com'
app.config['MAIL_PASSWORD'] = 'Kipkulei@12'


app.app_context().push()

boostrap = Bootstrap(app)
moment  = Moment(app)
mail =Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


@app.route('/user/<name>')
def user(name):
 return render_template ('user.html', name = name)
@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500
@app.route('/', methods = ['GET','POST'])
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    thread = Thread(target=send_async_email, args=(app, msg))
    thread.start()


def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('user.html', form=form, name=session.get('name'),
                           known=session.get('known', False))
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <benkaimugul@gmail.com>'


 
class NameForm(FlaskForm):
 name = StringField('What is your name ? ', validators=[DataRequired()])
 submit = SubmitField('submit')


class Role(db.Model):
  __tablename__= 'roles'
  id = db.Column(db.Integer, primary_key= True)
  name = db.Column(db.String(64), unique = True)
  users = db.relationship('User',backref = 'role', lazy = 'dynamic')
@app.shell_context_processor
def make_shell_context():
  return dict(db=db,User=User, Role=Role)



  def __repr__(self):
   return '<role %r>'%self.name
  
class User(db.Model):
   __tablename = 'users'
   id = db.Column(db.Integer,primary_key = True)
   username = db.Column(db.String(64), unique = True, index = True)
   role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

   def __repr__(self):
    return '<User %r>'% self.username




if __name__ == '__main__':
 
 app.run(debug=True)


