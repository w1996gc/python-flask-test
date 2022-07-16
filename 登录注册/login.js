document.addEventListener('DOMContentLoaded',function(event){
    document.addEventListener('selectstart',function(event){
        event.preventDefault();
    })
    document.addEventListener('contextmenu',function(event){
        event.preventDefault();
    })
    var random_box=document.querySelector('.random');
    var btn=document.querySelector('.reset');
    var wirte=document.querySelector('.write');
    function random(min,max){
         return Math.floor(Math.random()*(max-min+1))+min;
    }
    btn.addEventListener('click',function(){
        btn.style.backgroundColor='#fff';
        window.setTimeout(function(event){
            btn.style.backgroundColor='rgb(255, 224, 146)';
        },50)
        var randoms=random(1000,9999);
        console.log(randoms);
        random_box.innerHTML=randoms;
    })
})
$(function(){
      $('.change-register-button').on('click',function(){
            $('.login').animate(
                {
                    'left':'240px'
                },400,function(){
                    $('.login').css({'display':'none',
                                          'left':'60px'})
                    $('.change-register-box').css('display','none')
                    $('.register').css('display','block')
                    $('.change-login-box').css('display','block')
                }
            )
      })
      $('.change-login-button').on('click',function(){
        $('.register').animate(
            {
                'right':'240px'
            },400,function(){
                $('.register').css({'display':'none',
                                            'right':'60px'})
                $('.change-login-box').css('display','none')
                $('.login').css('display','block')
                $('.change-register-box').css('display','block')
            }
        )
  })
})