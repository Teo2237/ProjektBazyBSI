document.addEventListener('DOMContentLoaded', async () => {
    const detailsContainer = document.getElementById('game-details-container');
    const trailerSection = document.getElementById('trailer-section');
    const gallerySection = document.getElementById('gallery-section');

    try {
        const pathParts = window.location.pathname.split('/');
        const gameId = pathParts[pathParts.length - 1];

        if (!gameId) throw new Error('Nie znaleziono ID gry w adresie URL.');

        const response = await fetch(`/api/games/${gameId}`);
        if (!response.ok) throw new Error(`Nie udało się pobrać danych. Status: ${response.status}`);

        const game = await response.json();
        document.title = game.title;

        // --- Renderowanie głównych informacji (bez zmian) ---
        const genresHTML = game.genres.map(genre => `<span class="genre-tag">${genre}</span>`).join('');
        detailsContainer.innerHTML = `
                    <div class="details-grid">
                        <div class="cover-image">
                            <img src="${game.cover_image}" alt="Okładka gry ${game.title}">
                        </div>
                        <div class="game-info">
                            <h1>${game.title}</h1>
                            <div class="meta-info">
                                <p><strong>Deweloper:</strong> ${game.developer || 'Brak danych'}</p>
                                <p><strong>Wydawca:</strong> ${game.publisher || 'Brak danych'}</p>
                                <p><strong>Data wydania:</strong> ${game.release_date}</p>
                            </div>
                            <div class="genre-tags-container">${genresHTML}</div>
                            <p class="description">${game.description || 'Brak opisu.'}</p>
                        </div>
                    </div>
                `;

        // --- NOWA LOGIKA: Renderowanie zwiastuna ---
        if (game.youtube_trailer_id) {
            trailerSection.innerHTML = `
                        <h2 class="section-title">Zwiastun</h2>
                        <div class="trailer-container">
                            <iframe 
                                src="https://www.youtube.com/embed/${game.youtube_trailer_id}" 
                                title="YouTube video player" 
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                allowfullscreen>
                            </iframe>
                        </div>
                    `;
        }

        // --- NOWA LOGIKA: Renderowanie galerii screenshotów ---
        if (game.screenshots && game.screenshots.length > 0) {
            const galleryHTML = game.screenshots.map(url => `
                        <a href="${url}" target="_blank">
                            <img src="${url}" alt="Screenshot gry">
                        </a>
                    `).join('');

            gallerySection.innerHTML = `
                        <h2 class="section-title">Galeria</h2>
                        <div class="gallery-container">
                            ${galleryHTML}
                        </div>
                    `;
        }

    } catch (error) {
        console.error('Błąd:', error);
        detailsContainer.innerHTML = `<p style="color: red;">Wystąpił błąd podczas ładowania gry: ${error.message}</p>`;
    }
});