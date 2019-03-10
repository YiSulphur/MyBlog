import click
import random
from MyBlog import app,db
try:
    from MyBlog.models import User,Post,Comment
except:
    pass

@app.cli.command()
@click.option('--count',default = 40,help='Quantity of messages')
def forge(count):
    from faker import Faker
    db.drop_all()
    db.create_all()

    fake = Faker()
    click.echo("Working...")
    admin = User(username = 'liu')
    admin.set_password('123456')
    db.session.add(admin)
    for i in range(count):
        post = Post(
            title  = fake.sentence(),
            body = fake.text(2000),
            timestamp = fake.date_time_this_year(),
            author=admin
        )
        db.session.add(post)
    for i in range(count):
        comment = Comment(
            body=fake.text(20),
            timestamp=fake.date_time_this_year(),
            author = admin,
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    db.session.commit()
    click.echo('Created %d fake posts.' % count)
