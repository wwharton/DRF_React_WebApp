import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import AppBear from './AppBear';
import AppRocket from './AppRocket';
import reportWebVitals from './reportWebVitals';

// const response = fetch('http://localhost:8000/wsb/')
// const data = response.json

// const response = fetch('http://localhost:8000/wsb/')
// response.response = response.json
// const element = response.data
//
// console.log(element)



fetch('http://localhost:8000/wsb/')
  .then(response => response.json())
  .then(data => ReadResponse(data))

function ReadResponse(data) {
    var both = data[data.length - 1]
    var bears = both.bears
    var bulls = both.bulls
    console.log(both.bears)
    console.log(both.bulls)

    if(bears > bulls) {

        ReactDOM.render(<React.StrictMode>
            <AppBear/>
        </React.StrictMode>,
    document.getElementById('root')) }

    if(bulls >= bears) {

        ReactDOM.render(<React.StrictMode>
            <AppRocket/>
        </React.StrictMode>,
    document.getElementById('root')) }

};

    // ReactDOM.render(element,
    // document.getElementById('root'))





// function ToDisplay(python_response) {
//   if(python_response === 0) {
//     return (
//         <React.StrictMode>
//             <AppBear/>
//         </React.StrictMode>)
//     }
// if(python_response === 1) {
//     return (
//         <React.StrictMode>
//             <AppRocket/>
//         </React.StrictMode>)
// }
// };

// const element = ToDisplay(python_response)
//
//
//
// //
// ReactDOM.render(element,
//     document.getElementById('root'))

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
