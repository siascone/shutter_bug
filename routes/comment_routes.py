from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Post, User
from utils.auth import required_logged_in

comments_bp = Blueprint('comments', __name__)

# need routes for create_comment, update_comment, delete_coment