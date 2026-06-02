document.addEventListener("DOMContentLoaded", () => {
    const seatMapEl = document.getElementById("seat-map");
    const seatsDataEl = document.getElementById("seats-data");
    if (!seatMapEl || !seatsDataEl) return;

    const showtimeId = parseInt(seatMapEl.dataset.showtimeId, 10);
    const tierPrices = {
        prime: parseFloat(seatMapEl.dataset.pricePrime),
        gold: parseFloat(seatMapEl.dataset.priceGold),
        recliner: parseFloat(seatMapEl.dataset.priceRecliner),
    };
    const tierOrder = ["prime", "gold", "recliner"];
    const tierLabels = {
        prime: "Prime",
        gold: "Gold",
        recliner: "Recliners",
    };

    const seats = JSON.parse(seatsDataEl.textContent);
    const seatMeta = new Map();
    const selected = new Set();
    const countEl = document.getElementById("selected-count");
    const totalEl = document.getElementById("total-price");
    const confirmBtn = document.getElementById("confirm-booking");

    const formatInr = (amount) =>
        "₹" + amount.toLocaleString("en-IN", { maximumFractionDigits: 0 });

    tierOrder.forEach((tier) => {
        const tierSeats = seats.filter((s) => s.category === tier);
        if (tierSeats.length === 0) return;

        const heading = document.createElement("h3");
        heading.className = `tier-heading tier-heading-${tier}`;
        heading.textContent = `${tierLabels[tier]} — ${formatInr(tierPrices[tier])} per seat`;
        seatMapEl.appendChild(heading);

        const rows = {};
        tierSeats.forEach((seat) => {
            if (!rows[seat.row_label]) rows[seat.row_label] = [];
            rows[seat.row_label].push(seat);
        });

        Object.keys(rows)
            .sort()
            .forEach((rowLabel) => {
                const rowDiv = document.createElement("div");
                rowDiv.className = "seat-row";

                const label = document.createElement("span");
                label.className = "row-label";
                label.textContent = rowLabel;
                rowDiv.appendChild(label);

                rows[rowLabel]
                    .sort((a, b) => a.seat_number - b.seat_number)
                    .forEach((seat) => {
                        const price = tierPrices[seat.category];
                        seatMeta.set(seat.id, { category: seat.category, price });

                        const btn = document.createElement("button");
                        btn.type = "button";
                        btn.className = `seat ${seat.status}`;
                        btn.dataset.seatId = seat.id;
                        btn.title = `${rowLabel}${seat.seat_number} — ${formatInr(price)}`;

                        if (seat.status === "available") {
                            btn.addEventListener("click", () => toggleSeat(seat.id, btn));
                        }

                        rowDiv.appendChild(btn);
                    });

                seatMapEl.appendChild(rowDiv);
            });
    });

    function toggleSeat(seatId, btn) {
        if (selected.has(seatId)) {
            selected.delete(seatId);
            btn.classList.remove("selected");
            btn.classList.add("available");
        } else {
            selected.add(seatId);
            btn.classList.remove("available");
            btn.classList.add("selected");
        }
        updateSummary();
    }

    function updateSummary() {
        let total = 0;
        selected.forEach((id) => {
            total += seatMeta.get(id)?.price || 0;
        });
        countEl.textContent = selected.size;
        totalEl.textContent = formatInr(total);
        confirmBtn.disabled = selected.size === 0;
    }

    confirmBtn.addEventListener("click", async () => {
        if (selected.size === 0) return;

        confirmBtn.disabled = true;
        confirmBtn.textContent = "Processing...";

        try {
            const res = await fetch("/api/book", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    showtime_id: showtimeId,
                    seat_ids: Array.from(selected),
                }),
            });

            const data = await res.json();

            if (!res.ok) {
                alert(data.error || "Booking failed. Please try again.");
                confirmBtn.disabled = false;
                confirmBtn.textContent = "Confirm Booking";
                if (res.status === 409) window.location.reload();
                return;
            }

            window.location.href = data.redirect;
        } catch {
            alert("Network error. Please try again.");
            confirmBtn.disabled = false;
            confirmBtn.textContent = "Confirm Booking";
        }
    });
});
