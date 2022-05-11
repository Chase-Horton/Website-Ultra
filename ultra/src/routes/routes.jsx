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
        {path: 'register', element: app.state.account === null ? <Register /> : <Navigate to="/dashboard"/>},
        {path: 'dashboard', element:app.state.account !== null ? <Dashboard account={app.state.account} logout={app.logout}/> : <Navigate to="/login"/>},
    ]);
    return (
        <div>
            {element}
        </div>
    )
}
export default RoutesAsObject;