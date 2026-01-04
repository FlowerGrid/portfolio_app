from . import main_bp
from flask import render_template, abort, redirect, url_for, jsonify, Blueprint
from flask_ckeditor import CKEditor
from app.db_helpers import get_joined_project_from_db, get_active_projects, get_active_blog_posts, get_single_blog_post_by_slug # Removed - seed_categories, get_all_categories


@main_bp.route('/')
def index():
    import os
    return render_template('main/index.html')


@main_bp.route('/merch-store')
def merch():
    return render_template('main/merch.html')


@main_bp.route('/projects')
def projects():
    active_projects = get_active_projects()
    data = {
        'type': 'Project'
    }
    return render_template('main/show-projects-blogs.html', objects=active_projects, data=data)


@main_bp.route('/projects/<slug>')
def project(slug):
    project = get_joined_project_from_db('slug', slug)
    if not project or not project.is_active:
        abort(404)
    return render_template('main/project.html', project=project)


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
    if not post or not post.is_active:
        abort(404)
    return render_template('main/blog-post.html', post=post)


@main_bp.route('/dough-calculator')
def do_calc():
    return render_template('main/calculator.html')


@main_bp.route('/blog')
def blog():
    active_projects = get_active_projects()
    data = {
        'type': 'Blog'
    }
    return render_template('main/show-projects-blogs.html', objects=active_projects, data=data)