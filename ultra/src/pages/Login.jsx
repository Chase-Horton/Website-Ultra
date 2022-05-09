import React from 'react';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
class Login extends React.Component {
    constructor(props) {
        super(props);
        this.account = this.props.account;
        this.setAccount = this.props.setAccount;
        this.state = {
            username: '',
            password: ''
        }

        this.handleSubmit = this.handleSubmit.bind(this);
    }
    async getServerAccount(account){
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
    handleSubmit(e) {
        e.preventDefault();
        //CALL API TO CHECK IF USERNAME AND PASSWORD ARE CORRECT
        const data = await this.getServerAccount(this.state);
        if(data.error){
            alert(data.error);
        }else{
            this.setAccount(data);
        }
    }
    render() {
    return (
        <Grid container justifyContent="center" justifyItems="center">
            <Grid item sm={6} xs={6}>
                <Paper elevation={4} style={{ padding:"10px", marginTop: '30px', background:"#001E3C", borderRadius:'10px', height:"100%", paddingLeft:'30px', paddingRight:'30px', paddingBottom:'100px'}}>
                <h1>Login</h1>
                <form onSubmit={this.handleSubmit}>
                    <div style={{display:"flex", justifyContent:"center"} }>
                    <TextField type="text"
                        value={this.state.username}
                        label="Username"
                        onChange={(e) => this.setState({username: e.target.value})}
                    />
                    <TextField type="password"
                        style={{marginLeft:"10px"}}
                        value={this.state.password}
                        label="Password"
                        onChange={(e) => this.setState({password: e.target.value})}
                    />
                    <Button style={{marginLeft:'20px', paddingLeft:'25px', paddingRight:'25px'}}type="submit" variant="outlined" >Login</Button>
                    </div>
                </form>
                </Paper>           
            </Grid>
        </Grid>
        );
    }
}
export default Login;