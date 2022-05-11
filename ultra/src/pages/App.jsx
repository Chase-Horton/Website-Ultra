import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material/';
import { BrowserRouter, Routes, Route, Router } from 'react-router-dom';
import React from 'react';

import Home from './Home';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';


const STORAGEKEY = 'ultra-account';

const darkTheme = createTheme({
    palette: {
      mode: 'dark',
    },
});
const lightTheme = createTheme({
    palette: {
        mode: 'light',
    },
});
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoggedIn: false,
            account: null
        }
        const savedAccount = localStorage.getItem(STORAGEKEY);
        if(savedAccount !== "null"){
            this.state.isLoggedIn = true;
            this.state.account = JSON.parse(savedAccount);
        }
    }
    logout = () => {
        this.setState({
            isLoggedIn: false,
            account: null
        });
        localStorage.setItem(STORAGEKEY, null);
    }
    setAccount = (account) => {
        this.setState({
            account: account,
            isLoggedIn: true
        });
        localStorage.setItem(STORAGEKEY, JSON.stringify(account));
    }
    render() {
        return(
            <ThemeProvider theme={darkTheme}>
                <CssBaseline />
                <BrowserRouter>
                   <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login account={this.state.account} setAccount={this.setAccount}/>} />
                        <Route path="/register" element={<Register setAccount={this.setAccount}/>} />
                        <Route path="/dashboard" element={<Dashboard account={this.state.account} logout={this.logout}/>} />
                   </Routes>
                </BrowserRouter>
            </ThemeProvider>
        );
    }
}
export default App;