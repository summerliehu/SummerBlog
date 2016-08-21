from . import mail
from flask_mail import Message
from flask import render_template, current_app

#发送邮件，参数：收件人，主题，模板位置和名称，其它键值参数（这些参数会被传递至邮件模板
#用来生成邮件内容）
def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject, \
		sender = app.config['FLASKY_MAIL_SENDER'], recipients = [to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)
