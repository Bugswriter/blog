import os
import glob
import markdown
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to convert markdown to HTML and extract metadata
def parse_markdown(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        # Find index of YAML front matter end delimiter (---)
        end_index = lines.index('---\n', 1)
        metadata_lines = lines[1:end_index]
        metadata = yaml.safe_load(''.join(metadata_lines))
        # Extract content excluding YAML front matter
        content = ''.join(lines[end_index+1:])
        html_content = markdown.markdown(content)
    return metadata, html_content

def read_md_files(directory):
    """Reads all .md files from the given directory."""
    markdown_files = glob.glob(os.path.join(directory, '*.md'))
    blog_contents = []
    for file_path in markdown_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Convert markdown content to plain text
            html_content = markdown.markdown(content)
            plain_text_content = ''.join(html_content.split('\n'))
            blog_contents.append(plain_text_content)
    return blog_contents

def generate_recommendations(directory, target_blog_file, num_recommendations=3):
    """Generates recommendations for a target blog."""
    blog_contents = read_md_files(directory)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(blog_contents)

    target_blog_index = None
    for i, file_path in enumerate(glob.glob(os.path.join(directory, '*.md'))):
        if os.path.basename(file_path) == target_blog_file:
            target_blog_index = i
            break

    if target_blog_index is None:
        print("Target blog file not found.")
        return []

    similarities = cosine_similarity(tfidf_matrix[target_blog_index], tfidf_matrix)
    similar_blogs_indices = similarities.argsort()[0][-num_recommendations-1:-1][::-1]

    recommended_blogs = []
    for index in similar_blogs_indices:
        file_path = glob.glob(os.path.join(directory, '*.md'))[index]
        metadata, _ = parse_markdown(file_path)
        _slug = file_path.split('/')[-1]
        recommended_blogs.append({
            'title': metadata['title'],
            'date': metadata['date'],
            'slug': os.path.splitext(_slug)[0]
        })

    return recommended_blogs
