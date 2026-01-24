const ring = document.getElementById('ring');
const cards = document.querySelectorAll('.card');
const passInput = document.getElementById('pass-input');
const goBtn = document.getElementById('go-btn');
const log = document.getElementById('log');

let rotationY = 0;
let isDragging = false;
let startX = 0;

// 1. Position cards in a 3D Circle
const radius = 400; // Distance from the Py1iner text
const angleStep = 360 / cards.length;

function updateCards() {
    cards.forEach((card, i) => {
        const angle = (i * angleStep) + rotationY;
        // Check if card is being hovered
        const scale = card.matches(':hover') ? 1.15 : 1;
        // The magic: Rotate the ring, but counter-rotate the card so it faces us
        card.style.transform = `rotateY(${angle}deg) translateZ(${radius}px) rotateY(${-angle}deg) scale3d(${scale}, ${scale}, ${scale})`;
        
        // Simple Opacity/Z-index trick for realism
        const normalizedAngle = ((angle % 360) + 360) % 360;
        if (normalizedAngle > 90 && normalizedAngle < 270) {
            card.style.opacity = "0.4"; // Card is behind the text
        } else {
            card.style.opacity = "1";   // Card is in front
        }
    });
}

// 2. Drag Interaction
window.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX;
});

window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const deltaX = e.clientX - startX;
    rotationY += deltaX * 0.2; // Sensitivity
    startX = e.clientX;
    updateCards();
});

window.addEventListener('mouseup', () => isDragging = false);

// 3. Initial placement
updateCards();

// Add hover listeners to trigger updateCards
cards.forEach(card => {
    card.addEventListener('mouseenter', updateCards);
    card.addEventListener('mouseleave', updateCards);
});

// 4. Unlock Logic
goBtn.addEventListener('click', () => {
    if (passInput.value === "12345") {
        log.innerHTML = "<span style='color:#27c93f'>PASSCODE ACCEPTED. JUMPING...</span>";
        document.body.classList.add('warp-drive');
        setTimeout(() => { alert("Welcome, Commander."); window.location.reload(); }, 1500);
    } else {
        log.innerHTML = "<span style='color:#ff5f56'>INVALID KEY. ACCESS DENIED.</span>";
        passInput.value = "";
    }
});