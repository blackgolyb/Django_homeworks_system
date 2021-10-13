const empties = document.querySelectorAll('.empty');
const color_picker = document.querySelector('#color');
const color_field_adder = document.querySelector('.add-color');
var color_field_counter = 0;

// Fill listeners
function updateEventListener() {
  const colors = document.querySelectorAll('.color');
  for (var i = 0; i < colors.length; i++) {
    colors[i].addEventListener('dragstart', dragStart);
    colors[i].addEventListener('dragend', dragEnd);
    colors[i].addEventListener('click', getMutableObject);
  }
}

color_picker.addEventListener('change', setColor);
color_field_adder.addEventListener('click', addColorField);

// Loop through empty boxes and add listeners
for (const empty of empties) {
  empty.addEventListener('dragover', dragOver);
  empty.addEventListener('dragenter', dragEnter);
  empty.addEventListener('dragleave', dragLeave);
  empty.addEventListener('drop', dragDrop);
}

// Drag Functions
function dragStart() {
  this.classList.add('hold');
}

function dragEnd() {
  this.classList.remove('hold');
}

function dragOver(e) {
  e.preventDefault();
}

function dragEnter(e) {
  e.preventDefault();
  this.classList.add('hovered');
}

function dragLeave() {
  this.classList.remove('hovered');
}

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}

const rgbToHex = rgb => "#" + ((1 << 24) + (Number(rgb.match(/\d{1,3}/gi)[0]) << 16) + (Number(rgb.match(/\d{1,3}/gi)[1]) << 8) + Number(rgb.match(/\d{1,3}/gi)[2])).toString(16).slice(1);

function dragDrop(){
  if (this.classList.contains('hovered')) {
    relative_color_odj = document.querySelector('.hold');
    this.classList.remove('hovered');
    this.style.backgroundColor = window.getComputedStyle(relative_color_odj, null).backgroundColor;

    var rbg_s = window.getComputedStyle(relative_color_odj, null).backgroundColor
    this.querySelector('input[name="'+this.classList[1]+'"]').value = rgbToHex(rbg_s);
  }
}


//set color Functions
function getMutableObject(){
  this.classList.add('change_now');
}

function setColor(){
  mutable_object = document.querySelector('.change_now');
  mutable_object.classList.remove('change_now');
  mutable_object.style.backgroundColor = this.value;
}

//
function addColorField(){
  let html = '\
  <section class="color-field">\
    <label class="color" draggable="true" id="color-' + color_field_counter + '" for="color"></label>\
  </section>\
  '
  colors_list = document.querySelector('.colors__colors-list');
  colors_list.innerHTML += html;
  updateEventListener();
  color_field_counter++;
}
