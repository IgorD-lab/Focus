const addBox = document.querySelector(".add-box"),
popupBox = document.querySelector(".popup-box"),
popupTitle = popupBox.querySelector("header p"),
closeIcon = popupBox.querySelector("header i"),
titleTag = document.getElementById("noteTitle"), // Adjusted to match HTML ID
descTag = document.getElementById("noteDescription"), // Adjusted to match HTML ID
addBtn = popupBox.querySelector("button");

const months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
const notes = JSON.parse(localStorage.getItem("notes") || "[]");
let isUpdate = false, updateId;

addBox.addEventListener("click", () => {
    popupTitle.innerText = "Add a new Note";
    addBtn.innerText = "Add Note";
    popupBox.classList.add("show");
    document.querySelector("body").style.overflow = "hidden";
    if(window.innerWidth > 660) titleTag.focus();
});

closeIcon.addEventListener("click", () => {
    isUpdate = false;
    titleTag.value = descTag.value = "";
    popupBox.classList.remove("show");
    document.querySelector("body").style.overflow = "auto";
});

function showMenu(elem) {
    elem.parentElement.classList.add("show");
    document.addEventListener("click", e => {
        if(e.target.tagName != "I" || e.target != elem) {
            elem.parentElement.classList.remove("show");
        }
    });
}

function deleteNote(noteId) {
    fetch(`/delete-note/${noteId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
        }
    }).then(response => {
        if (response.ok) {
            window.location.reload(); // Reload the page to update the list of notes
        } else {
            console.error('Failed to delete the note with response status:', response.status);
        }
    }).catch(error => console.error('Error:', error));
}

function editNote(noteId, title, filterDesc) {
    let description = filterDesc.replaceAll('<br>', '\n');
    document.getElementById("noteTitle").value = title;
    document.getElementById("noteDescription").value = description;
    document.querySelector(".popup-box").classList.add("show");
    document.querySelector("body").style.overflow = "hidden";
    document.querySelector("form").action = `/edit-note/${noteId}`;
    document.querySelector("form button").innerText = "Update Note";
    popupTitle.innerText = "Edit Note";
}
