from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from scapy.all import sniff, IP
from collections import defaultdict
from datetime import datetime
from geo import get_geo_info
import threading
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a strong key in production

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store
users = {'admin': {'password': 'admin123'}}

# In-memory data store for packet information
ip_data = defaultdict(lambda: {"count": 0, "last_seen": "", "location": "", "org": ""})
suspicious_ips = set()
SUSPICIOUS_THRESHOLD = 50  # Customize threshold for detection

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

# def get_ip_info(ip):
#     """Fetch geographical information for the IP using ipinfo.io"""
#     try:
#         response = requests.get(f"https://ipinfo.io/{ip}/json").json()
#         return response.get("city", ""), response.get("org", "")
#     except Exception:
#         return "", ""

def process_packet(packet):
    if IP in packet:
        ip = packet[IP].src
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_data[ip]["count"] += 1
        ip_data[ip]["last_seen"] = now

        if not ip_data[ip]["location"]:  # Only fetch geo info once
            location, org = get_geo_info(ip)
            ip_data[ip]["location"] = location
            ip_data[ip]["org"] = org
            print(f"[{ip}] Location: {location} | Org: {org}")  # Debug print

        if ip_data[ip]["count"] > SUSPICIOUS_THRESHOLD:
            suspicious_ips.add(ip)


def start_sniffing():
    """Start sniffing network packets in a background thread."""
    sniff(prn=process_packet, store=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            login_user(User(username))
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = {'password': password}
            return redirect(url_for('login'))
        return render_template('signup.html', error='User already exists')
    return render_template('signup.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    # Your logic here for forgot password page
    return render_template('forgot.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # This will log the user out
    return redirect(url_for('login'))  # Redirects to login page after logout

@app.route('/')
@login_required
def home():
    return render_template('index.html')  # Home page after login

@app.route('/suspicious')
@login_required
def suspicious():
    return render_template('suspicious.html')

@app.route('/chart')
@login_required
def chart():
    return render_template('chart.html')

@app.route('/table')
@login_required
def table():
    return render_template('table.html')

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/alerts')
@login_required
def alerts():
    """API endpoint to get suspicious IPs."""
    return jsonify(list(suspicious_ips))

@app.route('/data')
@login_required
def data():
    """API endpoint to get packet data for each IP."""
    return jsonify(ip_data)

if __name__ == '__main__':
    threading.Thread(target=start_sniffing, daemon=True).start()
    app.run(debug=True)
