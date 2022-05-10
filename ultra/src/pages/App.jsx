import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material/';
import { BrowserRouter, Routes, Route, Router } from 'react-router-dom';
import React from 'react';

import RoutesObj from '../routes/routes';


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
                    <RoutesObj app={this}/>
                </BrowserRouter>
            </ThemeProvider>
        );
    }
}
export default App;