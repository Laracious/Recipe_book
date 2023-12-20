// import React, { useState } from 'react'

// const utilities = () => {
//   const [error, setError] = useState({
//     username: false,
//     email: false,
//     password: false,
//     match: false,
//   });
  
  
//   export const isVaild = (username: string, password: string, cpassword: string, email: string) => {
//     const nameRegex = /^[a-zA-Z]{3,15}$/;
//     const passwordRegex =
//       /^(?=.[a-z])(?=.[A-Z])(?=.[0-9])(?=.[!@#$%^&()])[a-zA-Z0-9!@#$%^&()]{8,}$/;
//     const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    
//     if (!nameRegex.test(username)) {
//       // The string does not match the regex pattern
//       console.log("Invalid name ");
//       setError((err) => ({ ...err, first: true }));
  
//       return false;
//     } else {
//       setError((err) => ({ ...err, first: false }));
//     }
//     if (!passwordRegex.test(password)) {
//       // The string does not match the regex pattern
//       console.log("Invalid password");
//       setError((err) => ({ ...err, pass: true }));
//       return false;
//     } else {
//       setError((err) => ({ ...err, pass: false }));
//     }
  
//     if (cpassword !== password) {
//       // The string does not match the regex pattern
//       setError((err) => ({ ...err, match: true }));
//       return false;
//     } else {
//       setError((err) => ({ ...err, match: false }));
//     }
  
//     if (!emailRegex.test(email)) {
//       // The string does not match the regex pattern
//       setError((err) => ({ ...err, mail: true }));
//       return false;
//     } else {
//       setError((err) => ({ ...err, mail: false }));
//     }
  
  
//     return true;
  
//   };
  
//   // export const err = error;

//   return (
//     <div>utilities</div>
//   )
// }

// export default utilities
