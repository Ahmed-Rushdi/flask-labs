from flask import Blueprint, render_template, request, redirect, url_for, session


bp = Blueprint("auth", __name__, url_prefix="/auth")