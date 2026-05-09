function openZoom() {
    const modal = document.getElementById("zoomModal");
    if (modal) {
        modal.style.display = "flex";
        document.body.style.overflow = "hidden"; 
    }
}

function closeZoom() {
    const modal = document.getElementById("zoomModal");
    if (modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
}

window.onclick = function(event) {
    const modal = document.getElementById("zoomModal");
    if (event.target == modal) {
        closeZoom();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const scanTriggers = document.querySelectorAll('.js-scan-trigger');

    const resetScans = () => {
        scanTriggers.forEach(t => t.classList.remove('scanning'));
    };

    window.addEventListener('pageshow', resetScans);

    scanTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const targetUrl = this.getAttribute('data-url');
            
            resetScans();
            this.classList.add('scanning');

            setTimeout(() => {
                window.location.href = targetUrl;
            }, 1800);
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.getElementById('bookletWrapper');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');

    if (wrapper && nextBtn && prevBtn) {
        nextBtn.onclick = () => {
            wrapper.scrollLeft += 270;
        };

        prevBtn.onclick = () => {
            wrapper.scrollLeft -= 270;
        };
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const audio = document.getElementById("audioGuide");
    const audioBtn = document.getElementById("audioBtn");
    const audioText = document.getElementById("audioText");
    const audioIcon = document.getElementById("audioIcon");

    if (!audioBtn || !audio) return;

    audioBtn.addEventListener('click', function() {
        audio.load();
        if (audio.paused) {
            // MODE PLAY
            audio.play().then(() => {
                audioIcon.innerText = "▶️"; 
                audioText.innerText = "Playing";
                audioBtn.classList.replace('btn-dark', 'btn-danger'); // Merah buat tanda Stop
            }).catch(error => console.error("Gagal putar:", error));
        } else {
            // MODE STOP (Langsung reset ke awal)
            audio.pause();
            audio.currentTime = 0; // Ini rahasianya biar dia balik ke detik 0
            
            audioIcon.innerText = "🔊";
            audioText.innerText = "Play Audio";
            audioBtn.classList.replace('btn-danger', 'btn-dark');
            console.log("⏹️ Audio Stopped & Reset");
        }
    });

    audio.onended = function() {
        audioIcon.innerText = "✅";
        audioText.innerText = "Played";
        audioBtn.classList.replace('btn-danger', 'btn-success');
        
        setTimeout(() => {
            audioIcon.innerText = "🔊";
            audioText.innerText = "Play Audio";
            audioBtn.className = "btn btn-dark me-2";
        }, 3000);
    };
});