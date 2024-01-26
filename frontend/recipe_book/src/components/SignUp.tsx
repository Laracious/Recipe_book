import { BaseSyntheticEvent, useState } from "react";
import "./signup.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const SignUp = () => {
  //STORE THE DEFAULT (EMPTY) FORM STATE OF THE FORM
  const defaultFormData = {
    fullname: "",
    username: "",
    email: "",
    password: "",
    cpassword: "",
  };

  //SET THE INITIAL FORM STATE TO THE DEFAULT.
  const [formData, setFormData] = useState(defaultFormData);

  //SET THE INITIAL ERROR STATE.
  const [error, setError] = useState({
    fullname: false,
    username: false,
    email: false,
    password: false,
    match: false,
  });

  const navigate = useNavigate();

  //DESTRUCTURE THE FORM-DATA OBJECT
  const { fullname, username, email, password, cpassword } = formData;

  //CHANGE FUNCTION FOR UPDATING FORM-DATA VALUES IN REAL-TIME.
  const handleChange = (e: BaseSyntheticEvent) => {
    //DESTRUCTURE INPUT EVENT OBJECT
    const { name, value } = e.target;

    //RESET ERROR STATE ON FORM CHANGE
    setError((prev) => ({ ...prev, [name]: false }));

    //SET THE STATE OF THE FORM-DATA TO THE CURRENT VALUE
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  //FUNCTION FOR HANDLING FORM VALIDATION
  const isValid = (
    fullname: string,
    username: string,
    password: string,
    cpassword: string,
    email: string
  ) => {
    let state = true;
    const nameRegex = /^[a-zA-Z ]{3,30}$/; // Allow spaces in the full name
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()]).{8,}$/;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    const isValidFullName = nameRegex.test(fullname.trim());
    const userName = username.trim();
    const pword = password.trim();
    const cPword = cpassword.trim();
    const mail = email.trim();

    const isValidUsername = nameRegex.test(userName);
    const isValidPassword = passwordRegex.test(pword);
    const isPasswordMatch = cPword === pword;
    const isValidEmail = emailRegex.test(mail);

    setError({
      fullname: !isValidFullName,
      username: !isValidUsername,
      password: !isValidPassword,
      match: !isPasswordMatch,
      email: !isValidEmail,
    });

    return (
      isValidFullName &&
      isValidUsername &&
      isValidPassword &&
      isPasswordMatch &&
      isValidEmail
    );
  };

  console.log(formData);
  

  //FUNCTION TO HANDLE SIGN-UP
  const handleSignup = async (e: BaseSyntheticEvent) => {
    e.preventDefault();

    //VALIDATE THE FORM-DATA AND STORE THE RESULT
    let valid = isValid(fullname, username, password, cpassword, email);

    //EXECUTE THE ENCLOSED CODE IF FORM VALIDATION RETURNS TRUE
    if (valid) {
      console.log("Form Valid!");
      

const data =  {
  username: username,
  full_name: fullname,
  email: email,
  password: password,
};
const payLoad = JSON.stringify(data);
console.log("payLoad: ", payLoad);


      try {
        
        fetchData(payLoad);
        

       
      } catch (error: any) {
        console.error("Error during registration:", error);
        //DISPLAY ERROR MESSAGE TO USER.
        toast.error(error.message);
      }
    }
  };
  async function fetchData(payLoad: any) {

    const response = await fetch(
      "http://0.0.0.0:5005/api/v1/auth/signup",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: payLoad
      }
    ) ;
    
    const data = await response.json();
    
    
    console.log('response: ', data);
    if (data.message === 'User created successfully.                 A verification email has been sent to your email address.                    Please check your inbox and follow the instructions.'){
      navigate("/sign-in")
    } 

    }
  return (
    <>
      <ToastContainer autoClose={2000} />
      <div className="signUp-container">
        <div className="signUp">
          <h2>Sign Up</h2>
          <form onSubmit={handleSignup}>
          <input
          type="text"
          name="fullname"
          placeholder="Full Name"
          value={fullname}
          onChange={(e) => handleChange(e)}
          required
          />
          {error.fullname && (
          <span className="error-message">
          <small>Invalid full name</small>
          </span>
          )}
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
              <ul className="password-format">
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
            Have an account? <a href="/sign-in">Sign In</a>
          </p>
        </div>
      </div>
    </>
  );
};

export default SignUp;