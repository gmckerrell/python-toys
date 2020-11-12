const app = document.getElementById('root');

const container = document.createElement('div');
container.setAttribute('class', 'container');

app.appendChild(container);

var request = new XMLHttpRequest();
request.open('GET', 'http://localhost:5000/booking', true);
request.onload = function () {

  // Begin accessing JSON data here
  var data = JSON.parse(this.response);
  if (request.status >= 200 && request.status < 400) {
    data.forEach(booking => {
      const card = document.createElement('div');
      card.setAttribute('class', 'card');
      container.appendChild(card);

      const h1 = document.createElement('h1');
      h1.textContent = booking.customer
      card.appendChild(h1)

      const table = document.createElement('TABLE')
      card.appendChild(table)

      const tr = document.createElement('TR');
      table.appendChild(tr)

      const td1 = document.createElement('TD')
      td1.textContent = booking.start_date;
      tr.appendChild(td1);
      
      const td2 = document.createElement('TD')
      td2.textContent = booking.end_date
      tr.appendChild(td2);

      const td4 = document.createElement('TD')
      td4.textContent = booking.manufacturer;
      tr.appendChild(td4);

      const td5 = document.createElement('TD')
      td5.textContent = booking.model;
      tr.appendChild(td5);

    });
  } else {
    const errorMessage = document.createElement('marquee');
    errorMessage.textContent = this.response;
    app.appendChild(errorMessage);
  }
}

request.send();
