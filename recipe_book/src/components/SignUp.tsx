import React, { useState } from 'react';
import "./signup.css";
// import { isVaild, err } from './utilities';

const SignUp = () => {
  const defaultFormData = {
    username: "",
    email: "",
    password: "",
    cpassword: "",
  };

  const [formData, setFormData] = useState(defaultFormData);

 const [error, setError] = useState({
    username: false,
    email: false,
    password: false,
    match: false,
  });
 


  const { username, email, password, cpassword } = formData;

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setError((prev) => ({ ...prev, [name]: false }));

    setFormData((prev) => ({ ...prev, [name]: value }));
    
  };

  
  const isValid = (username: string, password: string, cpassword: string, email: string) => {
    let state = true;
    const nameRegex = /^[a-zA-Z]{3,15}$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()]).{8,}$/;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    
    const userName = username.trim();
    const pword = password.trim();
    const cPword = cpassword.trim();
    const mail = email.trim();
    

    if (!nameRegex.test(userName)) {
      // The string does not match the regex pattern
      
      setError((err) => ({ ...err, username: true }));
  
    state =  false;
    } else {
      state = true;
      setError((err) => ({ ...err, username: false }));
    }
    if (!passwordRegex.test(pword)) {
      // The string does not match the regex pattern

      setError((err) => ({ ...err, password: true }));
    state =  false;
    } else {
      state = true;
      setError((err) => ({ ...err, password: false }));
    }
    if (cPword !== pword) {
      // The string does not match the regex pattern
      setError((err) => ({ ...err, match: true }));
      state = false;
    } else {
      state = true; 
      setError((err) => ({ ...err, match: false }));
    }
  
    if (!emailRegex.test(mail)) {
      // The string does not match the regex pattern
      setError((err) => ({ ...err, email: true }));
    state =  false;
    } else {
      state = true;  
      setError((err) => ({ ...err, email: false }));
    }
  
    return state;
  
  };

  
  const handleSignup = (e: any) => { 
    
    e.preventDefault();
    let valid = isValid(username, password, cpassword, email)
    if (valid) { 
      setFormData(defaultFormData);
    } 
   
  };


  return (
    <div className="signUp-container">
        <div className="signUp">
          <h2>Sign Up</h2>
          <form onSubmit={handleSignup}>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={username}
               onChange={(e) => handleChange(e)}
              required
            />
            {error.username && (
              <span className="error-message">
                <small>Invalid username</small>
              </span>
            )}
            <input
              type="email"
              name="email"
              placeholder="email@example.com"
              // pattern="\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
              value={email}
              onChange={(e) => handleChange(e)}
              required
            />
            {error.email && (
              <span className="error-message">
                <small>Invalid email</small>
              </span>
            )}
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={password}
              onChange={(e) => handleChange(e)}
              required
            />
            {error.password && (
              <span className="error-message">
                <small>Invalid password</small>
                
              </span>
            )}
            <small>
                Password must include at least:
                <ul className='password-format'>
                  <li>1 lowercase letter</li>
                  <li>1 uppercase letter</li>
                  <li>1 number</li>
                  <li>8 characters</li>
                  <li>1 of these special characters: !@#$%^&*()</li>
                </ul>
                 </small>
            <input
              type="password"
              name="cpassword"
              placeholder="Confirm password"
              value={cpassword}
              onChange={(e) => handleChange(e)}
              required
            />
            {error.match && (
              <span className="error-message">
                <small>Passwords do not match</small>
              </span>
            )}
            <button type="submit">Sign Up</button>
          </form>
          <p className="alternative">
            Have an account? <a href="/login">Sign In</a>
          </p>
        </div>
        </div>
      
  )
}

export default SignUp

// username = request.form['username']
// email = request.form['email']
// password = request.form[password]