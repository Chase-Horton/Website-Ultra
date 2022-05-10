import {useRoutes, Outlet, Navigate} from 'react-router-dom';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
const RoutesAsObject = (props) => {
    const app = props.app;
    let element = useRoutes([
        {path: '', element: <Home />},
        {path: 'login', element: app.state.account === null ? <Login setAccount={app.setAccount} account={app.state.account}/> : <Navigate to="/dashboard"/>},
        {path: 'register', element: <Register />},
        {path: 'dashboard', element: <Dashboard account={app.state.account} logout={app.logout}/>},
    ]);
    return (
        <div>
            {element}
        </div>
    )
}
export default RoutesAsObject;