import { useNavigate } from "react-router-dom";
import { useState, useEffect} from "react";
import { Button, Checkbox, Grid, Paper, TextField } from "@mui/material";

import TodoList from "../components/TodoList.component";
const Dashboard = (props) => {
    const nav = useNavigate();
    const account = props.account;
    const logout = props.logout;

    //const [isLoading, setIsLoading] = useState(true);
    const [todos, setTodos] = useState([]);
    const [newTodo, setNewTodo] = useState("");
    const [newTodoDate, setNewTodoDate] = useState(new Date());
    const [selectedTab, setSelectedTab] = useState("all");

    //CHANGE BEFORE BUILDING
    const LOCAL=true;
    const url = LOCAL ? 'http://localhost:80/api/todos/' : '/api/todos/';


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
        const todoText = newTodo;
        const newTodos = [...todos, {account_id:account.id, todo_text: todoText, is_complete: 0, id: todos.length + 1, date_to_complete: newTodoDate}];
        setNewTodo("")
        setTodos(newTodos);
    }
    const deleteTodo = (id) => {
        const newTodos = todos.filter(todo => todo.id !== id);
        setTodos(newTodos);
    }
    const handleCheckChange = (e) => {
        const todoId = e.target.id;
        const is_complete = e.target.checked ? 1 : 0;
        const newTodos = todos.map(todo => {
            if(String(todo.id) === todoId){
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
                            <Button style={{marginLeft:'15px'}}type="submit" variant="contained">Add</Button>
                            <input type={"date"} value={newTodoDate} onChange={(e) => setNewTodoDate(e.target.value)}/>
                        </Grid>
                    </form>
                    <br />
                    <Button onClick={() => setSelectedTab("all")} disabled={selectedTab == "all"}>Show All Tasks</Button>
                    <Button onClick={() => setSelectedTab("incomplete")} disabled={selectedTab == "incomplete"}>Show Incomplete Tasks</Button>
                    <Button onClick={() => setSelectedTab("complete")} disabled={selectedTab == "complete"}>Show Complete Tasks</Button>
                    <TodoList todos={todos} handleCheckChange={handleCheckChange} display={selectedTab} delete={deleteTodo}/>
                    <Button onClick = {() => pushTodos(account.id)}>Push Todos</Button>
                </div>
                    <Button onClick={() => {logout(); nav("/login");}}>Logout</Button>
                </Paper>
            </Grid>
        </div>
    );
}
export default Dashboard;