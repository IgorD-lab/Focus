@views.route('/complete-todo', methods=['POST'])
def complete_todo():
    todo = json.loads(request.data) 
    todoId = todo['todoId']
    todo = Todo.query.get(todoId) 
    if todo: 
        if todo.user_id == current_user.id: 
            todo.completed = True
            db.session.commit()
    return jsonify({})