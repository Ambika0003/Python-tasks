document.addEventListener('DOMContentLoaded', () => {
    const seatContainer = document.querySelector('.seating-grid');
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const noSeatsText = document.getElementById('no-seats-text');
    const seatsCountEl = document.getElementById('seats-count');
    const subtotalEl = document.getElementById('subtotal-amount');
    const totalEl = document.getElementById('total-amount');
    const hiddenSeatIdsInput = document.getElementById('hidden-seat-ids');
    const bookForm = document.getElementById('book-form');
    const submitBtn = document.getElementById('submit-booking-btn');

    if (!seatContainer) return;

    // Track selected seats
    // Map of seatId -> { name, price, type }
    const selectedSeats = new Map();
    const serviceFeePerTicket = 15.00; // Flat fee per ticket

    function updateCheckoutSummary() {
        // Clear list
        selectedSeatsList.innerHTML = '';
        
        if (selectedSeats.size === 0) {
            noSeatsText.style.display = 'block';
            seatsCountEl.textContent = '0';
            subtotalEl.textContent = '₹0.00';
            totalEl.textContent = '₹0.00';
            hiddenSeatIdsInput.value = '';
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.5';
            submitBtn.style.cursor = 'not-allowed';
            return;
        }

        noSeatsText.style.display = 'none';
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        submitBtn.style.cursor = 'pointer';

        let subtotal = 0;
        const seatIds = [];

        selectedSeats.forEach((seat, id) => {
            seatIds.push(id);
            subtotal += seat.price;

            // Create tag
            const tag = document.createElement('span');
            tag.className = `selected-seat-tag ${seat.type.toLowerCase()}`;
            tag.innerHTML = `${seat.name} <small style="margin-left: 4px; opacity: 0.7;">(₹${seat.price.toFixed(2)})</small>`;
            selectedSeatsList.appendChild(tag);
        });

        // Set hidden input value as comma-separated string
        hiddenSeatIdsInput.value = seatIds.join(',');

        // Calculate pricing
        const totalServiceFee = selectedSeats.size * serviceFeePerTicket;
        const grandTotal = subtotal + totalServiceFee;

        // Update elements
        seatsCountEl.textContent = selectedSeats.size;
        subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
        totalEl.textContent = `₹${grandTotal.toFixed(2)}`;
    }

    seatContainer.addEventListener('click', (e) => {
        const seat = e.target.closest('.seat');
        
        // Ensure clicked element is a seat and is not booked
        if (!seat || seat.classList.contains('booked')) {
            return;
        }

        const seatId = seat.dataset.id;
        const seatName = `${seat.dataset.row}${seat.dataset.col}`;
        const seatPrice = parseFloat(seat.dataset.price);
        const seatType = seat.dataset.type;

        if (selectedSeats.has(seatId)) {
            // Unselect
            selectedSeats.delete(seatId);
            seat.classList.remove('selected');
        } else {
            // Select
            selectedSeats.set(seatId, {
                name: seatName,
                price: seatPrice,
                type: seatType
            });
            seat.classList.add('selected');
        }

        updateCheckoutSummary();
    });

    // Initialize button state
    updateCheckoutSummary();
});
