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
