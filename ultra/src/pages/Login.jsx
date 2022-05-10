import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
//styles
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
async function handleSubmit(e, account, nav){
    e.preventDefault();
    //CALL API TO CHECK IF USERNAME AND PASSWORD ARE CORRECT
    const data = await getServerAccount(account);
    if(data.error){
        alert(data.error);
        nav('/')
    }else{
        this.setAccount(data[0]);
        nav('/');
    }
}
async function getServerAccount(account){
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(account)
        });
        const data = await response.json();
        return data;
    } catch (error) {
        return {error: error.message};
    }
}
const Login = (props) => {
    const nav = useNavigate();
    const [account, setAccount] = useState({username:'', password:''});
    return (
        <Grid container justifyContent="center" justifyItems="center">
            <Grid item sm={6} xs={6}>
                <Paper elevation={4} style={{ padding:"10px", marginTop: '30px', background:"#001E3C", borderRadius:'10px', height:"100%", paddingLeft:'30px', paddingRight:'30px', paddingBottom:'100px'}}>
                <h1>Login</h1>
                <form onSubmit={(e) => handleSubmit(e, account, nav)}>
                    <div style={{display:"flex", justifyContent:"center"} }>
                    <TextField type="text"
                        value={account.username || ""}
                        label="Username"
                        onChange={(e) => setAccount({username:e.target.value, password:account.password})}
                    />
                    <TextField type="password"
                        style={{marginLeft:"10px"}}
                        value={account.password || ""}
                        label="Password"
                        onChange={(e) => setAccount({username:account.username, password:e.target.value})}
                    />
                    <Button style={{marginLeft:'20px', paddingLeft:'25px', paddingRight:'25px'}}type="submit" variant="outlined" >Login</Button>
                    </div>
                </form>
                </Paper>           
            </Grid>
        </Grid>
        );
}
export default Login;