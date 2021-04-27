document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('.login-form').onsubmit = () => {

        // Инициализировать новый запрос
        const request = new XMLHttpRequest();
        const currency = document.querySelector('.login-form').value;
        request.open('POST', '/login');

        // Функция обратного вызова, когда запрос завершен
        request.onload = () => {

            // Извлечение данных JSON из запроса
            const data = JSON.parse(request.responseText);

            // Обновите result div
            if (data.success) {
                const contents = `1 USD is equal to ${data.rate} ${currency}.`
                document.querySelector('#result').innerHTML = contents;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }

        // Добавить данные для отправки с запросом
        const data = new FormData();
        data.append('currency', currency);

        // Послать запрос
        request.send(data);
        return false;
    };

});