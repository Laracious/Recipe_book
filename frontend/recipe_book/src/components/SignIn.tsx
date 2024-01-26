import { useState } from "react";
import "./signin.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import NavBar from "./NavBar";

const SignIn = () => {
  
  //STORE THE DEFAULT (EMPTY) FORM STATE OF THE FORM
  const defaultFormData = {
    usernameOrEmail: "",
    password: "",
  };

//SET THE INITIAL FORM STATE TO THE DEFAULT.
  const [formData, setFormData] = useState(defaultFormData);

  //SET THE INITIAL ERROR STATE.
  const [error, setError] = useState({
    usernameOrMail: false,
    pass: false,
  });

  const navigate = useNavigate();

  //DESTRUCTURE THE FORM-DATA OBJECT
  const { usernameOrEmail, password } = formData;

  //CHANGE FUNCTION FOR UPDATING FORM-DATA VALUES IN REAL-TIME.
  const handleChange = (e: any) => {
    //DESTRUCTURE INPUT EVENT OBJECT
    const { name, value } = e.target;

    //RESET ERROR STATE ON FORM CHANGE
    setError((prev) => ({ ...prev, [name]: false }));

    //SET THE STATE OF THE FORM-DATA TO THE CURRENT VALUE
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  //FUNCTION TO HANDLE SIGN-IN
  const handleLogin = async (e: any) => {
    e.preventDefault();


    //VALIDATE THE FORM-DATA AND STORE THE RESULT
    let valid = isValid(usernameOrEmail, password);

    //COPY THE FORM-DATA
    let data = JSON.stringify({email: formData.usernameOrEmail, password: formData.password});

    console.log("DATA: ", data )
    

    //EXECUTE THE ENCLOSED CODE IF FORM VALIDATION RETURNS TRUE
    if (valid) {
      try {
        // MAKE API CALL FOR LOGIN
      

        const response = await login(data);
        if (!response ) return;
        if (response.token){
          localStorage.setItem('token', response.token.access_token) 
            navigate('/');
  
        }


        
      } catch (error: any) {
        
        console.error("API Error:", error)
        
        //DISPLAY API CALL ERROR MESSAGE TO USER.
        toast.error(error.message);
      }
      

    }
  };

  //FUNCTION FOR HANDLING FORM VALIDATION
  const isValid = (usernameOrEmail: string, password: string) => {

    //CREATE REGEX PATTERN FOR FORM-DATA
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()]).{8,}$/;
      
    const usernameRegex = /^[a-zA-Z]{3,7}$/;

    //EELIMINATE ANY LEADING OR TRAILING WHITESPACE
    const nameOrMail = usernameOrEmail.trim();
    const pword = password.trim();

    
    //CHECK IF STRING IS EMAIL AND VALIDATE ACCORDINGLY
    const isValidNameOrMail = nameOrMail.includes("@")
      ? emailRegex.test(nameOrMail)
      : usernameRegex.test(nameOrMail);

      //VALIDATE PASSWORD
    const isValidPassword = passwordRegex.test(pword);

    //SET THE ERROR STATE TO OPPOSITE OF VALIDITY CHECK
    setError({
      usernameOrMail: !isValidNameOrMail,
      pass: !isValidPassword,
    });

    //RETURN TRUE IF BOTH VALIDATIOBS RETURN TRUE.
    return isValidNameOrMail && isValidPassword;

    
  };
  async function login(payLoad: any) {
try {
  const response = await fetch(
    "http://0.0.0.0:5005/api/v1/auth/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: payLoad
    }
  ) ;

  const data = await response.json();
  return data;

}
catch(error: any) {
        
  console.error("API Error:", error)
  
  //DISPLAY API CALL ERROR MESSAGE TO USER.
  toast.error(error.error);
  return false;
}
    
    }

  return (
    <>
    
    <ToastContainer autoClose={2000} />
    
    <div className="login-container">
      <div className="login">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <input
            type="text"
            name="usernameOrEmail"
            placeholder="Username or email@example.com"
            value={usernameOrEmail}
            onChange={(e) => handleChange(e)}
            required
          />
          {error.usernameOrMail && (
            <span className="error-message">
              <small>Invalid username or email</small>
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
          {error.pass && (
            <span className="error-message">
              <small>Invalid password</small>
            </span>
          )}
          <button type="submit">Sign In</button>
        </form>
        <p className="alternative">
          Dont have an account? <a href="/sign-up">Sign up</a>
        </p>
      </div>
    </div>
    </>
  );
};

export default SignIn;