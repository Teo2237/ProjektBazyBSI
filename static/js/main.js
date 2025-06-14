// Cały kod JavaScript pozostaje bez zmian
document.addEventListener('DOMContentLoaded', () => {
    const gamesContainer = document.getElementById('games-container');
    const genreFilter = document.getElementById('genre-filter');
    const sortControl = document.getElementById('sort-control');
    const renderGames = (games) => {
        gamesContainer.innerHTML = '';
        if (games.length === 0) {
            gamesContainer.innerHTML = '<p>Nie znaleziono gier spełniających wybrane kryteria.</p>';
            return;
        }
        games.forEach(game => {
            const cardLink = document.createElement('a');
            cardLink.className = 'game-card';
            cardLink.href = `/games/${game._id}`;
            const genresHTML = game.genres.map(genre => `<span class="genre-tag">${genre}</span>`).join('');
            cardLink.innerHTML = `
                        <img src="${game.cover_image}" alt="Okładka gry ${game.title}">
                        <div class="game-card-content">
                            <div>
                                <h3>${game.title}</h3>
                                <p>Data wydania: ${game.release_date}</p>
                                <p>Deweloper: ${game.developer || 'Brak danych'}</p>
                            </div>
                            <div class="genre-tags-container">
                                ${genresHTML}
                            </div>
                        </div>
                    `;
            gamesContainer.appendChild(cardLink);
        });
    };
    const fetchFilteredGames = async () => {
        const genre = genreFilter.value;
        const sort = sortControl.value;
        const params = new URLSearchParams();
        if (genre) params.append('genre', genre);
        if (sort) params.append('sort', sort);
        const queryString = params.toString();
        const url = `/api/games${queryString ? '?' + queryString : ''}`;
        try {
            gamesContainer.innerHTML = '<p>Ładowanie gier...</p>';
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Błąd HTTP! Status: ${response.status}`);
            const games = await response.json();
            renderGames(games);
        } catch (error) {
            gamesContainer.innerHTML = `<p style="color: red;">Wystąpił błąd: ${error.message}</p>`;
            console.error('Błąd podczas pobierania filtrowanych gier:', error);
        }
    };
    const setupGenreFilter = async () => {
        try {
            const response = await fetch('/api/games');
            if (!response.ok) throw new Error('Nie można pobrać gatunków.');
            const games = await response.json();
            const allGenres = new Set();
            games.forEach(game => game.genres.forEach(genre => allGenres.add(genre)));
            const sortedGenres = [...allGenres].sort();
            sortedGenres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre;
                option.textContent = genre;
                genreFilter.appendChild(option);
            });
        } catch (error) {
            console.error('Błąd podczas ustawiania filtrów gatunków:', error);
        }
    };
    genreFilter.addEventListener('change', fetchFilteredGames);
    sortControl.addEventListener('change', fetchFilteredGames);
    const init = async () => {
        await setupGenreFilter();
        await fetchFilteredGames();
    };
    init();
});