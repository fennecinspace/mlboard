function general_overlay(open) {
    if (open) {
        document.querySelector("#general_overlay").style.display = 'grid';
    }
    else {
        document.querySelector("#general_overlay").style.display = 'none';
        document.querySelector('.responsive-video > iframe').contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
    }
}