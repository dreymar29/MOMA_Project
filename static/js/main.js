function openArtModal(artId) {
    const modal = document.getElementById('modal-' + artId);
    if (modal) {
        console.log("Membuka modal untuk ID: " + artId); // Cek di console browser
        modal.style.setProperty('display', 'block', 'important');
        document.body.style.overflow = 'hidden';
    } else {
        console.error("Modal tidak ditemukan untuk ID: modal-" + artId);
    }
}

function closeArtModal(artId) {
    const modal = document.getElementById('modal-' + artId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});