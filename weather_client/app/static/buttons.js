document.addEventListener("DOMContentLoaded", function() {
    const spButtons = document.querySelectorAll('.sq-button');
    spButtons.forEach(function(e) {
        e.addEventListener('click', function() {
            window.location.href = e.dataset.url;
        });
    });
    
});

document.addEventListener('click', function(e) {
    if (e.target.matches('.sq-add-button')) {
        const container = e.target.previousElementSibling;
        newInput = document.createElement('input');
        newDelete = document.createElement('button');

        newInput.classList.add('sq-input');
        container.appendChild(newInput);

        newDelete.classList.add('btn');
        newDelete.classList.add('sq-delete-button');
        newDelete.textContent = 'Delete';
        newDelete.type = 'button';
        newDelete.value = 'delete';
        container.appendChild(newDelete);
    }
});

document.addEventListener('click', function(e) {
    if (e.target.matches('.sq-delete-button')) {
        const deleteButton = e.target;
        const inputToRemove = deleteButton.previousElementSibling;

        if (inputToRemove && inputToRemove.classList.contains('sq-input')) {
            inputToRemove.remove();
        }
        deleteButton.remove()
        
    }
});
