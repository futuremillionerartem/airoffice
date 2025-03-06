document.addEventListener('DOMContentLoaded', () => {
    loadPassengers();

    document.getElementById('addPassengerForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            firstName: document.getElementById('firstName').value.trim(),
            lastName: document.getElementById('lastName').value.trim(),
            birthDate: document.getElementById('birthDate').value,
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim()
        };

        try {
            const response = await fetch('/add_passenger', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw await response.json();

            document.getElementById('addPassengerForm').reset();
            loadPassengers();
        } catch (error) {
            alert(error.error || 'Ошибка при добавлении');
        }
    });
});

async function loadPassengers() {
    try {
        const response = await fetch('/passengers');
        const passengers = await response.json();

        const container = document.getElementById('passengersList');
        container.innerHTML = passengers.map(p => `
            <div class="col-12 col-md-6 col-lg-4">
                <div class="passenger-card card p-3 mb-3">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="mb-1">${p.name}</h5>
                            <small class="text-muted">${p.birth}</small>
                        </div>
                        <span class="badge bg-primary">Билетов: ${p.tickets}</span>
                    </div>
                    <div class="mt-2">
                        <div><i class="bi bi-envelope"></i> ${p.email}</div>
                        <div><i class="bi bi-phone"></i> ${p.phone}</div>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Ошибка загрузки:', error);
    }
}

