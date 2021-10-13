const days = document.querySelectorAll('.calendar-day');


for (var i = 0; i < days.length; i++) {
    const info = days[i].querySelector('.calendar-day__hidden-info').innerHTML;

    days[i].addEventListener('click', function (e) {
        // Получаем данные из формы
        render_info(info);
    });
}

function render_info(html) {
    const div = document.querySelector('.calendar-info');
    div.innerHTML = html;
}
