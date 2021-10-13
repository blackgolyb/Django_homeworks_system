window.addEventListener('unload', function() {
    /*window.open(window.location.protocol+"//"+window.location.hostname+":8000/logout", 'windowName', "height=200,width=200");
*/
    localStorage.clear();
});
