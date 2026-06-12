from flask import Flask, url_for, flash, redirect, request, render_template, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from config import Config
from models import db, User, RGBText
from forms import RegistrationForm, LoginForm, RGBTextForm

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    def run_migrations(app):
        """Automatically add any missing columns to the database without data loss."""
        import sqlite3, os
        db_path = os.path.join(app.instance_path, 'site.db')
        if not os.path.exists(db_path):
            return  # db.create_all() will handle it
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(rgb_text)")
        existing_cols = {row[1] for row in cursor.fetchall()}
        new_cols = {
            'color_1': "TEXT DEFAULT '#ff0000'",
            'color_2': "TEXT DEFAULT '#00ff00'",
            'color_3': "TEXT DEFAULT '#0000ff'",
            'font_weight': "INTEGER DEFAULT 700",
            'letter_spacing': "INTEGER DEFAULT 0",
            'shadow_color': "TEXT DEFAULT '#ffffff'",
        }
        for col, col_def in new_cols.items():
            if col not in existing_cols:
                cursor.execute(f"ALTER TABLE rgb_text ADD COLUMN {col} {col_def}")
        conn.commit()
        conn.close()


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Routes
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', title='Login', form=form)

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route("/dashboard", methods=['GET', 'POST'])
    @login_required
    def dashboard():
        form = RGBTextForm()
        if form.validate_on_submit():
            rgb_text = RGBText(
                text_content=form.text_content.data,
                font_size=form.font_size.data,
                animation_speed=form.animation_speed.data,
                glow_intensity=form.glow_intensity.data,
                color_1=form.color_1.data,
                color_2=form.color_2.data,
                color_3=form.color_3.data,
                font_weight=form.font_weight.data,
                letter_spacing=form.letter_spacing.data,
                shadow_color=form.shadow_color.data,
                author=current_user
            )
            db.session.add(rgb_text)
            db.session.commit()
            flash('Your RGB style has been saved!', 'success')
            return redirect(url_for('dashboard'))
        
        user_styles = RGBText.query.filter_by(author=current_user).order_by(RGBText.created_at.desc()).all()
        return render_template('dashboard.html', title='Dashboard', form=form, user_styles=user_styles)

    @app.route("/style/delete/<int:style_id>", methods=['POST'])
    @login_required
    def delete_style(style_id):
        style = RGBText.query.get_or_404(style_id)
        if style.author != current_user:
            return jsonify({'error': 'Unauthorized'}), 403
        db.session.delete(style)
        db.session.commit()
        flash('Style deleted.', 'success')
        return redirect(url_for('dashboard'))

    with app.app_context():
        db.create_all()
        run_migrations(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
