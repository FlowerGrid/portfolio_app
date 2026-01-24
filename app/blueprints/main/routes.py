from . import main_bp
from flask import render_template, abort, redirect, url_for, jsonify, Blueprint
from flask_ckeditor import CKEditor
from app.db_helpers import get_joined_project_from_db, get_active_projects, get_active_blog_posts, get_single_blog_post_by_slug, fetch_content_block_dicts # Removed - seed_categories, get_all_categories


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/merch-store')
def merch():
    return render_template('main/merch.html')


@main_bp.route('/projects')
def projects():
    active_projects = get_active_projects()
    data = {
        'type': 'Portfolio'
    }
    return render_template('main/show-projects-blogs.html', objects=active_projects, data=data)


@main_bp.route('/projects/<slug>')
def project(slug):
    project = get_joined_project_from_db('slug', slug)
    content_blocks = fetch_content_block_dicts(project.__tablename__, project.id)
    if not project or not project.is_active:
        abort(404)
    return render_template('main/content-item.html', project=project, content_blocks=content_blocks, content_type='Portfolio')


@main_bp.route('/blog')
def blog_posts():
    active_posts = get_active_blog_posts()
    data = {
        'type': 'Blog'
    }
    return render_template('main/show-projects-blogs.html', objects=active_posts, data=data)


@main_bp.route('/blog/<slug>')
def show_blog_post(slug):
    post = get_single_blog_post_by_slug(slug)
    content_blocks = fetch_content_block_dicts(post.__tablename__, post.id)
    if not post or not post.is_active:
        abort(404)
    return render_template('main/content-item.html', project=post, content_blocks=content_blocks, content_type='Blog')


@main_bp.route('/resume')
def resume():
    return render_template('main/resume.html')


@main_bp.route('/about-me')
def about():
    return render_template('main/about.html')