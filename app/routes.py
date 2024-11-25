from flask import render_template, request, redirect, session, url_for, flash
from app import app, db  # Import the app and database instance
from app.models import User  # Import the User model
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from functools import wraps
from app.models import MedicineList
from flask import request, jsonify
from flask import flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/onboarding')
def onboarding():
    if 'user_id' in session:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    return render_template('onboarding.html')  # Otherwise, show onboarding

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(email=email).first()
        
        # Check if the user exists and the password is correct
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

        # Store session data if the user is authenticated
        session['id'] = user.id
        session['email'] = user.email
        session['user_type'] = user.user_type  # Store user_type in session for future checks

        # Redirect based on user_type
        if user.user_type == 'admin':
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            user_type = request.form['user_type']

            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return render_template('signup.html')

            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists!', 'danger')
                return render_template('signup.html')

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create and add the new user
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,  # Store the hashed password
                user_type=user_type
            )
            db.session.add(new_user)
            db.session.commit()

            flash('User created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            app.logger.error(f"Error during signup: {e}")
            flash('An error occurred during signup. Please try again later.', 'danger')
            return render_template('signup.html')

    return render_template('signup.html')

@app.route('/home')
@login_required
def home():
    app.logger.debug(f"Session data: {session}")
    if 'id' not in session:  # Check if user is logged in
        flash('Please log in first', 'error')
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    # Clear user session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/account')
def account():
    if 'id' not in session:  # Ensure the user is logged in
        flash('Please log in first', 'error')
        return redirect(url_for('login'))
    return render_template('account.html')  # Render the account page

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'id' not in session or session.get('user_type') != 'admin':
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Process the form submission
        try:
            name = request.form['name']
            description = request.form['description']
            strength = request.form['strength']
            category = request.form['category']
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])

            # Add the new medicine to the database
            new_medicine = MedicineList(
                name=name,
                description=description,
                strength=strength,
                category=category,
                price=price,
                quantity=quantity
            )
            db.session.add(new_medicine)
            db.session.commit()
            flash('Medicine added successfully!', 'success')

        except Exception as e:
            app.logger.error(f"Error adding medicine: {e}")
            flash('An error occurred while adding the medicine.', 'danger')

        return redirect(url_for('admin'))  # Redirect to the admin page after form submission

    # Fetch the list of medicines to display in the table
    medicines = MedicineList.query.all()
    return render_template('admin.html', medicines=medicines)



@app.route('/update_medicine/<int:id>', methods=['POST'])
def update_medicine(id):
    data = request.get_json()
    try:
        # Fetch the medicine from the database
        medicine = MedicineList.query.get(id)
        if not medicine:
            return jsonify({'error': 'Medicine not found'}), 404

        # Update the medicine fields
        medicine.name = data.get('name', medicine.name)
        medicine.description = data.get('description', medicine.description)
        medicine.strength = data.get('strength', medicine.strength)
        medicine.category = data.get('category', medicine.category)
        medicine.price = float(data.get('price', medicine.price))
        medicine.quantity = int(data.get('quantity', medicine.quantity))

        # Save changes to the database
        db.session.commit()
        return jsonify({'success': 'Medicine updated successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error updating medicine: {e}")
        return jsonify({'error': 'An error occurred while updating the medicine'}), 500


@app.route('/delete_medicine/<int:id>', methods=['GET'])
def delete_medicine(id):
    if 'id' not in session or session.get('user_type') != 'admin':
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    
    try:
        # Fetch and delete medicine from database
        medicine = MedicineList.query.get_or_404(id)
        db.session.delete(medicine)
        db.session.commit()
        flash('Medicine deleted successfully!', 'success')
    except Exception as e:
        app.logger.error(f"Error deleting medicine: {e}")
        flash('An error occurred while deleting the medicine.', 'danger')
    
    return redirect(url_for('admin'))



