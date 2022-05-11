import { List } from '@mui/material';
import Todo from './Todo.component'
const TodoList = (props) => {
    const todos = props.todos;
    const display = props.display;
    if(display == 'all'){
        return(
            <List>
                {todos.map(todo => {
                    return(
                        <Todo key={todo.id} todo={todo} id={todo.id} handleCheckChange={props.handleCheckChange} delete={props.delete}/>
                    )
                })}
            </List>
        );
    }
    else if(display == 'complete'){
        return(
            <List>
                {todos.map(todo => {
                    if(todo.is_complete === 1){
                        return(
                            <Todo key={todo.id} todo={todo} id={todo.id} handleCheckChange={props.handleCheckChange} delete={props.delete}/>
                        );
                    }
                })}
            </List>
        );
    }
    else if(display == 'incomplete'){
        return(
            <List>
                {todos.map(todo => {
                    if(todo.is_complete === 0){
                        return(
                            <Todo key={todo.id} todo={todo} id={todo.id} handleCheckChange={props.handleCheckChange}/>
                        );
                    }
                })}
            </List>
        );
    }
}
export default TodoList;