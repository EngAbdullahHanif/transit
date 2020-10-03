       // converting miladi date to hijri
    function miladiToHijri(className){
      var miladiClass = document.getElementsByClassName(className);
      hijri = [];
      for(var i = 0; i < miladiClass.length; i++){
          hijri[i] = miladiClass[i].innerHTML;
          miladiClass[i].innerHTML += ' ' + '<span class="text-info">مطابق به </span>' + ' ' + new Date(hijri[i]).toLocaleDateString('fa-IR');
      }

  }

  miladiToHijri('miladi_date');