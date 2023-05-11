// src/components/Navbar.js
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/login">Login</Link>
      <Link to="/signup">Signup</Link>
      
    </nav>
  );
  <li class ="nav-item">
    <a class = "nav-link" href={% url 'design_report' %}>View Finplate Design Report</a>
  </li>
}

export default Navbar;
