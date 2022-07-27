import http from 'k6/http'
import { check, sleep } from 'k6'
export let options =
{
    stages:
    [
        { duration: '30s', target: 20 },
        { duration: '1m30s', target: 10 },
        { duration: '20s', target: 0 },
    ]
        
}
export default function()
{ 
    var url = 'http://127.0.0.1:5000/login'
    var payload = JSON.stringify({
        "correo": "pruebasminutos@gmail.com",
        "pasw": "pruebas"
        })
         
    var headers = 
    {
        headers : {
            'Content-Type': 'application/json'
          }
    } 

    var result = http.post(url, payload, headers);
    check
    (
        result, 
        {
            'status was 200' : r=> r.status == 200
        }
    )
    console.log(result.status);
    
    sleep(1);
}