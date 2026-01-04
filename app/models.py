from datetime import datetime
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey, DateTime, Boolean, Text, Table, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

# Association Tables
project_tags = Table(
    'project_tags',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

blog_tags = Table(
    'blog_tags',
    Base.metadata,
    Column('blog_post_id', Integer, ForeignKey('blog_posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

    projects_with_tag = relationship('Project', secondary=project_tags, back_populates='tags_in_project')
    blog_posts_with_tag = relationship('BlogPost', secondary=blog_tags, back_populates='tags_in_blog_post')


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    blurb = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)
    image_url = Column(String)
    # category_id = Column(Integer, ForeignKey('categories.id'), nullable=False) # need to build table
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    # Add plain text blurb
    blurb_plaintext = Column(Text)

    tags_in_project = relationship('Tag', secondary=project_tags, back_populates='projects_with_tag')
    # category = relationship('Category', back_populates='projects_for_category')


class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    blurb = Column(Text, nullable=False)
    image_url = Column(String)
    # category_id = Column(Integer, ForeignKey('categories.id'), nullable=False) # need to build table
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    blurb_plaintext = Column(Text)

    tags_in_blog_post = relationship('Tag', secondary=blog_tags, back_populates='blog_posts_with_tag')
    # blog_cat = relationship('Category', back_populates='blogs_in_category')


# Deprecated in favor of tags
# class Category(Base):
#     __tablename__ = 'categories'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False, unique=True)
#     slug = Column(String, unique=True)

#     projects_for_category = relationship('Project', back_populates='category')
#     blogs_in_category = relationship('BlogPost', back_populates='blog_cat')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    logo_img = Column(String, unique=True)
    security_question = Column(String, nullable=False)
    security_answer_hash = Column(String)

    is_admin = Column(Boolean, nullable=False, default=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def set_security_answer(self, answer):
        normalized = answer.strip().casefold()
        self.security_answer_hash = generate_password_hash(normalized)

    
    def check_security_answer(self, answer):
        normalized = answer.strip.casefold()
        return check_password_hash(self.security_answer_hash, normalized)
    