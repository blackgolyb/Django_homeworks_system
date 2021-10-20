const fixed_blocks = document.querySelectorAll('.default-fixed-wrap');
const body = document.querySelector('body');

function open_fixed_block(block) {
    // console.log(block);
    body.style.overflow = 'hidden';
    block.classList.add('active');
}

function close_fixed_block(block) {
    // console.log(block);
    body.style.overflow = 'auto';
    block.classList.remove('active');
}


fixed_blocks.forEach(function(item) {
  var exitBtn = item.querySelector('.default-fixed-block__close');
  var openBtn = item.querySelector('.default-fixed-block__open');
  // console.log(block);

  exitBtn.addEventListener('click', function () {
    close_fixed_block(item);
  });
  openBtn.addEventListener('click', function () {
    open_fixed_block(item);
  });
});



function toggleActiveEditor(elm) {
  elm.classList.toggle('active');
}

function coverBlockEvents() {
  const coverBlockOptionalDiv = body.querySelectorAll(".cover-block-optional");
  for (var i = 0; i < coverBlockOptionalDiv.length; i++) {
    const coverBlockActivator = coverBlockOptionalDiv[i].querySelector(".cover-block-activator");
    const coverBlockWrap = coverBlockOptionalDiv[i].querySelector(".cover-block__wrapper");
    const bg = coverBlockOptionalDiv[i].querySelector(".cover-block-bg");
    const exitBtn = coverBlockOptionalDiv[i].querySelector(".cover-block__exit-btn");

    coverBlockActivator.addEventListener('click', function () {
      toggleActiveEditor(coverBlockWrap);
    });
    bg.addEventListener('click', function () {
      toggleActiveEditor(coverBlockWrap);
    });
    exitBtn.addEventListener('click', function () {
      toggleActiveEditor(coverBlockWrap);
    });
  }
};
coverBlockEvents();
