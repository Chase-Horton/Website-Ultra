import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material/';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import React from 'react';

import Home from './Home';
import Login from './Login';
import Register from './Register';
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
    }
    setAccount(account) {
        this.setState({
            account: account,
            isLoggedIn: true
        })
    }
    render() {
        return(
            <ThemeProvider theme={darkTheme}>
                <CssBaseline />
                <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login account={this.state.account} setAccount={this.setAccount}/>} />
                    <Route path="/register" element={<Register />} />
                </Routes>
                </BrowserRouter>
            </ThemeProvider>
        );
    }
}
export default App;