
async function main() {
    const app       = document.getElementById('root');
    renderBookings(app);
    renderCars(app);
}

async function renderBookings(root) {
    const bookings  = await fetchJsonData("../booking");
    createElement("H2", root, undefined, "Bookings");
    const container = createElement("DIV", root, 'container');
    bookings.forEach(
        booking => {
            const card  = createElement("DIV",   container, 'card');
            const h1    = createElement("H1",    card, undefined, booking.customer);
            const table = createElement("TABLE", card);
            var tr = createElement("TR",    table);
            createElement("TD", tr, undefined, "Dates");
            createElement("TD", tr, undefined, booking.start_date);
            createElement("TD", tr, undefined, booking.end_date);
            
            var tr = createElement("TR",    table);
            createElement("TD", tr, undefined, "Manufacturer");
            createElement("TD", tr, undefined, booking.manufacturer);

            var tr = createElement("TR",    table);
            createElement("TD", tr, undefined, "Model");
            createElement("TD", tr, undefined, booking.model);
        }
    );
}

async function renderCars(root) {
    const cars  = await fetchJsonData("../car");
    createElement("H2", root, undefined, "Cars");
    const container = createElement("DIV", root, 'container');
    cars.forEach(
        car => {
            const card  = createElement("DIV",   container, 'card');
            const h1    = createElement("H1",    card, undefined, car.registration);
            const table = createElement("TABLE", card);
            
            var tr = createElement("TR",    table);
            createElement("TD", tr, undefined, "Model");
            createElement("TD", tr, undefined, car.model);

            var tr = createElement("TR",    table);
            createElement("TD", tr, undefined, "Manufacturer");
            createElement("TD", tr, undefined, car.manufacturer);

            var tr = createElement("TR",    table);
            createElement("TD", tr, undefined, "People Capacity");
            createElement("TD", tr, undefined, car.people);

            var tr = createElement("TR",    table);
            createElement("TD", tr, undefined, "Luggage Capacity");
            createElement("TD", tr, undefined, car.luggage);
        }
    );
}

async function fetchJsonData(url) {
    var response = await fetch(url);
    if (response.ok) {
        return response.json();
    }
}

function createElement(name, container, className, innerText) {
    var e = document.createElement(name);
    if(className) {
        e.className = className;
    }
    if(container) {
        container.appendChild(e);
    }
    if(innerText) {
        e.innerText = innerText;
    }
    return e;
}
