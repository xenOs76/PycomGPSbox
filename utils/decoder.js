/*
Function to be used in TTN's console as a payload decoder
*/

function Decoder(bytes, port) {

      function bytesToInt (bytes) {
        // since Int is a 4 bytes value we consider 4 indices of bytes array
        var v = bytes[3]<<24 | bytes[2]<<16 | bytes[1]<<8 | bytes[0];
        return v;
      }

      function bytesToULong(bytes) {
        var v = bytes[3]<<24 | bytes[2]<<16 | bytes[1]<<8 | bytes[0];
        return v;
      }

      function bytesToFloat(bytes) {
        // JavaScript bitwise operators yield a 32 bits integer, not a float.
        // Assume LSB (least significant byte first).
        var bits = bytes[3]<<24 | bytes[2]<<16 | bytes[1]<<8 | bytes[0];
        var sign = (bits>>>31 === 0) ? 1.0 : -1.0;
        var e = bits>>>23 & 0xff;
        var m = (e === 0) ? (bits & 0x7fffff)<<1 : (bits & 0x7fffff) | 0x800000;
        var f = sign * m * Math.pow(2, e - 150);
        return f;
      }

      function bytesToUShort(bytes){
        var v = bytes[1]<<8 | bytes[0];
        return v;
      }


      function dir_to_s(n){
        var cards = new Array();
        cards[1] = 'N';
        cards[2] = 'S';
        cards[3] = 'E';
        cards[4] = 'W';

        var dir_s = '';

        while (n>0){
          if (n>10){
            var d = n % 10; //  last digit as a remainder
            n = n / 10; // divide by 10
            n = parseInt(n); // and discard the decimals
            //console.log("curr last digit: " + d)
            //ocnsole.log("now n is:" + n)
            //console.log("now dir is:" + cards[d])
            dir_s = cards[d] + dir_s ;
          } else {
             //console.log("first digit:" + n)
             //console.log("now dir is:" + cards[n])
            dir_s = cards[n] + dir_s ;
            n = 0; // exits the while
          }

        }
        return dir_s;
      }

      lat = bytesToFloat(bytes.slice(0,4)).toFixed(5);
      lon = bytesToFloat(bytes.slice(4,8)).toFixed(5);

      alt_x10 = bytesToUShort(bytes.slice(8,10));
      alt = (alt_x10 / 10).toFixed(1);

      speed_x10 = bytesToUShort(bytes.slice(10,12));
      speed = (speed_x10 / 10).toFixed(1);

      dir_n = bytesToUShort(bytes.slice(12,14));
      dir = dir_to_s(dir_n);

      ts = bytesToULong(bytes.slice(14,18));

      json = { "lat": lat, "lon": lon, "alt": alt, "speed": speed, "dir": dir, "ts": ts };

      return {
        gps_data: json
      };
  }
