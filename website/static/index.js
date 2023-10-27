function deleteNote(noteId) {
  // take note id that was passed in index.html
  fetch("/delete-note", {
    // send post request to delete note endpoint
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/"; // redirect to home page (refresh page)
  });
}
