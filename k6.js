import http from 'k6/http'
import { check, sleep } from 'k6'
export let options =
{
    stages:
    [
        { duration: '2m', target: 400 }, // ramp up to 400 users
        { duration: '3h56m', target: 400 }, // stay at 400 for ~4 hours
        { duration: '2m', target: 0 },
    ]
        
}
export default function()
{ 
    var url = 'http://127.0.0.1:5000/login'
    var payload = JSON.stringify({
        "corr": "lachata@gmail.com",
        "pas": "pruebascarga"
          })
         
    var headers = 
    {
        headers : {
            'Content-Type': 'application/json'
          }
    } 

    var result = http.get(url, payload, headers);
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