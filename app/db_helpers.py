import bleach
from bs4 import BeautifulSoup
from .db import db_session
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
import uuid
from werkzeug.utils import secure_filename
from .models import Base, Project, User, BlogPost, Tag, ContentBlock # Removed Category


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'static', 'uploads'))

pillow_heif.register_heif_opener()

MAX_SIZE = 1024


def gather_form_data_unified(model_cls, form, rel_attr_name):

    try:
        title = form.title.data.strip()
        slug = secure_filename(slugify(title))
        # cat_id = form.category.data
        blurb = sanitize_html(form.blurb.data.strip())
        model_cls_str = model_cls.__tablename__ # String of table's name
        # logger.info('model class string: ', model_cls_str)
        files = request.files # Images from content blocks


        project_exclusives = {}
        try:
            project_exclusives['project_link'] = sanitize_html(form.project_link.data.strip()) or None
            project_exclusives['github_link'] = sanitize_html(form.github_link.data.strip()) or None
        except AttributeError:
            pass

        image_file = form.photo.data

        tags_list = json.loads(form.tags.data)
        content_blocks = json.loads(form.content_blocks.data) # List of dictionaries

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
                model_obj.image_url = image_helper(model_cls_str, image_file, obj_id, 'hero')

            tags_handler(model_obj, tags_list, rel_attr_name)

            content_blocks_handler(model_cls_str, content_blocks, obj_id, files, slug)

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

            db_session.add(model_obj)
            db_session.flush()

            if image_file and image_file.filename != '':
                model_obj.image_url = image_helper(model_cls_str, image_file, model_obj.id, 'hero')

            if content_blocks:
                content_blocks_handler(model_cls_str, content_blocks, model_obj.id, files, slug)
        
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logger.error(f'>>>> Main Exception: Form processing failed for project/blog - {e}')
        flash('Something went wrong. Please try again.', 'error')
        return


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


def content_blocks_handler(content_item_class, content_blocks, parent_id, files, slug):
    # Remove existing blocks
    if parent_id:
        delete_content_blocks(content_item_class, parent_id)

    block_types = ['text', 'image', 'subheading']

    for i, block in enumerate(content_blocks, start=1):
        image_url = None
        sanitized_alt_text = None
        image_uuid = None
        text_content = None

        b_type = block['blockType']

        if b_type not in block_types:
            raise ValueError('bad block type in content block image upload')
        
        if b_type == 'image':
            image_file = files.get(block['imageName']) # The actual file

            if block.get('recycleUuid'):
                image_uuid = sanitize_text_input(block['imageName'])
                _, image_url = image_urls_builder(
                    content_item_class, parent_id, image_uuid
                    )

            if image_file:
                image_uuid = image_uuid or str(uuid.uuid4())
                image_url = image_helper(content_item_class, image_file, parent_id, image_uuid)

            sanitized_alt_text = sanitize_text_input(block.get('altText'), 150)

        if b_type == 'subheading':
            text_content = sanitize_text_input(block.get('textContent'), 70)
        elif b_type == 'text':
            text_content = sanitize_text_input(block.get('textContent'), 750)
            
        content_block_model_object = ContentBlock(
            parent_type = content_item_class,
            parent_id = parent_id,
            block_type=b_type,
            position = i,
            text_content = text_content,
            image_url = image_url,
            image_uuid = image_uuid,
            image_alt_text = sanitized_alt_text
        )

        db_session.add(content_block_model_object)


def fetch_content_blocks(content_item_class, parent_id):
    content_blocks_table = db_session.query(ContentBlock).filter_by(
        parent_type=content_item_class,
        parent_id=parent_id  
    ).order_by(ContentBlock.position).all()

    return content_blocks_table


def fetch_content_block_dicts(content_item_class, parent_id):
    return [cb.to_dict() for cb in fetch_content_blocks(content_item_class, parent_id)]


def delete_content_blocks(content_item_class, parent_id):
    db_session.query(ContentBlock).filter_by(
        parent_type=content_item_class,
        parent_id=parent_id
    ).delete(synchronize_session=False)


def image_urls_builder(content_item_class, content_item_id, image_uuid):
    path = os.path.join(
        content_item_class,
        content_item_id,
        'images',
        f'{image_uuid}.png'
        )
    
    rel_url = os.path.join('/uploads', path)
    full_url = os.path.join(current_app.config['IMAGE_STORAGE_CONTAINER'], path)

    return full_url, rel_url


def image_helper(model_cls_str, image_file, content_item_id, image_uuid):
    try:
        with Image.open(image_file) as img:
            img.verify()

            # Reset file pointer so Pillow can read the image again
            image_file.seek(0)

            img_public_url = current_app.extensions['image_storage'].save(
                image_file, model_cls_str, str(content_item_id), image_uuid
                )

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
    return db_session.query(BlogPost).filter_by(is_active=True).order_by(BlogPost.created_at.desc()).all()


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


def update_user(form):
    user = get_user_info(session['user_id'])

    user.username = form.username.data.lower()
    user.email = form.email.data
    user.security_question = form.security_question.data.strip()
    user.set_security_answer(form.answer.data)

    image_file = form.logo_img.data

    model_cls_str = 'users'
    slug = 'user-logo'

    user.logo_img = image_helper(model_cls_str, image_file, slug, 'logo')

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

def sanitize_text_input(text, limit=None):
    if not text:
        return None
    
    text = text.strip()
    if not text:
        return None
    
    if limit is not None and len(text) > limit:
        text = text[:limit + 1]

    return text