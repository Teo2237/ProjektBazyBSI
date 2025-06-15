document.addEventListener('DOMContentLoaded', () => {
    const addForm = document.getElementById('add-game-form');
    const editFormContainer = document.getElementById('edit-form-container');
    const editForm = document.getElementById('edit-game-form');
    const gamesList = document.getElementById('admin-games-list');
    const cancelEditBtn = document.getElementById('cancel-edit');

    const API_URL = '/api/admin/games';

    const getFormData = (form) => {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => { data[key] = value; });
        if (data.genres) {
            data.genres = data.genres.split(',').map(g => g.trim());
        } else {
            data.genres = [];
        }
        return data;
    };

    const fetchAndDisplayGames = async () => {
        try {
            const response = await fetch('/api/games');
            const games = await response.json();
            gamesList.innerHTML = '';
            games.forEach(game => {
                const li = document.createElement('li');
                li.innerHTML = `
                        <span>${game.title}</span>
                        <div class="buttons">
                            <button class="edit-btn" data-id="${game._id}">Edytuj</button>
                            <button class="delete-btn" data-id="${game._id}">Usuń</button>
                        </div>
                    `;
                gamesList.appendChild(li);
            });
        } catch (error) {
            console.error('Błąd podczas pobierania gier:', error);
        }
    };

    addForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = getFormData(addForm);
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            if (response.ok) {
                addForm.reset();
                fetchAndDisplayGames();
            } else {
                alert('Nie udało się dodać gry.');
            }
        } catch (error) {
            console.error('Błąd:', error);
        }
    });

    gamesList.addEventListener('click', async (e) => {
        const gameId = e.target.dataset.id;
        if (!gameId) return;

        if (e.target.classList.contains('delete-btn')) {
            if (confirm('Czy na pewno chcesz usunąć tę grę?')) {
                try {
                    const response = await fetch(`${API_URL}/${gameId}`, { method: 'DELETE' });
                    if (response.ok) {
                        fetchAndDisplayGames();
                    } else {
                        alert('Nie udało się usunąć gry.');
                    }
                } catch (error) {
                    console.error('Błąd:', error);
                }
            }
        }

        if (e.target.classList.contains('edit-btn')) {
            const response = await fetch(`/api/games/${gameId}`);
            const game = await response.json();

            editForm.elements.id.value = game._id;
            editForm.elements.title.value = game.title;
            editForm.elements.release_date.value = game.release_date;
            editForm.elements.genres.value = game.genres.join(', ');
            editForm.elements.developer.value = game.developer || '';
            editForm.elements.publisher.value = game.publisher || '';
            editForm.elements.cover_image.value = game.cover_image || '';
            editForm.elements.description.value = game.description || '';

            editForm.elements.youtube_trailer_id.value = game.youtube_trailer_id || '';
            editForm.elements.screenshots.value = game.screenshots ? game.screenshots.join('\n') : '';

            editFormContainer.style.display = 'block';
            addForm.style.display = 'none';
        }
    });

    editForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = getFormData(editForm);
        const gameId = data.id;
        delete data.id;

        try {
            const response = await fetch(`${API_URL}/${gameId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                editFormContainer.style.display = 'none';
                addForm.style.display = 'flex';
                fetchAndDisplayGames();
            } else {
                alert('Nie udało się zaktualizować gry.');
            }
        } catch (error) {
            console.error('Błąd:', error);
        }
    });

    cancelEditBtn.addEventListener('click', () => {
        editFormContainer.style.display = 'none';
        addForm.style.display = 'flex';
    });

    fetchAndDisplayGames();
});