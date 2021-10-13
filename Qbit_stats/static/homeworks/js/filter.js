const forms = document.querySelector('form[name=filter_homework]');

forms.addEventListener('submit', function (e) {
    // Получаем данные из формы
    e.preventDefault();
    let url = this.action;
    let method = this.method;
    let params = new URLSearchParams(new FormData(this)).toString();
    // console.log(params);
    ajaxSend(url, method, params);
});

function format_homework_status(val) {
    if (val == 0) {
      return 'not_done';
    }
    else if (val == 1) {
      return 'expected';
    }
    else{
      return 'done';
    }
}

function render(data) {
    // Рендер шаблона
    //
    //
    console.log(data);
    for (var key = 0; key < data['homeworks'].length; key++) {
        data['homeworks'][key]['status'] = format_homework_status(data['homeworks'][key]['status']);
    }

    for (var key = 0; key < data['individual_homeworks'].length; key++) {
        data['individual_homeworks'][key]['status'] = format_homework_status(data['individual_homeworks'][key]['status']);
    }
    console.log(data);

    let homework_section = '\
    <section class="homework default-block {{status}}">\
      <div class="homework__context">\
        <header>\
          <h2>{{ name }}</h2>\
          <h2>{{ topic }}</h2>\
          <hr>\
        </header>\
        <div class="homework__additional-information">\
          <p>\
            Учитель:\
            <a href="{{ teacher.url }}">{{ teacher.full_name }}</a>\
          </p>\
          <p> Дата загрузки: {{ date }}</p>\
        </div>\
        <div class="homework__buttons">\
          {{#file}}\
              <a class="homework__file" href="{{ file }}" download>Скачать</a>\
          {{/file}}\
          {{^file}}\
            <a class="homework__file" href="" onclick="alert(123)">Скачать</a>\
          {{/file}}\
          <input id="homework-{{ id }}" type="file" name="homework_file" onchange="uploadHomework(this)">\
          <label for="homework-{{ id }}">Загрузить</label>\
        </div>\
    \
      </div>\
      <div class="homework__background1">\
  	  </div>\
      <div class="homework__background">\
          <span>{{ name }}</span>\
      </div>\
    </section>'

    let html_homeworks = '{{#homeworks}}' + homework_section + '{{/homeworks}}';
    let html_ind_homeworks = '{{#individual_homeworks}}' + homework_section + '{{/individual_homeworks}}';

    let template = Hogan.compile(html_homeworks);
    let homeworks_ounput = template.render(data);

    let ind_template = Hogan.compile(html_ind_homeworks);
    let ind_homeworks_ounput = ind_template.render(data);

    const homeworks_div = document.querySelector('.homeworks');
    const ind_homeworks_div = document.querySelector('.individual-homeworks');
    homeworks_div.innerHTML = homeworks_ounput;
    ind_homeworks_div.innerHTML = ind_homeworks_ounput;
}
