$(function() {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    
    ctx.canvas.width = 2500;
    ctx.canvas.height = 2500;
    var datas = [{% for row in rows %}
                    {{ row }},
                 {% endfor %}];
    var path = [{% for p in path %}
                    {{ p }},
                {% endfor %}];
    colors = ['rgb(200, 200, 200)', 'rgb(200, 0, 0)', 'rgb(0, 200, 0)', 'rgb(0, 0, 0)'];
    ctx.fillStyle = 'rgb(200, 0, 0)';
    for (var i = 0; i < datas.length; i++) {
        for (var j = 0; j < datas[i].length; j++) {
            console.log(colors[datas[i][j]]);
            ctx.fillStyle = colors[datas[i][j]];
            ctx.fillRect(i*12, j*12, 8, 8);
        }
    }
    
    ctx.beginPath()
    ctx.fillStyle = 'rgb(255, 255, 255)'
    ctx.lineWidth = 5;
    ctx.moveTo(path[0][0], path[0][1]);
    for (var i = 1; i < path.length; i++) {
        ctx.lineTo(path[i][0]*12+6, path[i][1]*12+6);
    }
    ctx.stroke();

    $('#confirm').click(function() {
        location.href="http://127.0.0.1:5000?height=" + $('#width').val() + "&width=" + $('#height').val()
                            + "&o_width=" + $('#o-width').val() + "&o_height=" + $("#o-height").val()
                            + "&o_count=" + $("#o-count").val() + "&algo=" + $('#algo').val();
    });
});
