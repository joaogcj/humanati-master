const values=[72,84,67,91];document.querySelectorAll('[data-progress]').forEach((el,i)=>el.style.width=(values[i%values.length])+'%');
