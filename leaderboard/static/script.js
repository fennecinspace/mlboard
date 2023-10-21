function onFileSubmit(URL) {
    if (document.getElementById("fileInput").files.length != 1 )
        alert("Please select a file");
    else{
        document.getElementById("FileForm").style.display = 'none'
        document.getElementById("spinner").style.display = "block"
        var file = document.getElementById('fileInput').files[0];
        var req = new XMLHttpRequest();
        var form = new FormData();
        form.append('image', file);
        req.onreadystatechange = function() {
            if (req.readyState == XMLHttpRequest.DONE) {
                onResponse(URL, req.responseText);
            }
        }
        req.open("POST", `${URL}/upload`)
        req.send(form)

    }
}


function onResponse(URL, response){
    res = JSON.parse(response)
    var result = ""
    for(var key in res){
        console.log(key)
        if (key == "origin_path"){
            console.log("here")
            document.getElementById("app-results-original").style.display = "block";
            document.getElementById("app-results-original").getElementsByTagName("img")[0].src = res.origin_path.replaceAll("./", URL + "/");
        } else if (key == "path"){
            document.getElementById("app-results-after").style.display = "block";
            document.getElementById("app-results-after").getElementsByTagName("img")[0].src = res.path.replaceAll("./", URL + "/");
        } else {
            result += "<b>" + key + "</b>" + " : " + res[key] + "<br>"
        }
    }
    document.getElementById("app-results-result").style.display = "block";
    document.getElementById("result-content").innerHTML = result;


    document.getElementById("spinner").style.display = "none"
    document.getElementById("FileForm").style.display = "block"
    //document.getElementById("app-results").style.display = "flex"
}
