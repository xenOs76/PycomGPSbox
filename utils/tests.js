/*
to run:
nodejs tests.js
*/
var n = 1234;

function dir_to_s(n){
   var cards = new Array();
   cards[1] = 'N';
   cards[2] = 'S';
   cards[3] = 'E';
   cards[4] = 'W';

   var dir_s = ''

   while (n>0){
     if (n>10){
       var d = n % 10; // first digit as a remainder
       n = n / 10; // divide by 10
       n = parseInt(n) // and discard the decimals
       console.log("curr last digit: " + d)
       console.log("now n is:" + n)
       console.log("now dir is:" + cards[d])
       dir_s = cards[d] + dir_s
     } else {
       console.log("first digit:" + n)
       console.log("now dir is:" + cards[n])
       dir_s = cards[n] + dir_s
       n = 0; // exits the while
     }

   }
   return dir_s;
 }


dir = dir_to_s(n)
console.log(dir)
