import os
from flask import Flask, render_template
from utils.suggestor import generate_recommendations, parse_markdown

app = Flask(__name__)

# Directory where markdown blogs are stored
BLOGS_DIRECTORY = 'blogs'

# Route to serve individual blog posts
@app.route('/blog/<blog_name>')
def blog(blog_name):
    blog_path = os.path.join(BLOGS_DIRECTORY, f'{blog_name}.md')
    similar_blogs = generate_recommendations(BLOGS_DIRECTORY, blog_name + '.md')
	
    if os.path.exists(blog_path):
        metadata, html_content = parse_markdown(blog_path)
        return render_template(
			'blog.html', metadata=metadata, content=html_content, suggestions=similar_blogs)
    else:
        return 'Blog not found', 404

@app.route('/')
def index():
    blogs = []
    for file_name in os.listdir(BLOGS_DIRECTORY):
        if file_name.endswith('.md'):
            blog_path = os.path.join(BLOGS_DIRECTORY, file_name)
            metadata, _ = parse_markdown(blog_path)
            metadata['slug'] = os.path.splitext(file_name)[0]  # Add slug field
            blogs.append(metadata)
    return render_template('index.html', blogs=blogs)

if __name__ == '__main__':
    app.run(debug=True)
