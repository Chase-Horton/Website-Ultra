import {Checkbox, IconButton} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete';

const Todo = (props) => {
    const todo = props.todo;
    const handleCheckChange = props.handleCheckChange;
    const del = props.delete;
    return(
    <li key={props.id}>
        <Checkbox id={String(todo.id)} checked={todo.is_complete === 1 ? true:false} onClick={(e) => handleCheckChange(e)}> </Checkbox>
         {todo.todo_text}, {todo.date_to_complete.split('-')[1]}/{todo.date_to_complete.split('-')[2]}
         <IconButton aria-label="delete" onClick={(e) => del(todo.id)}>
            <DeleteIcon />
        </IconButton>
    </li>
    );
}
export default Todo;