import "./Footer.css";

function Footer() {
  return (
    <div className="main-footer">
      <div className="container">
        <div className="row">
          {/* Column1 */}
          <div className="col-sm-4">
            <h4>Recipe Book INC</h4>
            <ul className="list-unstyled">
              <li>342-420-6969</li>
              <li>Moscow, Russia</li>
              <li>123 Street South North</li>
            </ul>
          </div>

        </div>
        <hr />
        <div className="row">
          <p className="col-sm">
            &copy;{new Date().getFullYear()} Recipe Book | All rights reserved |
            <a href="/terms" >Terms Of Service</a> | <a href="/privacy">Privacy</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Footer;
