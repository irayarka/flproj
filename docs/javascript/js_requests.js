function setLocal(id) {
    localStorage.setItem('id', id);
}

function login() {
    const user = {
        username: document.getElementById('username_id').value,
        password: document.getElementById('pass_id').value,
    };
    const xhr = new XMLHttpRequest();
    xhr.crossorigin = true;
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === 4) {
            localStorage.setItem('user', 'Bearer '.concat(JSON.parse(xhr.responseText).access_token));
            localStorage.setItem('userId', JSON.parse(xhr.responseText).id);
        }
    });
    xhr.open('POST', 'http://127.0.0.1:5000/login');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    const data = JSON.stringify(user);
    xhr.send(data);
}

function getcars() {
    const xhr = new XMLHttpRequest();
    xhr.crossorigin = true;
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === 4) {
            const data = JSON.parse(xhr.responseText);
            for (let i = 0; i < 6; ++i) {
                document.getElementsByClassName('car_name')[i].innerHTML = data[i].name;
                document.getElementsByClassName('car_price')[i].innerHTML = data[i].price;
            }
            for (let i = 0; i < 6; ++i) {
                document.getElementById(i).addEventListener('click', setLocal.bind('id', i + 1));
            }
        }
    });
    xhr.open('GET', 'http://127.0.0.1:5000/cars');
    xhr.setRequestHeader('Authorization', localStorage.getItem('user'));
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    xhr.send(null);
}

function signup() {
    const confPass = document.getElementById('conf_pass').value;
    const user = {
        username: document.getElementById('username_id').value,
        firstName: document.getElementById('fname_id').value,
        lastName: document.getElementById('lname_id').value,
        email: document.getElementById('email_id').value,
        phone: document.getElementById('pass_id').value,
        password: document.getElementById('pass_id').value,
        admin: document.getElementById('admin_id').value,
    };
    const xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === 4) {
            if (user.password !== confPass) {
                alert('Passwords don\'t match!');
                window.location.reload();
            } else {
                localStorage.setItem('user', JSON.parse(xhr.responseText).access_token);
                window.location.href = 'home.html';
            }
        }
    });
    xhr.open('POST', 'http://127.0.0.1:5000/user');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    const data = JSON.stringify(user);
    xhr.send(data);
}

function updateuser() {
    let user = {
        username: document.getElementById('username_id').value,
        firstName: document.getElementById('fname_id').value,
        lastName: document.getElementById('lname_id').value,
        email: document.getElementById('email_id').value,
        phone: document.getElementById('phone_id').value,
        password: document.getElementById('pass_id').value,
    };
    const xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === 4) {
            window.location.href = 'home.html';
        }
    });
    xhr.open('PUT', 'http://127.0.0.1:5000/user/'.concat(localStorage.getItem('userId')));
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    xhr.setRequestHeader('Authorization', localStorage.getItem('user'));
    xhr.send(user);
    alert('The user has been updated succesfully!');
}

function carbyid() {
    const xhr = new XMLHttpRequest();
    xhr.crossorigin = true;
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === 4) {
            const data = JSON.parse(xhr.responseText);
            document.getElementsByClassName('car_name')[0].innerHTML = data.name;
            document.getElementsByClassName('car_price')[0].innerHTML = data.price;
        }
    });
    const carId = localStorage.getItem('id');
    xhr.open('GET', 'http://127.0.0.1:5000/cars/car/'.concat(carId));
    xhr.setRequestHeader('Authorization', localStorage.getItem('user'));
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    xhr.send(null);
}

function addtocart() {
    let data = {
        shipDate: document.getElementById('from').value,
        returnDate: document.getElementById('to').value,
    };
    const xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === 4) {
            localStorage.setItem('orderId', JSON.parse(xhr.responseText).id);
            localStorage.setItem('orderedCar', localStorage.getItem('id'));
        }
    });
    const carId = localStorage.getItem('id');
    xhr.open('POST', 'http://127.0.0.1:5000/cars/car/'.concat(carId, '/order'));
    xhr.setRequestHeader('Authorization', localStorage.getItem('user'));
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    data = JSON.stringify(data);
    xhr.send(data);
}

function carincart() {
    const xhr = new XMLHttpRequest();
    xhr.crossorigin = true;
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === 4) {
            const data = JSON.parse(xhr.responseText);
            document.getElementsByClassName('product-title')[0].innerHTML = data.name;
            document.getElementsByClassName('product-price')[0].innerHTML = data.price;
        }
    });
    const orderedCar = localStorage.getItem('orderedCar');
    xhr.open('GET', 'http://127.0.0.1:5000/cars/car/'.concat(orderedCar));
    xhr.setRequestHeader('Authorization', localStorage.getItem('user'));
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    xhr.send(null);
}
