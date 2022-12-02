var x=  document.getElementById("input")//获取输入框元素
var y=  document.getElementById("html") //获取id为html的元素

function btn(){
    y.innerHTML = x.value; //将输入框的值赋给div标签
    document.getElementById('myaaa').innerText=x.value

}