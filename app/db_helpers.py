import bleach
from bs4 import BeautifulSoup
from flask import request, session, flash, current_app
from google.cloud import storage
import html, json
import io
from .logger import logger
import os
from PIL import Image
import pillow_heif
import re
from sqlalchemy.orm import joinedload
from .db import db_session
from werkzeug.utils import secure_filename
from .models import Base, Project, User, BlogPost, Tag # Removed Category


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'static', 'uploads'))

pillow_heif.register_heif_opener()

MAX_SIZE = 1024


def gather_form_data_unified(model_cls, form, rel_attr_name):

    title = form.title.data.strip()
    slug = secure_filename(slugify(title))
    # cat_id = form.category.data
    blurb = sanitize_html(form.blurb.data.strip())

    model_cls_str = model_cls.__tablename__ # String of table's name
    logger.info('model class string: ', model_cls_str)

    project_exclusives = {}
    try:
        project_exclusives['ingredients'] = sanitize_html(form.ingredients.data.strip())
        project_exclusives['steps'] = sanitize_html(form.steps.data.strip())
    except AttributeError:
        pass

    image_file = form.photo.data

    tags_list = json.loads(form.tags.data)

    # Add plain text blurb
    blurb_plaintext = BeautifulSoup(blurb, 'html.parser').get_text()

    obj_id = form.id.data

    if obj_id:
        # Delete old photo up here
        model_obj = db_session.query(model_cls).filter_by(id=obj_id).first()
        model_obj.title = title
        model_obj.slug = slug
        # project.category_id = cat_id
        model_obj.blurb = blurb

        if project_exclusives:
            for key, value in project_exclusives.items():
                setattr(model_obj, key, value)

        model_obj.blurb_plaintext = blurb_plaintext

        model_cls_str = model_cls.__tablename__ # String of table's name

        if image_file and image_file.filename != '':
            model_obj.image_url = image_helper(model_cls_str, image_file, slug)

        tags_handler(model_obj, tags_list, rel_attr_name)

    else:
        model_obj = model_cls(
            title=title,
            slug=slug,
            blurb=blurb,
            # image_url=None,
            blurb_plaintext=blurb_plaintext) # Removed category_id=cat_id,
        
        if project_exclusives:
            for key, value in project_exclusives.items():
                setattr(model_obj, key, value)

        if tags_list:
            tags_handler(model_obj, tags_list, rel_attr_name)

        if image_file and image_file.filename != '':
            model_obj.image_url = image_helper(model_cls_str, image_file, slug)


        db_session.add(model_obj)
    db_session.commit()


def normalize_tag_name(tag_name):
    tag_name = re.sub(r'_+', ' ', tag_name)
    tag_name = tag_name.strip().lower()
    tag_name = re.sub(r'\s+', '_', tag_name)
    tag_name = re.sub(r'[^a-zA-Z0-9_]', '', tag_name)

    return tag_name


def tags_handler(model_obj, tags_list, relation):
    final_tags_list = []

    for tag_name in tags_list:
        normed_tag_name = normalize_tag_name(tag_name)
        # skip strings that can't normalize or are empty
        if not normed_tag_name:
            continue

        tag_obj = db_session.query(Tag).filter_by(name=normed_tag_name).first()
        if not tag_obj:
            tag_obj = Tag(name=normed_tag_name)
            db_session.add(tag_obj)

        final_tags_list.append(tag_obj)

    setattr(model_obj, relation, final_tags_list)


def image_helper(model_cls_str, image_file, slug):
    try:
        with Image.open(image_file) as img:
            img.verify()

            # Reset file pointer so Pillow can read the image again
            image_file.seek(0)

            organized_slug = f'{model_cls_str}/{slug}'
            img_public_url = current_app.extensions['image_storage'].save(image_file, organized_slug)

        return img_public_url
    
    except Exception as e:
        # Log this
        logger.exception("Image Upload Error")
        return None


def get_joined_project_from_db(key, value):
    project = (
        db_session.query(Project)
        .options(
            joinedload(Project.tags_in_project)
        )
        .filter(getattr(Project, key) == value).first()
    )

    return project


def get_all_projects_joined():
    all_projects = (
        db_session.query(Project)
        .options(
            joinedload(Project.tags_in_project)
        )
        .all()
    )
    return all_projects


def get_single_project_by_id(id):
    return db_session.query(Project).filter_by(id=id).first()


def get_all_projects():
    return db_session.query(Project).all()


def get_all_blog_posts():
    return db_session.query(BlogPost).all()


def get_single_blog_post_by_id(id):
    return db_session.query(BlogPost).filter_by(id=id).first()


def get_single_blog_post_by_slug(slug):
    return db_session.query(BlogPost).filter_by(slug=slug).first()


def get_active_blog_posts():
    return db_session.query(BlogPost).filter_by(is_active=True)


def get_active_projects():
    return db_session.query(Project).filter_by(is_active=True)


# def get_all_categories():
#     return db_session.query(Category).all()


def slugify(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


def toggle_active_status_in_db(orm_object):
    orm_object.is_active = not orm_object.is_active
    db_session.commit()


def query_user(username, password):
    user = db_session.query(User).filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        session['user_id'] = user.id
        return True
    return False


def get_user_info(id):
    return db_session.query(User).filter_by(id=id).first()


def get_admin():
    try:
        return db_session.query(User).filter_by(is_admin=True).one_or_none()
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        return None


# Deprecated in favor of tags
# Seed data to db
# def seed_categories():
#     category_names = ['Pizza', 'Dough', 'Sauce']
#     for name in category_names:
#         slug = slugify(name)
#         existing = db_session.query(Category).filter_by(name=name).first()
#         if not existing:
#             category = Category(name=name, slug=slug)
#             db_session.add(category)
#     db_session.commit()
#     print("✅ Categories seeded.")


def update_user(form):
    user = get_user_info(session['user_id'])

    user.username = form.username.data.lower()
    user.email = form.email.data
    user.security_question = form.security_question.data.strip()
    user.set_security_answer(form.answer.data)

    image_file = form.logo_img.data

    model_cls_str = 'users'
    slug = 'user-logo'

    user.logo_img = image_helper(model_cls_str, image_file, slug)

    db_session.commit()


def change_pw(form):
    message = ''
    user = get_user_info(session['user_id'])
    old_pw = form.old_pw.data
    new_pw = form.new_pw.data
    rep_new_pw = form.rep_new_pw.data
    if user.check_password(old_pw):
        if new_pw == rep_new_pw:
            user.set_password(new_pw)
            db_session.commit()
            message = 'Password successfully reset.'
            
            return True, message
        else:
            message = 'New password does not match.'
    else:
        message = 'Incorrect Password.'

    return False, message


def sanitize_html(html_input):
    cleaned = bleach.clean(
        html_input,
        tags=['p', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'br'],
        attributes={'a': ['href']}
    )

    return cleaned