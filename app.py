from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session
DATA_FILE = 'data.xlsx'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Full Name", "Preferred Name", "Father Name", "Mother Name",
        "Phone", "Email", "Address", "Aadhar", "Emergency Name",
        "Emergency Contact", "Job Title", "Team", "Start Date",
        "Employment Type", "Manager", "Work Location", "Bank Account",
        "Bank Holder", "PAN", "Device", "Software Needs",
        "Additional Needs", "Account Setup", "Handbook",
        "NDA", "Confidentiality", "Conduct", "Data Policy",
        "Additional Info", "Signature", "Today Date"
    ])
    df.to_excel(DATA_FILE, index=False)
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('success'))
    return render_template('form.html')
@app.route('/submit', methods=['POST'])
def submit():
    df = pd.read_excel(DATA_FILE)
    new_data = {
        "Full Name": request.form.get("full_name"),
        "Preferred Name": request.form.get("preferred_name"),
        "Father Name": request.form.get("father_name"),
        "Mother Name": request.form.get("mother_name"),
        "Phone": request.form.get("phone_number"),
        "Email": request.form.get("email"),
        "Address": request.form.get("address"),
        "Aadhar": request.form.get("aadhar_number"),
        "Emergency Name": request.form.get("emergency_contact_name"),
        "Emergency Contact": request.form.get("emergency_contact_number"),
        "Job Title": request.form.get("job_title"),
        "Team": request.form.get("team"),
        "Start Date": request.form.get("start_date"),
        "Employment Type": request.form.get("employment_type"),
        "Manager": request.form.get("manager"),
        "Work Location": request.form.get("work_location"),
        "Bank Account": request.form.get("bank_account"),
        "Bank Holder": request.form.get("bank_holder"),
        "PAN": request.form.get("pan_number"),
        "Device": request.form.get("device_type"),
        "Software Needs": request.form.get("software_needs"),
        "Additional Needs": request.form.get("additional_needs"),
        "Account Setup": request.form.get("account_setup", "No"),
        "Handbook": request.form.get("handbook", "No"),
        "NDA": request.form.get("nda", "No"),
        "Confidentiality": request.form.get("confidentiality", "No"),
        "Conduct": request.form.get("code_of_conduct", "No"),
        "Data Policy": request.form.get("data_protection", "No"),
        "Additional Info": request.form.get("additional_info"),
        "Signature": request.form.get("signature"),
        "Today Date": request.form.get("today_date")
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False)
    return redirect(url_for('success'))
@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
        else:
            return "Invalid credentials. Try again."
    if not session.get('admin'):
        return '''
        <h2>Admin Login</h2>
        <form method="POST">
            <label>Username:</label><input type="text" name="username"><br>
            <label>Password:</label><input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''
    try:
        df = pd.read_excel(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame()
    return render_template('admin.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin'))
if __name__ == '__main__':
    app.run(debug=True, port=81)