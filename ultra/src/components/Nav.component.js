import { Link } from "react-router-dom"

const Nav = (props) => {
    const logout = props.logout
    return(
        <nav>
            <div style={{display:"flex", flexDirection:"row", justifyContent:"space-between", paddingLeft:'300px', paddingRight:'300px'}}>
                <Link to="/">Home</Link>
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/account">Account</Link>
                <Link onClick={() => {logout()}} to="/">Logout</Link>
            </div>
        </nav>
    )
}
export default Nav;