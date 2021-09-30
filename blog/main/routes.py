from flask import Blueprint, request, render_template
from blog.models import Post
main = Blueprint('main', __name__)


@main.route("/")
def home_page():
    page_number = request.args.get('page',1,type=int) # 1 is the default value
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page_number)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about_page():
    return render_template('about.html', title='About')