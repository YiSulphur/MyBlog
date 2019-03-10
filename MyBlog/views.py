from flask import flash,redirect,url_for,render_template,request,abort,make_response
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from flask_wtf.csrf import CSRFError
from MyBlog import app,db
from MyBlog.models import User,Post,Comment
from MyBlog.forms import PostForm,CommentForm,LoginForm,SignupForm
from MyBlog.utils import is_safe_url,redirect_back

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page',1,type=int)
    post_total = Post.query.count()
    per_page = 20
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page = per_page)
    posts = pagination.items
    return render_template('index.html',pagination = pagination,posts = posts,post_total=post_total)



@app.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.first()
        if user:
            if username == user.username and user.validate_password(password):
                login_user(user,remember)
                flash('Welcome Back!','info')
                return redirect_back()
            flash('Invalid username or password.','warning')
        else:
            flash('No account.','warning')
    return render_template('login.html',form=form)

@app.route('/signup',methods = ['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username = form.username.data)
        user.set_password(form.password.data)
        remember = form.remember.data
        db.session.add(user)
        db.session.commit()
        login_user(user, remember)
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.','success')
    return redirect_back()

@app.route('/post/<int:post_id>', methods = ['GET','POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(page,per_page=per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = CommentForm()
        if form.validate_on_submit():
            author = current_user
            body = form.body.data
            comment = Comment(author=author,body = body,post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Comment created.','success')
            return redirect(url_for('.show_post',post_id=post.id))
        else:
            return render_template('post.html', post=post, pagination=pagination, comments=comments, form=form)
    return render_template('post.html', post=post, pagination=pagination, comments=comments)

@app.route('/post/new',methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        author = current_user
        title = form.title.data
        body = form.body.data
        post = Post(author=author,title = title, body=body)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('.show_post',post_id=post.id))
    return render_template('new_post.html',form=form)



@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('400.html', description=e.description), 400

@app.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in app.config['MYBLOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme',theme_name,max_age=30*24*60*60)
    return response
