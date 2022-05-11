import { useState } from "react";
import { Button, Grid, Paper, TextField } from "@mui/material";
import { useNavigate } from "react-router-dom";
function Register(props){
    const nav = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const handleSubmit = (e) => {
        e.preventDefault();
        if(password !== confirmPassword){
            //TODO: show error
            alert("Passwords do not match");
        }
        else{
            const account = {
                username: username,
                password: password
            }
            fetch("/api/accounts/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                    },
                    body: JSON.stringify(account)
            })
            .then(res => res.json())
            .then(data => {
                if(data.error){
                    //TODO: show error probably username taken
                    alert(data.error);
                }
                else{
                    props.setAccount(data);
                    nav("/dashboard");
                }
            })
        }
    }
    return (
        <Grid container justifyContent="center" justifyItems="center">
            <Grid item sm={6} xs={6}>
                <Paper elevation={4} style={{ padding:"10px", marginTop: '30px', background:"#001E3C", borderRadius:'10px', height:"100%", paddingLeft:'30px', paddingRight:'30px', paddingBottom:'100px'}}>
                <h1>Register</h1>
                <form onSubmit={(e) => handleSubmit(e)}>
                    <div style={{display:"flex", justifyContent:"center"} }>
                    <TextField type="text"
                        value={username || ""}
                        label="Username"
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <TextField type="password"
                        style={{marginLeft:"10px"}}
                        value={password || ""}
                        label="Password"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <TextField type="password"
                        style={{marginLeft:"10px"}}
                        value={confirmPassword || ""}
                        label="Confirm Password"
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                    <Button style={{marginLeft:'20px', paddingLeft:'25px', paddingRight:'25px'}}type="submit" variant="outlined" >Login</Button>
                    </div>
                </form>
                </Paper>           
            </Grid>
        </Grid>
        );
}
export default Register;