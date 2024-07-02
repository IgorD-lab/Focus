function deleteTodo(todoId) {
  // take note id that was passed in index.html
  fetch("/delete-todo", {
    // send post request to delete note endpoint
    method: "POST",
    body: JSON.stringify({ todoId: todoId }),
  }).then((_res) => {
    window.location.href = "/todo"; // redirect to home page (refresh page)
  });
}

function completeTodo(todoId) {
  fetch("/complete-todo", {
    method: "POST",
    body: JSON.stringify({ todoId: todoId }),
  }).then((_res) => {
    window.location.href = "/todo";
  });
}

