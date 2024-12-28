from flask import Flask, render_template
import requests
from flask import request
from smtplib import SMTP


API = 'https://api.npoint.io/d6cb0d9ec8c30f004364'
MY_EMAIL = "Your email"
MY_PASSWORD = "app password of email"  # check description

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', all_posts=all_posts)

@app.route('/post/<int:index>')
def get_post(index):
    return render_template('post.html', post=all_posts[index-1])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':
        form_data = request.form
        is_sent = send_mail(form_data)
        return render_template('contact.html', msg_sent=is_sent)

def send_mail(form):
    email_message = f"Subject:Blog's New Message\n\nName: {form['name']}\nEmail: {form['email']}\nPhone: {form['phone']}\nMessage:{form['message']}"
    try:
        with SMTP(host='smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(MY_EMAIL, MY_EMAIL, email_message)
            print(f'message sent {email_message}')
            return True
    except:
        print('message not sent.')
        return False

if __name__ == '__main__':
    all_posts = requests.get(url=API).json()
    app.run(debug=True, port=5002)
