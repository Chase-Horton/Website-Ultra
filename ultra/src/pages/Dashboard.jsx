import { useNavigate } from "react-router-dom";
import { useState, useEffect} from "react";
import { Button, Grid, Paper, TextField } from "@mui/material";
import SaveIcon from '@mui/icons-material/Save';

import TodoList from "../components/TodoList.component";
const Dashboard = (props) => {
    const nav = useNavigate();
    const account = props.account;
    const logout = props.logout;

    //const [isLoading, setIsLoading] = useState(true);
    const [todos, setTodos] = useState([]);
    const [newTodo, setNewTodo] = useState("");
    const [newTodoDate, setNewTodoDate] = useState('');
    const [selectedTab, setSelectedTab] = useState("all");

    const url = '/api/todos/';


    const pushTodos = (account_id) => {
        fetch(url + account_id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(todos)
        })
        .then(res => res.json())
        .then(data => {
            //check for err
            if(data.error){
                console.log(data.error);
            }
        });
    }
    const updateTodos = () => {
        fetch(url + account.id)
        .then(res => res.json())
        .then(data => {
            const newTodos = data.map(todo => {
                todo.date_to_complete = todo.date_to_complete.split("T")[0];
                return todo
            })
            setTodos(newTodos);
        });
    }
    const addTodo = () => {
        console.log(newTodoDate)
        if(newTodoDate){
            const todoText = newTodo;
            const newTodos = [...todos, {account_id:account.id, todo_text: todoText, is_complete: 0, id: todos.length + 1, date_to_complete: newTodoDate}];
            setNewTodo("")
            setTodos(newTodos);
        }else{
            // TODO: add error message
            alert("Please select a date");
        }
    }
    const deleteTodo = (id) => {
        const newTodos = todos.filter(todo => todo.id !== id);
        setTodos(newTodos);
    }
    const handleCheckChange = (todoId) => {
        const todo = todos.find(todo => todo.id === todoId);
        const is_complete = todo.is_complete === 1 ? 0 : 1;
        const newTodos = todos.map(todo => {
            if(todo.id === todoId){
                todo.is_complete = is_complete;
            }
            return todo;
        })
        setTodos(newTodos);
    }
    useEffect(() => { updateTodos(); }, []);
    return(
        <div id="Dashboard">
            <Grid container justifyContent="center" justifyItems="center">
                <Paper elevation={4} style={{ padding:"10px", marginTop: '30px', background:"#001E3C", borderRadius:'10px', height:"100%", paddingLeft:'30px', paddingRight:'30px', paddingBottom:'100px'}}>
                <div>
                    <h2>Tasks</h2>
                    <form onSubmit={(e) => {e.preventDefault(); addTodo();}}>
                        <Grid container justifyContent="center">
                            <TextField label="Add Task" type="text" value={newTodo} onChange={(e) => setNewTodo(e.target.value)} required={true}/>
                            <input style={{marginLeft:'15px'}} type={"date"} value={newTodoDate} onChange={(e) => setNewTodoDate(e.target.value)}/>
                            <Button style={{marginLeft:'15px'}}type="submit" variant="contained">Add</Button>
                        </Grid>
                    </form>
                    <br />
                    <Button onClick={() => setSelectedTab("all")} disabled={selectedTab == "all"}>Show All Tasks</Button>
                    <Button onClick={() => setSelectedTab("incomplete")} disabled={selectedTab == "incomplete"}>Show Incomplete Tasks</Button>
                    <Button onClick={() => setSelectedTab("complete")} disabled={selectedTab == "complete"}>Show Complete Tasks</Button>
                    <TodoList todos={todos} handleCheckChange={handleCheckChange} display={selectedTab} delete={deleteTodo}/>
                    <Button variant="outlined" onClick = {() => pushTodos(account.id)} endIcon={<SaveIcon />}>Save Todos</Button>
                </div>
                    <Button variant="outlined" onClick={() => {logout(); nav("/login");}}>Logout</Button>
                </Paper>
            </Grid>
        </div>
    );
}
export default Dashboard;