from flask import Blueprint, request, session, jsonify
from app import db, requires_auth
from .models import Todo

mod_todo = Blueprint('todo', __name__, url_prefix='/api')

@mod_todo.route('/todo', methods=['POST'])
@requires_auth
def create_todo():
    title = request.form['title']
    text = request.form['text']
    color = request.form['color']
    user_id = session['user_id']
    todo = Todo(title, text, color, user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify(success=True, todo=todo.to_dict())

@mod_todo.route('/todo', methods=['GET'])
@requires_auth
def get_all_todos():
    user_id = session['user_id']
    todos = Todo.query.filter(Todo.user_id == user_id).all()
    return jsonify(success=True, todos=[todo.to_dict() for todo in todos])

@mod_todo.route('/todo/<id>', methods=['GET'])
@requires_auth
def get_todo(id):
    user_id = session['user_id']
    todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
    if todo is None:
        return jsonify(success=False), 404
    else:
        return jsonify(success=True, todo=todo.to_dict())

@mod_todo.route('/todo/<id>', methods=['POST'])
@requires_auth
def edit_todo(id):
    user_id = session['user_id']
    todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
    if todo is None:
        return jsonify(success=False), 404
    else:
        todo.title = request.form['title']
        todo.text = request.form['text']
        todo.color = request.form['color']
        db.session.commit()
        return jsonify(success=True)

@mod_todo.route('/todo/<id>/done', methods=['POST'])
@requires_auth
def mark_done(id):
    user_id = session['user_id']
    todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
    if todo is None:
        return jsonify(success=False), 404
    else:
        todo.done = True
        db.session.commit()
        return jsonify(success=True)


@mod_todo.route('/todo/<id>/delete', methods=['POST'])
@requires_auth
def delete_todo(id):
    user_id = session['user_id']
    todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
    if todo is None:
        return jsonify(success=False), 404
    else:
        db.session.delete(todo)
        db.session.commit()
        return jsonify(success=True)
