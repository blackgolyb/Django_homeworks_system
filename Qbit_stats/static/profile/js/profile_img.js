var img = new Image();
var canvas = document.getElementById('preview-canvas');
var ctx = canvas.getContext('2d');
var WIDTH = 200;
var HEIGHT = 200;
canvas.width = WIDTH;
canvas.height = HEIGHT;
var fileName = '';

var startСhanging = false;
var mouseIsDown = false;
var lastX = 0;
var lastY = 0;

var profile_form = document.forms.profile_form;




class ResizingPointer {
    width = 20;
    height = 20;
    fillColor = 'rgba(127, 127, 127, 0.2)';
    strokeColor = '#61afef';//'rgb(127, 127, 127)';
    is_draggable = false;
    related_obj = null;
    related_orientation = null;

    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    move_to(x, y) {
      if (this.related_obj) {
        if (this.related_orientation.includes('left')) {
            if (x < 0) {
                this.x = 0;
            } else if (x > this.related_obj.x) {
                this.x = this.related_obj.x;
            } else {
                this.x = x;
            }
        } else if (this.related_orientation.includes('right')) {
            if (x < this.related_obj.x) {
                this.x = this.related_obj.x;
            } else if (x > WIDTH) {
                this.x = WIDTH;
            } else {
                this.x = x;
            }
        } else {
            if (x < 0) {
                this.x = 0;
            } else if (x > WIDTH) {
                this.x = WIDTH;
            } else {
                this.x = x;
            }
        }

        if (this.related_orientation.includes('top')) {
            if (x < 0) {
                this.y = 0;
            } else if (y > this.related_obj.y) {
                this.y = this.related_obj.y;
            } else {
                this.y = y;
            }
        } else if (this.related_orientation.includes('bottom')) {
            if (y < this.related_obj.y) {
                this.y = this.related_obj.y;
            } else if (y > WIDTH) {
                this.y = WIDTH;
            } else {
                this.y = y;
            }
        } else {
            if (y < 0) {
                this.y = 0;
            } else if (y > HEIGHT) {
                this.y = HEIGHT;
            } else {
                this.y = y;
            }
        }
      } else {
        if (x < 0) {
            this.x = 0;
        } else if (x > WIDTH) {
            this.x = WIDTH;
        } else {
            this.x = x;
        }

        if (y < 0) {
            this.y = 0;
        } else if (y > HEIGHT) {
            this.y = HEIGHT;
        } else {
            this.y = y;
        }
      }
    }

    make_rect() {
        ctx.beginPath();
        ctx.rect(this.x - this.width/2, this.y - this.height/2, this.width, this.height);
        ctx.closePath();
    }

    draw() {
        rect(this.x - this.width/2, this.y - this.height/2, this.width, this.height, this.fillColor, this.strokeColor);
    }
}

var pointer1 = new ResizingPointer(0, 0);
var pointer2 = new ResizingPointer(WIDTH, HEIGHT);
pointer1.related_obj = pointer2;
pointer2.related_obj = pointer1;
pointer1.related_orientation = 'top-left';
pointer2.related_orientation = 'right-bottom';

let pointers = [pointer1, pointer2];



// draw functions
function clear() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
}

function rect(x, y, w, h, fillColor, strokeColor) {
    ctx.beginPath();
    ctx.rect(x, y, w, h);
    ctx.closePath();

    if (strokeColor){
        ctx.strokeStyle = strokeColor;
    	ctx.stroke();
    }

    if (fillColor){
        ctx.fillStyle = fillColor;
    	ctx.fill();
    }
}

function draw_skroke() {
    var x1 = pointer1.x;
    var y1 = pointer1.y;
    var x2 = pointer2.x;
    var y2 = pointer2.y;
    var color1 = '#61afef';//'rgb(127, 127, 127)';
    var color2 = 'rgba(127, 127, 127, 0.2)';

    //  paint over the surrounding space
    rect(x1, y1, x2-x1, y2-y1, null, color1);
    rect(0, 0, x1, HEIGHT, color2, null);
    rect(x2, 0, WIDTH-x2, HEIGHT, color2, null);
    rect(x1, 0, x2-x1, y1, color2, null);
    rect(x1, y2, x2-x1, HEIGHT-y2, color2, null);

    for (var i = 0; i < pointers.length; i++) {
        pointers[i].draw();
    }
}

function draw(img, dose_stroke_draw = true) {
    clear();
    ctx.drawImage(img, 0, 0, WIDTH, HEIGHT);
    $("#preview-canvas").removeAttr("data-caman-id");
    if (dose_stroke_draw) {
        draw_skroke();
    }
}

function change_img_start(){
    var file = document.querySelector('#profile-img').files[0];
    var reader = new FileReader();
    var src;
    img = new Image();

    if (file) {
        fileName = file.name;
        reader.readAsDataURL(file);
        reader.addEventListener("load", function (){
            startСhanging = true;

            img.src = reader.result;
            img.onload = function () {
                draw(img);
            }
        }, false);
    }
    else {
        img.src = document.querySelector('#user-img').src;
        img.onload = function () {
            draw(img, dose_stroke_draw = false);
        }
    }
}

function change_img(){
    var file = document.querySelector('#profile-img').files[0];
    var reader = new FileReader();
    if (file) {
        fileName = file.name;
        reader.readAsDataURL(file);
    }
    reader.addEventListener("load", function () {
        startСhanging = true;

        img = new Image();
        img.src = reader.result;
        img.onload = function () {
            draw(img);
        }
    }, false);
}





function get_position_relative_to_canvas(clientX, clientY) {
    var canvasRect = canvas.getBoundingClientRect();
    var x = clientX - canvasRect.left;
    var y = clientY - canvasRect.top;

    return {
        x: x,
        y: y
    };
}

// func for mouse
function handleMouseDown(e) {
    var pos = get_position_relative_to_canvas(e.clientX, e.clientY);
    mouseX = pos.x;
    mouseY = pos.y;

    for (var i = 0; i < pointers.length; i++) {
        pointers[i].make_rect();
        if (ctx.isPointInPath(mouseX, mouseY)) {
            pointers[i].is_draggable = true;
        }
    }

    lastX = mouseX;
    lastY = mouseY;
    mouseIsDown = true;
}

function handleMouseUp(e) {
    var pos = get_position_relative_to_canvas(e.clientX, e.clientY);
    mouseX = pos.x;
    mouseY = pos.y;

    for (var i = 0; i < pointers.length; i++) {
        pointers[i].is_draggable = false;
    }

    mouseIsDown = false;
}

function handleMouseMove(e) {
    if (!mouseIsDown || !startСhanging) {
        return;
    }

    var pos = get_position_relative_to_canvas(e.clientX, e.clientY);
    mouseX = pos.x;
    mouseY = pos.y;

    for (var i = 0; i < pointers.length; i++) {
        let pointer = pointers[i];

        if (pointer.is_draggable) {
            pointer.move_to(pointer.x + (mouseX - lastX), pointer.y + (mouseY - lastY))
        }
    }
    lastX = mouseX;
    lastY = mouseY;

    draw(img);
}





// func for touch
function handleStart(e) {
  var touch = e.changedTouches[0];
  var pos = get_position_relative_to_canvas(touch.clientX, touch.clientY);
  mouseX = pos.x;
  mouseY = pos.y;

  //console.log('handleStart_pos', mouseX, mouseY);

  for (var i = 0; i < pointers.length; i++) {
      pointers[i].make_rect();
      if (ctx.isPointInPath(mouseX, mouseY)) {
          //console.log('you touch it');
          pointers[i].is_draggable = true;
          mouseIsDown = true;
      }
  }

  lastX = mouseX;
  lastY = mouseY;
}


function handleMove(e) {
    if (!mouseIsDown || !startСhanging) {
        return;
    }

    e.preventDefault();
    var touch = e.changedTouches[0];
    var pos = get_position_relative_to_canvas(touch.clientX, touch.clientY);
    mouseX = pos.x;
    mouseY = pos.y;

    //console.log('handleMove_pos', mouseX, mouseY);

    for (var i = 0; i < pointers.length; i++) {
        let pointer = pointers[i];

        if (pointer.is_draggable) {
            pointer.move_to(pointer.x + (mouseX - lastX), pointer.y + (mouseY - lastY))
        }
    }
    lastX = mouseX;
    lastY = mouseY;

    draw(img);
}


function handleEnd(e) {
  e.preventDefault();
  var touch = e.changedTouches[0];
  var pos = get_position_relative_to_canvas(touch.clientX, touch.clientY);
  mouseX = pos.x;
  mouseY = pos.y;

  //console.log('handleEnd_pos', mouseX, mouseY);

  for (var i = 0; i < pointers.length; i++) {
      pointers[i].is_draggable = false;
  }

  mouseIsDown = false;
}




// forms set function
function set_position_to_form(x1, y1, x2, y2) {
  profile_form.x1.value = x1;
  profile_form.y1.value = y1;
  profile_form.x2.value = x2;
  profile_form.y2.value = y2;
}

function set_size_to_form(w, h) {
  profile_form.canvas_w.value = w;
  profile_form.canvas_h.value = h;
}




set_size_to_form(canvas.width, canvas.height);
set_position_to_form(pointers[0].x, pointers[0].y, pointers[1].x, pointers[1].y);
change_img_start();
$("#profile-img").on("change", change_img);


$("#preview-canvas").mousedown(function (e) {
    //.log('mousedown');
    handleMouseDown(e);
});

$("#preview-canvas").mousemove(function (e) {
    //.log('mousemove');
    handleMouseMove(e);
});

$("body").mouseup(function (e) {
    //console.log('mouseup');
    handleMouseUp(e);
    set_position_to_form(pointers[0].x, pointers[0].y, pointers[1].x, pointers[1].y);
});



canvas.addEventListener("touchstart", function (e) {
    //console.log('touchstart');
    handleStart(e);
}, false);

canvas.addEventListener("touchmove", function (e) {
    //console.log('touchmove');
    handleMove(e);
}, false);

canvas.addEventListener("touchend", function (e) {
    //console.log('touchend');
    handleEnd(e);
    set_position_to_form(pointers[0].x, pointers[0].y, pointers[1].x, pointers[1].y);
}, false);
